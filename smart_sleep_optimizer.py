# Smart Sleep Cycle Optimizer
import datetime
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import requests
# Configuration 
DATA_FILE = Path(__file__).parent / "sleep_history.csv"
DEFAULT_CITY = "Vellore"

# Data Loading
def load_sleep_history():
    """Load sleep history from CSV if it exists."""
    if DATA_FILE.exists():
        return pd.read_csv(DATA_FILE).to_dict("records")
    return []


sleep_history = load_sleep_history()
# Weather Tip 
def get_weather_tip(city: str = DEFAULT_CITY) -> str:
    """Fetch temperature and return sleep advice."""
    try:
        url = f"https://wttr.in/{city}?format=%t"
        response = requests.get(url, timeout=5)
        temp = response.text.strip()

        temperature = int(temp.replace("°C", "").replace("+", ""))

        if temperature > 30:
            return (
                f"It's {temperature}°C — warm night! Keep your room cool for better sleep."
            )
        elif temperature < 20:
            return (
                f"It's {temperature}°C — cold weather! Use a blanket to sleep comfortably."
            )
        else:
            return f"The temperature is pleasant ({temperature}°C). Perfect night for good rest!"

    except Exception:
        return (
            "Couldn't fetch weather info, but remember: environment affects sleep quality."
        )


# ---------------- Core Logic ----------------
def optimized_cycles(age: int):
    """Return recommended sleep durations based on age."""
    if age < 18:
        return [9, 7.5, 6]
    elif age <= 25:
        return [7.5, 6, 4.5]
    elif age <= 40:
        return [7, 6, 4.5]
    elif age >= 60:
        return [8, 6.5, 5]
    else:
        return [6.5, 5, 4.5]


def suggest_habits(avg_sleep: float, mood_trend: float) -> str:
    """Provide lifestyle suggestions based on sleep data."""
    if avg_sleep < 6:
        suggestion = (
            "You are sleeping too little! Try earlier bedtime and avoid screens 1–2 hours before bed."
        )
    elif 6 <= avg_sleep <= 8:
        suggestion = "Excellent! Maintain consistent sleep and wake-up times."
    else:
        suggestion = "You might be oversleeping. Reduce naps or caffeine before bed."

    if mood_trend <= 3:
        suggestion += (
            " Also, try relaxing music or breathing exercises before bed for better mood."
        )
    elif mood_trend > 4:
        suggestion += " Keep it up! Your mood shows healthy rest."

    return suggestion

# Features
def sleep_now(age: int):
    """Suggest wake-up times if the user sleeps now."""
    now = datetime.datetime.now()

    print(f"\nCurrent time: {now.strftime('%I:%M %p')}")
    print("If you go to bed now, ideal wake-up times are:\n")

    fall_asleep = datetime.timedelta(minutes=15)

    for hrs in optimized_cycles(age):
        wake_time = now + fall_asleep + datetime.timedelta(hours=hrs)
        print(f" - {wake_time.strftime('%I:%M %p')} ({hrs:.1f} hrs sleep)")

    print("\n" + get_weather_tip())


def wake_up(age: int):
    """Suggest sleep times based on target wake-up time."""
    time_str = input("\nEnter your target wake-up time (HH:MM AM/PM): ")

    try:
        wake_time = datetime.datetime.strptime(time_str, "%I:%M %p")

        print("\nTo wake up refreshed, you should try sleeping at:\n")

        fall_asleep = datetime.timedelta(minutes=15)

        for hrs in optimized_cycles(age):
            sleep_time = wake_time - fall_asleep - datetime.timedelta(hours=hrs)
            print(f" - {sleep_time.strftime('%I:%M %p')} ({hrs:.1f} hrs before wake-up)")

        print("\n" + get_weather_tip())

    except ValueError:
        print("Invalid time format! Use HH:MM AM/PM.")


def log_sleep():
    """Log a sleep session and save to CSV."""
    try:
        s = input("\nEnter sleep time (HH:MM AM/PM): ")
        w = input("Enter wake time (HH:MM AM/PM): ")
        mood = int(input("Rate your refreshed mood next morning (1–5): "))

        s_time = datetime.datetime.strptime(s, "%I:%M %p")
        w_time = datetime.datetime.strptime(w, "%I:%M %p")

        if w_time < s_time:
            w_time += datetime.timedelta(days=1)

        duration = (w_time - s_time).seconds / 3600

        record = {
            "Sleep Time": s_time.strftime("%I:%M %p"),
            "Wake Time": w_time.strftime("%I:%M %p"),
            "Duration (hrs)": round(duration, 2),
            "Mood (1–5)": mood,
        }

        sleep_history.append(record)

        df = pd.DataFrame(sleep_history)
        df.to_csv(DATA_FILE, index=False)

        print(f"Logged {round(duration, 2)} hrs of sleep with mood {mood}/5.\n")

    except ValueError:
        print("Invalid time format. Example: 10:30 PM")


def analyze_history():
    """Analyze sleep history and show graph."""
    if not sleep_history:
        print("\nNo data yet! Log some sleep sessions first.")
        return

    df = pd.DataFrame(sleep_history)

    avg_sleep = df["Duration (hrs)"].mean()
    avg_mood = df["Mood (1–5)"].mean()

    print("\nSleep Analysis Summary:")
    print(f"- Average sleep duration: {avg_sleep:.2f} hours")
    print(f"- Average mood rating: {avg_mood:.1f}/5")

    print(suggest_habits(avg_sleep, avg_mood))

    plt.plot(df["Duration (hrs)"], marker="o", label="Sleep Duration")
    plt.plot(df["Mood (1–5)"], marker="x", label="Mood")

    plt.title("Sleep vs Mood Trend")
    plt.xlabel("Days")
    plt.ylabel("Value")

    plt.legend()
    plt.grid(True)

    plt.show()


# Main Menu
def main():
    print("****** SMART SLEEP CYCLE OPTIMIZER ******")

    name = input("Enter your name: ")

    try:
        age = int(input("Enter your age: "))
    except ValueError:
        print("Age must be a number.")
        return

    while True:
        print("\nChoose an option:")
        print("1. Sleep now (show wake-up times)")
        print("2. Plan bedtime (based on wake-up time)")
        print("3. Log a sleep session")
        print("4. Analyze my sleep patterns")
        print("5. Exit")

        choice = input("\nEnter your choice (1–5): ")

        if choice == "1":
            sleep_now(age)

        elif choice == "2":
            wake_up(age)

        elif choice == "3":
            log_sleep()

        elif choice == "4":
            analyze_history()

        elif choice == "5":
            print(f"\nGoodnight, {name}! Sleep smarter, live better.\n")
            break

        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
