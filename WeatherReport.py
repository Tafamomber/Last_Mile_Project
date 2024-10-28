import requests
import tkinter as tk
from datetime import datetime

# Fetch weather data from OpenWeatherMap API
def get_weather_data(city, api_key):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
    response = requests.get(base_url)
    print(f"API URL: {response.url}")
    print(f"Response Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    if response.status_code != 200:
        return None  # Handle error case
    return response.json()

# Predict volunteer availability based on weather conditions (temperature, precipitation)
def predict_volunteer_availability(temp, weather_desc, precipitation):
    if precipitation > 0:  # If there's precipitation (rain/snow)
        return "Low volunteer availability (due to precipitation)"
    elif temp >= 70:  # 70°F and above
        return "High volunteer availability"
    elif 50 <= temp < 70:
        return "Medium volunteer availability"
    else:
        return "Low volunteer availability"

# Update the weather data on the GUI and make AI predictions
def update_weather():
    weather_data = get_weather_data(CITY, API_KEY)
    if weather_data and 'main' in weather_data:
        # Extract relevant data
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']

        # Get precipitation data (if available)
        precipitation = weather_data.get('rain', {}).get('1h', 0)  # Rain volume for the last 1 hour in mm
        if precipitation == 0:
            precipitation = weather_data.get('snow', {}).get('1h', 0)  # Snow volume for the last 1 hour in mm
        
        # Make AI prediction based on temperature and precipitation
        availability_prediction = predict_volunteer_availability(temp, description, precipitation)

        # Update the labels with fetched data
        temp_label.config(text=f"Temperature: {temp} °F")
        humidity_label.config(text=f"Humidity: {humidity} %")
        desc_label.config(text=f"Weather: {description}")
        precip_label.config(text=f"Precipitation: {precipitation} mm")
        last_update_label.config(text=f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        prediction_label.config(text=f"Volunteer Availability: {availability_prediction}")
    else:
        temp_label.config(text="Error fetching weather data")

    # Run again after 60 seconds
    root.after(60000, update_weather)

# Cincinnati and API key
CITY = "Cincinnati"
API_KEY = "bd7f96bc0c1c57950270daa8c1d2682a"  

# GUI
root = tk.Tk()
root.title("Live Weather Updates & Volunteer Prediction")

# Set window size
root.geometry("400x350")
root.config(bg="#f0f0f0")

# Labels with styles
temp_label = tk.Label(root, font=('Arial', 18), fg="#333", bg="#f0f0f0")
temp_label.pack(pady=10)

humidity_label = tk.Label(root, font=('Arial', 18), fg="#333", bg="#f0f0f0")
humidity_label.pack(pady=10)

desc_label = tk.Label(root, font=('Arial', 18), fg="#333", bg="#f0f0f0")
desc_label.pack(pady=10)

precip_label = tk.Label(root, font=('Arial', 18), fg="#333", bg="#f0f0f0")
precip_label.pack(pady=10)

last_update_label = tk.Label(root, font=('Arial', 12, 'italic'), fg="#555", bg="#f0f0f0")
last_update_label.pack(pady=10)

prediction_label = tk.Label(root, font=('Arial', 18, 'bold'), fg="#007BFF", bg="#f0f0f0")
prediction_label.pack(pady=20)

# The weather update loop
update_weather()

# GUI main loop
root.mainloop()
