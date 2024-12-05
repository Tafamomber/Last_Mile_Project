import tkinter as tk
from tkinter import ttk
from EventsAPI_GUI import EventsFrame
from trafficAPI_GUI import TrafficFrame  # Import TrafficFrame from trafficAPI_GUI.py
import requests
from datetime import datetime
from PIL import Image, ImageTk
from CrashReportsAPI import CrashReport

class WeatherApp:
    def __init__(self, master):
        self.master = master
        self.city = "Cincinnati"
        self.api_key = "bd7f96bc0c1c57950270daa8c1d2682a"  # Replace with your OpenWeatherMap API key

        master.config(background="white")
        # Weather Label
        self.weather_label = tk.Label(master, text="Weather", font=("Times New Roman", 16, "bold"), bg="white")
        self.weather_label.pack(pady=10)

        # Labels for weather information
        self.temp_label = tk.Label(master, text="", font=("Times New Roman", 14), bg="white")
        self.temp_label.pack(pady=5)

        self.humidity_label = tk.Label(master, text="", font=("Times New Roman", 14), bg="white")
        self.humidity_label.pack(pady=5)

        self.desc_label = tk.Label(master, text="", font=("Times New Roman", 14), bg="white")
        self.desc_label.pack(pady=5)

        self.last_update_label = tk.Label(master, text="", font=("Times New Roman", 12, "italic"), bg="white")
        self.last_update_label.pack(pady=5)

        self.update_weather()  # Initialize weather data

    def get_weather_data(self):
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=imperial"
        response = requests.get(base_url)
        if response.status_code == 200:
            return response.json()
        return None

    def update_weather(self):
        weather_data = self.get_weather_data()
        if weather_data and 'main' in weather_data:
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']

            self.temp_label.config(text=f"Temperature: {temp} °F")
            self.humidity_label.config(text=f"Humidity: {humidity} %")
            self.desc_label.config(text=f"Weather: {description}")
            self.last_update_label.config(text=f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            self.temp_label.config(text="Error fetching weather data")

        # Update every minute
        self.master.after(60000, self.update_weather)

def update_week_date_label(label):
    now = datetime.now()
    week_number = now.strftime("%U")  # ISO week number
    current_date = now.strftime("%A, %B %d, %Y")
    label.config(text=f"Week: {week_number} | Date: {current_date}")
    # Update every 24 hours (86400000 ms)
    label.after(86400000, lambda: update_week_date_label(label))

# Create the main window
root = tk.Tk()
root.title("Main GUI")
root.geometry("800x600")  # Set a fixed window size
root.config(bg="orange")

# Define grid layout for the GUI
root.columnconfigure(0, weight=2)  # Left column (Weather) gets more weight
root.columnconfigure(1, weight=1)  # Center column (Traffic, Active Users, Crash Report)
root.columnconfigure(2, weight=2)  # Right column (Events) gets more weight
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=4)  # Middle row for traffic/crash reports
root.rowconfigure(2, weight=3)  # Bottom row for weather/events

padding_val = 10

# Top row layout (Week/Date bar, Prev/Next Week buttons)
prev_week_button = ttk.Button(root, text="Previous Week")
prev_week_button.grid(row=0, column=0, sticky="nw", padx=padding_val, pady=padding_val, ipadx=5, ipady=5)

# Week/Date bar
week_date_bar = tk.Frame(root, relief="solid", bg="white")
week_date_bar.grid(row=0, column=1, sticky="nsew", padx=padding_val, pady=padding_val)
week_date_label = tk.Label(week_date_bar, text="Week / Date", anchor="center", bg="white")
week_date_label.pack(expand=True)

update_week_date_label(week_date_label)

# Adjust logo placement: Add an extra row for the logo if needed
logo_frame = tk.Frame(root, background="orange")
logo_frame.grid(row=2, column=1, sticky="nsew", padx=padding_val, pady=(0, padding_val))

logo_image_pil = Image.open("/Users/xlcarplx/Desktop/LastMile/image.jpeg")
logo_image_pil = logo_image_pil.resize((350, 350), Image.LANCZOS)
logo_image = ImageTk.PhotoImage(logo_image_pil)
logo_label = tk.Label(logo_frame, image=logo_image, bg="orange")
logo_label.pack(expand=True, anchor="center")

# Next Week button
next_week_button = ttk.Button(root, text="Next Week")
next_week_button.grid(row=0, column=2, sticky="ne", padx=padding_val, pady=padding_val, ipadx=5, ipady=5)

# Middle section layout (Traffic, Active Users, Crash Report)
traffic_frame = tk.Frame(root, relief="solid", bg="white")
traffic_frame.grid(row=1, column=0, sticky="nsew", padx=padding_val, pady=padding_val)

# Add TrafficFrame directly into traffic_frame to fill the space
traffic_api_interface = TrafficFrame(traffic_frame)  # Instantiate the traffic API interface
traffic_api_interface.pack(fill=tk.BOTH, expand=True)

active_users_frame = tk.Frame(root, relief="solid", bg="white", highlightbackground="white", highlightthickness=0, bd=3)
active_users_frame.grid(row=1, column=1, sticky="nsew", padx=padding_val, pady=padding_val)
active_users_label = tk.Label(active_users_frame, text="How many people expected to be active today", anchor="center", bg="white")
active_users_label.pack(expand=True)

crash_report_frame = tk.Frame(root, relief="solid", bg="white", highlightbackground="white", highlightthickness=0, bd=3)
crash_report_frame.grid(row=1, column=2, sticky="nsew", padx=padding_val, pady=padding_val)
crash_report_label = tk.Label(crash_report_frame, text="Crash Report", anchor="center", bg="white")
crash_report_label.pack(expand=True)
crash_report_app = CrashReport(crash_report_frame)

# Bottom section layout (Weather and Events)
weather_frame = tk.Frame(root, relief="solid", bg="white", highlightbackground="white", highlightthickness=0, bd=3)
weather_frame.grid(row=2, column=0, sticky="nsew", padx=padding_val, pady=padding_val)

weather_app = WeatherApp(weather_frame)

events_frame = tk.Frame(root, relief="solid", bg="white", highlightbackground="white", highlightthickness=0, bd=3)
events_frame.grid(row=2, column=2, sticky="nsew", padx=padding_val, pady=padding_val)
events_app = EventsFrame(events_frame)
events_app.pack(fill="both", expand=True)

# Run the main loop
root.mainloop()
