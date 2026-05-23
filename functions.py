import random
import time
from datetime import datetime

# User class
class User:
	def __init__(self, data):
		self.username = data["username"]
		self.points = data["points"]
		self.streak = data["streak"]
		self.focus_days = data["focus_days"]

# Data Functions

def load_data():
	data = {
		"username": "none",
		"points": 0,
		"streak": 0,
		"focus_days": 0,
		"last_checkin_date": "none",
		"last_focus_date": "none",
		"warmup_records": [],
		"focus_records": []
	}

	try:
		file = open("save.txt", "r")
		lines = file.readlines()

		for line in lines:
			line = line.strip()

			if line == "":
				continue

			parts = line.split("=")

			if len(parts) != 2:
				continue

			key = parts[0]
			value = parts[1]

			if key == "username":
				data["username"] = value

			elif key == "points":
				data["points"] = int(value)

			elif key == "streak":
				data["streak"] = int(value)

			elif key == "focus_days":
				data["focus_days"] = int(value)

			elif key == "last_checkin_date":
				data["last_checkin_date"] = value

			elif key == "last_focus_date":
				data["last_focus_date"] = value

			elif key == "warmup_records":
				if value != "":
					record_strings = value.split(",")

					for record in record_strings:
						data["warmup_records"].append(float(record))

			elif key == "focus_records":
				if value != "":
					data["focus_records"] = value.split(",")

		file.close()

	except FileNotFoundError:
		save_data(data)

	return data


def save_data(data):
	file = open("save.txt", "w")

	file.write("username=" + data["username"] + "\n")
	file.write("points=" + str(data["points"]) + "\n")
	file.write("streak=" + str(data["streak"]) + "\n")
	file.write("focus_days=" + str(data["focus_days"]) + "\n")
	file.write("last_checkin_date=" + data["last_checkin_date"] + "\n")
	file.write("last_focus_date=" + data["last_focus_date"] + "\n")

	warmup_text = ""

	for i in range(len(data["warmup_records"])):
		warmup_text += str(data["warmup_records"][i])

		if i != len(data["warmup_records"]) - 1:
			warmup_text += ","

	file.write("warmup_records=" + warmup_text + "\n")

	focus_text = ""

	for i in range(len(data["focus_records"])):
		focus_text += data["focus_records"][i]

		if i != len(data["focus_records"]) - 1:
			focus_text += ","

	file.write("focus_records=" + focus_text + "\n")

	file.close()


def get_username(data):
	if data["username"] == "none":
		name = input("What's your name? ")
		data["username"] = name
		save_data(data)

	return data["username"]


def get_today_date():
	now = datetime.now()
	today = now.strftime("%Y-%m-%d")

	return today


def update_streak(data):
	today = get_today_date()

	if data["last_checkin_date"] != today:
		data["streak"] += 1
		data["last_checkin_date"] = today


def update_focus_days(data):
	today = get_today_date()

	if data["last_focus_date"] != today:
		data["focus_days"] += 1
		data["last_focus_date"] = today


def add_warmup_record(data, game_name, difficulty, score, total):
	if total == 0:
		accuracy = 0

	else:
		accuracy = score / total

	data["warmup_records"].append(accuracy)

	points = 5

	if accuracy >= 0.8:
		points += 3

	data["points"] += points

	update_streak(data)

	print("Warm-up accuracy:", accuracy)
	print("You earned " + str(points) + " points.")


def add_focus_record(data, period, score):
	record = period + ":" + str(score)
	data["focus_records"].append(record)


def clear_statistics(data):
	username = data["username"]

	data["points"] = 0
	data["streak"] = 0
	data["focus_days"] = 0
	data["last_checkin_date"] = "none"
	data["last_focus_date"] = "none"
	data["warmup_records"] = []
	data["focus_records"] = []
	data["username"] = username

	save_data(data)

	print("Statistics cleared.")


