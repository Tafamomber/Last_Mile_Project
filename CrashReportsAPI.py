import requests
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from collections import defaultdict


class CrashReport:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master, padding="10", relief="solid")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.fetch_crash_data()
        self.create_widgets()

    def fetch_crash_data(self):
        response = requests.get("https://data.cincinnati-oh.gov/resource/rvmt-pkmq")
        crash_data = response.json()

        self.total_crashes = 0
        self.crashes_with_date = 0
        self.crashes_by_day = {"MON": 0, "TUE": 0, "WED": 0, "THU": 0, "FRI": 0, "SAT": 0, "SUN": 0}  # Counts crashes for each day of the week

        for crash in crash_data:   # loop over each crash
            self.total_crashes += 1
            crash_date_str = crash.get('crashdate')
            day_of_week = crash.get('dayofweek')

            if crash_date_str and day_of_week:
                self.crashes_with_date += 1
                self.crashes_by_day[day_of_week] += 1
        self.calculate_weekly_data(crash_data)

    def calculate_weekly_data(self, crash_data):
        self.crashes_by_day = defaultdict(int)
        self.total_weeks = set()

        for crash in crash_data:
            crash_date_str = crash.get('crashdate')
            day_of_week = crash.get('dayofweek')

            if crash_date_str and day_of_week:
                crash_date = datetime.strptime(crash_date_str, "%Y-%m-%dT%H:%M:%S.%f")
                week_number = crash_date.isocalendar()[1]
                year = crash_date.year

                self.total_weeks.add((year, week_number))
                self.crashes_by_day[day_of_week] += 1

        self.num_weeks = len(self.total_weeks)
        self.average_crashes_per_day = {day: self.crashes_by_day[day] / self.num_weeks for day in self.crashes_by_day}
        self.calculate_date_range(crash_data)

    def calculate_date_range(self, crash_data):
        crash_dates = [
            datetime.strptime(crash.get('crashdate'), "%Y-%m-%dT%H:%M:%S.%f")
            for crash in crash_data if crash.get('crashdate')
        ]
        if crash_dates:  # Check if crash_dates is not empty
            self.min_date = min(crash_dates)
            self.max_date = max(crash_dates)
        else:
            self.min_date = None
            self.max_date = None

    def create_widgets(self):
        # Labels
        total_crashes_label = ttk.Label(self.frame, text=f'Total Crashes: {self.total_crashes}')
        total_crashes_label.pack(pady=5)

        crashes_with_date_label = ttk.Label(self.frame, text=f'Crashes with date: {self.crashes_with_date}')
        crashes_with_date_label.pack(pady=5)

        crashes_by_day_label = ttk.Label(self.frame, text="Crashes by day of week:")
        crashes_by_day_label.pack(pady=5)

        days_order = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        for day in days_order:
            day_label = ttk.Label(self.frame, text=f'{day}: {self.crashes_by_day[day]}')
            day_label.pack()

        num_weeks_label = ttk.Label(self.frame, text=f'Number of weeks in the dataset: {self.num_weeks}')
        num_weeks_label.pack(pady=5)

        for day in days_order:
            avg_day_label = ttk.Label(self.frame, text=f'Average crashes on {day}: {self.average_crashes_per_day[day]:.2f}')
            avg_day_label.pack()

        date_range_label = ttk.Label(self.frame, text=f'Data spans from {self.min_date.date()} to {self.max_date.date()}')
        date_range_label.pack(pady=5)
