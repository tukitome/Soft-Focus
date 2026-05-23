from functions import *


def main():
	data = load_data()

	username = get_username(data)

	current_user = User(data)

	print("\nWelcome back, " + current_user.username + "!")
	print("Focus days:", current_user.focus_days)
	print("Points:", current_user.points)

	while True:
		show_menu()

		choice = input("Choose an option: ")

		if choice == "1":
			run_warmup_then_focus(data)

		elif choice == "2":
			run_focus_session(data, False)

		elif choice == "3":
			run_recommended_warmup(data)

		elif choice == "4":
			run_manual_warmup(data)

		elif choice == "5":
			show_focus_report(data)

		elif choice == "6":
			clear_statistics(data)

		elif choice == "7":
			save_data(data)
			print("Goodbye☆")
			break

		else:
			print("Invalid input.")


if __name__ == "__main__":
	main()