# Menu Functions

def show_menu():
	print("\n☆=== Soft Focus ===☆")
	print("1. Warm-up + focus session")
	print("2. Focus only")
	print("3. Warm-up only")
	print("4. Choose warm-up manually")
	print("5. View focus report")
	print("6. Clear statistics")
	print("7. Exit")


def recommend_game(data):
	games = ["memory_pulse", "number_trail", "word_check", "focus_filter", "rule_switch"]

	random_game = random.choice(games)

	return random_game


def run_warmup_set(data):
	difficulty = get_adaptive_difficulty(data)

	games = ["memory_pulse", "number_trail", "word_check", "focus_filter", "rule_switch"]

	chosen_games = random.sample(games, 3)

	total_score = 0
	total_possible = 0

	print("\nToday's warm-up set")
	print("Difficulty:", difficulty)
	print("You will play 3 short mini-games.\n")

	for game_name in chosen_games:
		print("\nNext game:", game_name)

		score, total = run_game(game_name, difficulty)

		total_score += score
		total_possible += total

	add_warmup_record(data, "warmup_set", difficulty, total_score, total_possible)

	save_data(data)

	print("\nWarm-up set complete.")
	print("Total score:", total_score, "/", total_possible)

	return total_score, total_possible


def run_warmup_then_focus(data):
	run_warmup_set(data)

	print("\nNow start your focus session.")
	run_focus_session(data, True)


def run_recommended_warmup(data):
	difficulty = get_adaptive_difficulty(data)

	game_name = recommend_game(data)

	print("\nToday's recommended warm-up:")
	print(game_name)
	print("Difficulty:", difficulty)

	score, total = run_game(game_name, difficulty)

	add_warmup_record(data, game_name, difficulty, score, total)

	save_data(data)

	print("Warm-up complete.")
	print("Score:", score, "/", total)


def choose_difficulty():
	print("\nChoose difficulty:")
	print("1. Easy")
	print("2. Medium")
	print("3. Hard")

	choice = input("Choose difficulty: ")

	if choice == "1":
		return 1

	elif choice == "2":
		return 2

	elif choice == "3":
		return 3

	else:
		print("[!]Invalid choice. Difficulty set to Medium.")
		return 2


def run_manual_warmup(data):
	difficulty = choose_difficulty()

	print("\nEnter the number to choose a game:")
	print("1. 🧠 Memory Pulse")
	print("2. 👣 Number Trail")
	print("3. ❓ Word Check")
	print("4. ⏳ Focus Filter")
	print("5. 🎯 Rule Switch")

	choice = input("Choose a game: ")

	if choice == "1":
		game_name = "memory_pulse"

	elif choice == "2":
		game_name = "number_trail"

	elif choice == "3":
		game_name = "word_check"

	elif choice == "4":
		game_name = "focus_filter"

	elif choice == "5":
		game_name = "rule_switch"

	else:
		print("[!]Invalid choice.")
		return

	print("Difficulty:", difficulty)

	score, total = run_game(game_name, difficulty)

	add_warmup_record(data, game_name, difficulty, score, total)

	save_data(data)

	print("Warm-up complete.")
	print("Score:", score, "/", total)


# Game Mechanic Functions

def make_typo(word):
	# Change the position of two nearby letters for Word Check.
	if len(word) < 2:
		return word

	word_list = list(word)

	index = random.randint(0, len(word) - 2)

	temp = word_list[index]
	word_list[index] = word_list[index + 1]
	word_list[index + 1] = temp

	typo_word = "".join(word_list)

	return typo_word


