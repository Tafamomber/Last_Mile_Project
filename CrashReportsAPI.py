import requests
import tkinter as tk
from datetime import datetime
from collections import defaultdict

response = requests.get("https://data.cincinnati-oh.gov/resource/rvmt-pkmq")
crash_data = response.json()

total_crashes = 0  # counter for total_crashes
crashes_with_date = 0  # counter for crashes with date
crashes_by_day = {
    "MON": 0, "TUE": 0, "WED": 0, "THU": 0, "FRI": 0, "SAT": 0, "SUN": 0
}  # Counts crashes for each day of the week


for crash in crash_data:   # loop over each crash
    total_crashes += 1
    crash_date_str = crash.get('crashdate')
    day_of_week = crash.get('dayofweek')

    if crash_date_str and day_of_week:
        crashes_with_date += 1
        crashes_by_day[day_of_week] += 1

print(f"Total Crashes: {total_crashes}")
print(f"Crashes with valid date: {crashes_with_date}")
print("Crashes by day of week:")
for day, count in crashes_by_day.items():
    print(f"{day}: {count}")


crashes_by_day = defaultdict(int)
total_weeks = set()

for crash in crash_data:
    crash_date_str = crash.get('crashdate')
    day_of_week = crash.get('dayofweek')

    if crash_date_str and day_of_week:
        crash_date = datetime.strptime(crash_date_str, "%Y-%m-%dT%H:%M:%S.%f")
        week_number = crash_date.isocalendar()[1]
        year = crash_date.year

        total_weeks.add((year, week_number))
        crashes_by_day[day_of_week] += 1
num_weeks = len(total_weeks)
print(f"Number of weeks in the dataset: {num_weeks}")
print("Average crashes per day of week: ")
days_order = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
for day in days_order:
    avg_crashes = crashes_by_day[day] / num_weeks
    print(f"{day}: {avg_crashes:.2f}")
total_crashes = sum(crashes_by_day.values())
overall_daily_avg = total_crashes / (num_weeks * 7)
print(f"Overall Daily Average: {overall_daily_avg:.2f}")

crash_dates = [datetime.strptime(crash.get('crashdate'), "%Y-%m-%dT%H:%M:%S.%f"
                                 ) for crash in crash_data if crash.get
                                ('crashdate')]
min_date = min(crash_dates)
max_date = max(crash_dates)
print(f"Data spans from {min_date.date()} to {max_date.date()}")

# GUI
root = tk.Tk()
root.title("Crash Report Data")

# Window
root.geometry("400x350")
root.config(bg="#f0f0f0")

# Labels
total_crashes_label = tk.Label(root,
                               text=f'Total Crashes: {total_crashes}',
                               bg="#f0f0f0")
total_crashes_label.pack(pady=5)

crashes_with_date_label = tk.Label(
    root,
    text=f'Crashes with date:{crashes_with_date}',
    bg="#f0f0f0")
crashes_with_date_label.pack(pady=5)

crashes_by_day_label = tk.Label(root,
                                text="Crashes by day of week:",
                                bg="#f0f0f0")
crashes_by_day_label.pack(pady=5)
for day in days_order:
    day_label = tk.Label(root,
                         text=f'{day}: {crashes_by_day[day]}',
                         bg="#f0f0f0")
    day_label.pack()

num_weeks_label = tk.Label(root,
                           text=f'Number of weeks in the dataset: {num_weeks}',
                           bg="#f0f0f0")
num_weeks_label.pack(pady=5)

for day in days_order:
    avg_crashes = crashes_by_day[day] / num_weeks
    avg_day_label = tk.Label(
        root,
        text=f'Average crashes on {day}: {avg_crashes:.2f}',
        bg="#f0f0f0")
    avg_day_label.pack()

date_range_label = tk.Label(
    root,
    text=f'Data spans from {min_date.date()} to {max_date.date()}',
    bg="#f0f0f0")
date_range_label.pack(pady=5)

root.mainloop()
