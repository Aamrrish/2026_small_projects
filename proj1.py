import time
import datetime

DATA_FILE = "focus_log.txt"


def start_focus_session(minutes):
    total_seconds = minutes * 60
    start_time = time.time()

    print("\nFocus session started.")
    print("Do NOT exit. Press Ctrl+C = Distraction \n")

    try:
        while True:
            elapsed = int(time.time() - start_time)
            remaining = total_seconds - elapsed

            if remaining <= 0:
                print("\rTime Left: 00:00 ")
                print("\nSession completed successfully ")
                return True, total_seconds

            mins = remaining // 60
            secs = remaining % 60

            print(f"\rTime Left: {mins:02d}:{secs:02d}", end="")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nSession interrupted (Distraction detected)")
        focused_time = int(time.time() - start_time)
        return False, focused_time


def log_session(success, focused_seconds):
    today = datetime.date.today().isoformat()
    status = "SUCCESS" if success else "FAILED"

    with open(DATA_FILE, "a") as file:
        file.write(f"{today},{status},{focused_seconds}\n")


def show_today_report():
    today = datetime.date.today().isoformat()
    total_focus = 0
    success_count = 0
    fail_count = 0

    try:
        with open(DATA_FILE, "r") as file:
            for line in file:
                date, status, seconds = line.strip().split(",")

                if date == today:
                    total_focus += int(seconds)
                    if status == "SUCCESS":
                        success_count += 1
                    else:
                        fail_count += 1

    except FileNotFoundError:
        print("\nNo focus data found yet.")
        return

    print("\nTODAY'S FOCUS REPORT")
    print("----------------------")
    print(f"Completed Sessions : {success_count}")
    print(f"Failed Sessions    : {fail_count}")
    print(f"Total Focus Time   : {total_focus // 60} minutes")


def main_menu():
    while True:
        print("\n FOCUS GUARD")
        print("1. Start Focus Session")
        print("2. View Today's Report")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            try:
                minutes = int(input("Enter focus duration (minutes): "))
                success, focused_time = start_focus_session(minutes)
                log_session(success, focused_time)

            except ValueError:
                print("Please enter a valid number.")

        elif choice == "2":
            show_today_report()

        elif choice == "3":
            print("Stay disciplined. Exiting ")
            break

        else:
            print("Invalid choice. Try again.")


main_menu()