def make_sequence(difficulty):
# Generate a structure-fixed sequence by random words for Memory Pulse.
	skeleton_list = ["I", "made by", "in the", "for my"]

	verb_list = [
		"eat", "have", "kick", "look at", "generate",
		"listen to", "buy", "feed", "give", "cook", "grow"
	]

	noun_list = [
		"Shingeki no Kyojin", "Demon Slayer", "strawberry cakes",
		"birds", "bin chicken", "bubble teas", "Malatang",
		"Coke Cola", "brothers", "sisters", "husbands", "CPU",
		"Valorant", "boiled water", "lunch", "teeth", "geese",
		"Hatsune Miku", "USB-C", "Eren Jeager", "COMP9001", "Batman", 
		"Peter Parker", "Vergil", "Sushi", "Arknights"
	]

	place_list = [
		"garden", "university", "BSB teaching building", "room",
		"Fisher library", "balcony", "swimming pool",
		"Wall Maria", "backroom"
	]

	verb = random.choice(verb_list)
	noun_1 = random.choice(noun_list)
	place = random.choice(place_list)

	if difficulty == 1:
		sequence = [
			skeleton_list[0],
			verb,
			noun_1,
			skeleton_list[2],
			place
		]

	elif difficulty == 2:
		noun_2 = random.choice(noun_list)

		sequence = [
			skeleton_list[0],
			verb,
			noun_1,
			skeleton_list[1],
			noun_2,
			skeleton_list[2],
			place
		]

	else:
		noun_2 = random.choice(noun_list)
		noun_3 = random.choice(noun_list)

		sequence = [
			skeleton_list[0],
			verb,
			noun_1,
			skeleton_list[1],
			noun_2,
			skeleton_list[2],
			place,
			skeleton_list[3],
			noun_3
		]

	return sequence


def make_filter_string(string_length, target_count_range):
# Generate a string with multiple target letters for Focus Filter.
	letters = ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T"]

	target_letter = random.choice(["A", "E", "I", "O", "U"])

	target_count = random.randint(target_count_range[0], target_count_range[1])

	characters = []

	for i in range(string_length):
		characters.append(random.choice(letters))

	target_indexes = random.sample(range(string_length), target_count)

	for index in target_indexes:
		characters[index] = target_letter

	return characters, target_letter, target_count


# Run Game Functions
def run_game(game_name, difficulty):
	if game_name == "memory_pulse":
		return run_memory_pulse(difficulty)

	elif game_name == "number_trail":
		return run_number_trail(difficulty)

	elif game_name == "word_check":
		return run_word_check(difficulty)

	elif game_name == "focus_filter":
		return run_focus_filter(difficulty)

	elif game_name == "rule_switch":
		return run_rule_switch(difficulty)

	else:
		print("Please enter a valid game! ")
		return 0, 1


def run_memory_pulse(difficulty):

# Memory Pulse mini-game.
# User needs to remember the sequence and type it correctly.

# Return:score, total

	sequence = make_sequence(difficulty)

	print("Remember this sentence:")
	print(" ".join(sequence))

	input("\nPress Enter when ready to continue...")

	print("\n" * 20)

	user_answer = input("Type the sentence in order: ")

	correct_answer = " ".join(sequence)

	if user_answer == correct_answer:
		print("Correct☆")
		return 1, 1

	else:
		print("Not quite.")
		print("The answer was:")
		print(correct_answer)
		return 0, 1



def run_number_trail(difficulty):

# Number Trail mini-game.
# User needs to sort the numbers from smallest to largest.

# Return:score, total

	if difficulty == 1:
		count = 4
		max_number = 50

	elif difficulty == 2:
		count = 5
		max_number = 100

	else:
		count = 6
		max_number = 199

	numbers = random.sample(range(1, max_number + 1), count)

	while numbers == sorted(numbers):
		numbers = random.sample(range(1, max_number + 1), count)

	correct_order = sorted(numbers)

	print("\n=== Number Trail ===")
	print("Sort the numbers from smallest to largest.")
	print("Type your answer with spaces between numbers.\n")

	print("Numbers:")
	print(numbers)

	user_answer = input("Your answer: ")

	user_parts = user_answer.split()

	user_numbers = []

	for part in user_parts:
		if part.isdigit():
			user_numbers.append(int(part))

		else:
			print("[!]Please only enter numbers with correct format.")
			return 0, 1

	if user_numbers == correct_order:
		print("Correct☆\n")
		return 1, 1

	else:
		print("Not quite.")
		print("Correct answer:", correct_order)
		return 0, 1



