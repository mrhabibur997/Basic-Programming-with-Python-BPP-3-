import csv
import datetime


ACTIVITIES = {
    'Running': 15,
    'Cycling': 9,
    'Yoga': 3.5,
    'Swimming': 7,
    'Pushups': 3,
    'Sit-ups': 3,
    'Stretching': 3
}


ACTIVITY_HISTORY_FILE = "C:/Users/ASUS/Desktop/Project/activity_history.csv"
FITNESS_GOALS_FILE = "C:/Users/ASUS/Desktop/Project/fitness_goals.csv"


def log_activity():
    """Logs a new activity to the CSV file."""
    date = input("Enter the date (YYYY-MM-DD): ")
    activity_name = input("Enter activity name (or type 'Custom' to add a new one): ")

    if activity_name == 'Custom':
        activity_name = input("You are adding a new activity. Please enter the name of the activity: ")
        calories_per_minute = float(input("Enter the calories burned per minute for this new activity: "))
        ACTIVITIES[activity_name] = calories_per_minute  # Add new activity to the dictionary
    else:
        if activity_name not in ACTIVITIES:
            print(f"{activity_name} is not in the preset activities list.")
            return  

        calories_per_minute = ACTIVITIES[activity_name]

    duration = int(input("Enter the duration in minutes: "))
    calories_burned = duration * calories_per_minute

    with open(ACTIVITY_HISTORY_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, activity_name, duration, calories_burned])

    print(f"Activity logged: {activity_name} for {duration} minutes, Calories burned: {calories_burned}")

def view_activity_history():
    try:
        with open(ACTIVITY_HISTORY_FILE, mode='r') as file:
            reader = csv.reader(file)
            activities = list(reader)
            for activity in activities:
                print(activity)
    except FileNotFoundError:
        print("No activity history found.")

def load_data():
    try:
        with open(ACTIVITY_HISTORY_FILE, mode='r') as file:
            reader = csv.reader(file)
            return list(reader)
    except FileNotFoundError:
        print("No data found.")
        return []

def summary_by_period(start_date, period='week'):
    activities = load_data()
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = start_date

    if period == 'week':
        end_date = datetime.datetime(start_date.year, start_date.month, start_date.day + 6)
    elif period == 'month':
        if start_date.month == 12:
            end_date = datetime.datetime(start_date.year + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            end_date = datetime.datetime(start_date.year, start_date.month + 1, 1) - datetime.timedelta(days=1)

    total_duration = 0
    total_calories = 0
    for activity in activities:
        activity_date = datetime.datetime.strptime(activity[0], "%Y-%m-%d")
        if start_date <= activity_date <= end_date:
            total_duration += int(activity[2])
            total_calories += float(activity[3])
    
    print(f"From {start_date.date()} to {end_date.date()}, you have:")
    print(f"- Total duration: {total_duration} minutes")
    print(f"- Total calories burned: {total_calories}")

def set_fitness_goal():
    calories_goal = int(input("Enter the calorie goal: "))
    goal_date = input("Enter the goal date (YYYY-MM-DD): ")

    with open(FITNESS_GOALS_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([goal_date, calories_goal])

    print(f"Fitness goal set: Burn {calories_goal} calories on {goal_date}")

def view_progress_reports():
    """Checks progress towards a fitness goal set for a specific date."""
    goal_date = input("Enter the goal date (YYYY-MM-DD) to check progress: ")
    goal_date = datetime.datetime.strptime(goal_date, "%Y-%m-%d").date()

    try:
        with open(FITNESS_GOALS_FILE, mode='r') as file:
            reader = csv.reader(file)
            goal_calories = 0
            for row in reader:
                if datetime.datetime.strptime(row[0], "%Y-%m-%d").date() == goal_date:
                    goal_calories = int(row[1])
                    break

        with open(ACTIVITY_HISTORY_FILE, mode='r') as file:
            reader = csv.reader(file)
            total_calories = sum(int(activity[3]) for activity in reader if datetime.datetime.strptime(activity[0], "%Y-%m-%d").date() == goal_date)

        if goal_calories == 0:
            print("No goal set for this date.")
            return

        if total_calories >= goal_calories:
            print(f"Goal achieved! Burned {total_calories} calories on {goal_date}, goal was {goal_calories}.")
        else:
            print(f"Goal not met. Burned {total_calories} calories on {goal_date}, goal was {goal_calories}.")
    except FileNotFoundError:
        print("No goal set or activities logged for this date.")

def main_menu():
    while True:
        print("\n--- Fitness Tracker Menu ---")
        print("1. Log a new activity")
        print("2. View activity history")
        print("3. Progress Monitoring")
        print("4. Set and update fitness goals")
        print("5. View progress reports")
        print("6. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            log_activity()
        elif choice == '2':
            view_activity_history()
        elif choice == '3':
            start_date = input("Enter the start date (YYYY-MM-DD): ")
            period = input("Weekly or Monthly summary? Enter 'week' or 'month': ")
            summary_by_period(start_date, period)
        elif choice == '4':
            set_fitness_goal()
        elif choice == '5':
            view_progress_reports()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()
