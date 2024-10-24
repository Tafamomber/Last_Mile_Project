import tkinter as tk
import http.client
import json

api_key = 'vIWAkgxeRxGm3GsoHEdyv95p4Tf1qkc5'
origin = '39.1517,-84.4675'

def get_traffic_info(origin, destination):
    conn = http.client.HTTPSConnection("api.tomtom.com")
    url = f"/routing/1/calculateRoute/{origin}:{destination}/json?key={api_key}&routeType=fastest"
    conn.request("GET", url)
    response = conn.getresponse()
    
    if response.status == 200:
        data = response.read()
        return json.loads(data)
    else:
        return None

def get_traffic():
    destination = entry.get().strip()  # Get the destination from the input field
    traffic_info = get_traffic_info(origin, destination)
    
    if traffic_info:
        result = "Current Traffic Information for Cincinnati:\n"
        for route in traffic_info.get('routes', []):
            summary = route.get('summary', {})
            travel_time = summary.get('travelTimeInSeconds', 0)
            traffic_delay = summary.get('trafficDelayInSeconds', 0)
            
            if traffic_delay > 0:
                result += f"Traffic is moving slow. Travel time: {travel_time // 60} minutes, Delay: {traffic_delay // 60} minutes.\n"
            else:
                result += f"Traffic is moving fast. Travel time: {travel_time // 60} minutes, No delay.\n"
        
        result_label.config(text=result)  # Update the label with the result
    else:
        result_label.config(text="Error: Failed to retrieve traffic information.")

root = tk.Tk()
root.title("Traffic Information")

label = tk.Label(root, text="Enter the destination coordinates (e.g., 39.2022,-84.3772):")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

button = tk.Button(root, text="Get Traffic Info", command=get_traffic)
button.pack(pady=20)

# Label to display the result
result_label = tk.Label(root, text="", justify="left", anchor="w")
result_label.pack(pady=10)

root.mainloop()