def run_word_check(difficulty):

# Word Check mini-game.
# User needs to find the word with incorrect letter order.

# Return:score, total

	if difficulty == 1:
		word_bank = [
			"friend", "Merlin", "people", "Thor", "before", "zombie", "plant", 
			"Overwatch", "practice", "Arknights", "Loki", "Valorant"
		]
		rounds = 3

	elif difficulty == 2:
		word_bank = [
			"because", "morning", "student", "Ragnarok", "between", "Parramatta", 
			"DevilMayCry", "Sekiro", "CounterStrike2", "Avocado", "Darksoul", "Cyberpunk2077"
		]
		rounds = 4

	else:
		word_bank = [
			"attention", "pronunciation", "addition", "Ulaanbaatar", "LeviAckerman", 
			"CopacabanaBeach", "electromagnetic", "Woolloomooloo", "pharaoh", "rhythm", 
			"ParadiIsland", "conscientious", "Unknown Mother Goose", "ArthurPendragon"
		]
		rounds = 5

	score = 0
	total = rounds

	print("\n=== Word Check ===")
	print("Find the word with incorrect letter order.")
	print("Type the number of the wrong word.\n")

	selected_words = random.sample(word_bank, rounds)

	for round_number in range(1, rounds + 1):

		correct_word = selected_words[round_number - 1]
		wrong_word = make_typo(correct_word)

		# Avoid the rare case where typo is same as original
		while wrong_word == correct_word:
			wrong_word = make_typo(correct_word)

		options = [correct_word, correct_word, correct_word, wrong_word]
		random.shuffle(options)

		answer_index = options.index(wrong_word) + 1

		print(f"Round {round_number}/{rounds}")

		for i in range(len(options)):
			print(f"{i + 1}. {options[i]}")

		user_answer = input("Your answer: ")

		if user_answer.isdigit():

			user_answer = int(user_answer)

			if user_answer == answer_index:
				print("Correct☆\n")
				score += 1

			else:
				print(f"Not quite. The answer was {answer_index}.\n")

		else:
			print(f"[!]Please enter a number next time. The answer was {answer_index}.\n")
			continue

	print(f"Word Check complete: {score}/{total}\n")

	return score, total


def run_focus_filter(difficulty):

# Focus Filter mini-game.
# User needs to count how many times a target character appears.

# Return:score, total

	if difficulty == 1:
		string_length = 8
		target_count_range = [1, 2]

	elif difficulty == 2:
		string_length = 12
		target_count_range = [2, 4]

	else:
		string_length = 16
		target_count_range = [3, 5]

	characters, target_letter, target_count = make_filter_string(string_length, target_count_range)

	print("\n=== Focus Filter ===")
	print(f"Count how many times the letter {target_letter} appears.\n")

	print(" ".join(characters))

	user_answer = input("\nYour answer: ")

	if user_answer.isdigit():
		user_answer = int(user_answer)

		if user_answer == target_count:
			print("Correct☆\n")
			return 1, 1

		else:
			print(f"Not quite. The answer was {target_count}.\n")
			return 0, 1

	else:
		print(f"Please enter a number next time. The answer was {target_count}.\n")
		return 0, 1    


def run_rule_switch(difficulty):

# Rule Switch mini-game.
# User converts symbols or letters based on given rules.

# Return:score, total

	if difficulty == 1:
		rule = {
			"🌸": "Q",
			"🚀": "S"
		}
		rounds = 2
		min_length = 4
		max_length = 7

	elif difficulty == 2:
		rule = {
			"Q": "h",
			"K": "c"
		}
		rounds = 4
		min_length = 5
		max_length = 9

	else:
		rule = {
			"M": "P",
			"D": "A"
		}
		rounds = 6
		min_length = 6
		max_length = 11

	score = 0
	total = rounds

	print("\n=== Rule Switch ===")
	print("Respond using the matching keys.")
	print("If you make a mistake, the game stops.\n")

	for key in rule:
		print(key + " = " + rule[key])

	print()

	symbols = list(rule.keys())

	for round_number in range(1, rounds + 1):
		length = random.randint(min_length, max_length)

		sequence = []

		for i in range(length):
			sequence.append(random.choice(symbols))

		correct_answer = ""

		for item in sequence:
			correct_answer += rule[item]

		print("Round " + str(round_number) + "/" + str(rounds))
		print("Sequence:")
		print(" ".join(sequence))

		user_answer = input("Your answer: ")

		if user_answer == correct_answer:
			print("Correct☆\n")
			score += 1

		else:
			print("Not quite.")
			print("Correct answer was: " + correct_answer)
			print("Rule Switch stopped.\n")
			break

	print("Rule Switch complete: " + str(score) + "/" + str(total) + "\n")

	return score, total


# Adaptive Functions

def get_adaptive_difficulty(data):
	records = data["warmup_records"]

	if len(records) == 0:
		return 2

	recent_records = records[-3:]

	total_accuracy = 0

	for accuracy in recent_records:
		total_accuracy += accuracy

	average_accuracy = total_accuracy / len(recent_records)

	if average_accuracy >= 0.8:
		return 3

	elif average_accuracy >= 0.5:
		return 2

	else:
		return 1


# Focus Session Functions

def run_focus_session(data, after_warmup):
	print("\n=== Focus Session ===")

	task = input("Focus task: ")
	duration = input("Focus duration in minutes: ")

	if duration.isdigit():
		duration = int(duration)
	else:
		duration = 10

	print("\nGoal:", task, "for", duration, "minutes.")
	finish = input('Type "done" when finished: ')

	if finish.lower() == "done":
		score_input = input("Focus score 1-10: ")

		if score_input.isdigit():
			score = int(score_input)
		else:
			score = 5

		if score < 1:
			score = 1
		elif score > 10:
			score = 10

		period = get_time_period()

		add_focus_record(data, period, score)
		update_focus_days(data)

		points = int(duration / 5) * 5

		if after_warmup:
			points += 5

		data["points"] += points

		save_data(data)

		print("Focus complete. +" + str(points) + " points.")

	else:
		print("Focus session not recorded.")


def get_time_period():
	now = datetime.now()
	hour = now.hour

	if hour >= 5 and hour <= 11:
		return "morning"

	elif hour >= 12 and hour <= 16:
		return "afternoon"

	elif hour >= 17 and hour <= 21:
		return "evening"

	else:
		return "night"


# Report Functions

def show_focus_report(data):
	print("\n=== Focus Report ===")

	if len(data["focus_records"]) == 0:
		print("No focus records yet.")
		return

	period_scores = {
		"morning": [],
		"afternoon": [],
		"evening": [],
		"night": []
	}

	for record in data["focus_records"]:
		parts = record.split(":")

		if len(parts) == 2:
			period = parts[0]
			score = int(parts[1])

			if period in period_scores:
				period_scores[period].append(score)

	best_period = "none"
	best_average = 0

	for period in period_scores:
		scores = period_scores[period]

		if len(scores) > 0:
			total = 0

			for score in scores:
				total += score

			average = total / len(scores)

			print(period + " average:", average)

			if average > best_average:
				best_average = average
				best_period = period

	print("\nTotal focus days:", data["focus_days"])
	print("Total points:", data["points"])

	if best_period != "none":
		print("Your best focus period seems to be:", best_period)
		print("Average score:", best_average)
