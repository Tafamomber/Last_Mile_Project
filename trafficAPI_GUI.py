import http.client
import json
import tkinter as tk

# API Key for TomTom
api_key = 'vIWAkgxeRxGm3GsoHEdyv95p4Tf1qkc5'

# List of major highways with coordinates (latitude, longitude) and speed limits
highways = {
    # Interstates
    'I-71': {'north': {'coords': '39.1072,-84.5045'}, 'south': {'coords': '39.1000,-84.5100'}},
    'I-74': {'east': {'coords': '39.1310,-84.5477'}, 'west': {'coords': '39.1200,-84.5500'}},
    'I-75': {'north': {'coords': '39.0736,-84.5323'}, 'south': {'coords': '39.0600,-84.5400'}},
    'I-275': {'east': {'coords': '39.0663,-84.3748'}, 'west': {'coords': '39.0600,-84.3800'}},

    # US Highways
    'US-50': {'east': {'coords': '39.0920,-84.5200'}, 'west': {'coords': '39.0800,-84.5300'}},
    'US-27': {'north': {'coords': '39.1300,-84.5200'}, 'south': {'coords': '39.1200,-84.5300'}},
    'US-52': {'east': {'coords': '38.9770,-84.2868'}, 'west': {'coords': '38.9720,-84.3000'}},

    # Ohio State Routes
    'OH-126': {'east': {'coords': '39.2290,-84.3950'}, 'west': {'coords': '39.2200,-84.4000'}},
    'OH-32': {'east': {'coords': '39.1327,-84.2861'}, 'west': {'coords': '39.1200,-84.3000'}},
    'OH-4': {'north': {'coords': '39.3743,-84.4585'}, 'south': {'coords': '39.3600,-84.4600'}},

    # Kentucky State Routes
    'KY-8': {'east': {'coords': '39.0920,-84.4950'}, 'west': {'coords': '39.0800,-84.5000'}},
    'KY-18': {'north': {'coords': '39.0462,-84.6632'}, 'south': {'coords': '39.0400,-84.6700'}},
    'KY-237': {'north': {'coords': '39.0481,-84.6700'}, 'south': {'coords': '39.0400,-84.6750'}},
}

class TrafficFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.results_text = tk.Text(self, width=60, height=20, wrap='word', font=("Helvetica", 10))
        self.results_text.tag_configure("highway", font=("Helvetica", 12, "bold"))
        self.results_text.tag_configure("delay", foreground="red", font=("Helvetica", 10, "bold"))
        self.results_text.tag_configure("normal", foreground="green", font=("Helvetica", 10, "bold"))
        self.results_text.tag_configure("error", foreground="orange", font=("Helvetica", 10, "italic"))
        self.results_text.pack(pady=10)
        
        # Refresh button
        refresh_button = tk.Button(self, text="Refresh Traffic Info", command=self.refresh_traffic_info)
        refresh_button.pack(pady=5)

        # Initial load of traffic information
        self.refresh_traffic_info()

    def get_traffic_flow(self, coords):
        conn = http.client.HTTPSConnection("api.tomtom.com")
        url = f"/traffic/services/4/flowSegmentData/absolute/10/json?key={api_key}&point={coords}"
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            return json.loads(data)
        else:
            return None

    def calculate_delay(self, free_flow_speed, current_speed):
        if current_speed > 0 and current_speed < free_flow_speed:
            # Calculate time for 1 mile
            time_at_free_flow_speed = 1 / free_flow_speed * 60  # minutes
            time_at_current_speed = 1 / current_speed * 60  # minutes
            delay = time_at_current_speed - time_at_free_flow_speed
            return max(0, round(delay, 2))  # Ensure delay is not negative
        return 0  # No delay if speeds are equal or if current_speed is 0

    def refresh_traffic_info(self):
        self.results_text.delete(1.0, tk.END)  # Clear previous results
        self.results_text.insert(tk.END, "Traffic Information for Major Highways:\n\n")
        
        for highway, directions in highways.items():
            self.results_text.insert(tk.END, f"Highway: {highway}\n", "highway")
            
            for direction, info in directions.items():
                coords = info['coords']
                traffic_flow = self.get_traffic_flow(coords)
                
                if traffic_flow:
                    flow_data = traffic_flow.get("flowSegmentData", {})
                    current_speed = flow_data.get("currentSpeed", 0)
                    free_flow_speed = flow_data.get("freeFlowSpeed", 0)
                    
                    # Calculate delay
                    delay = self.calculate_delay(free_flow_speed, current_speed)
                    
                    # Determine status
                    if current_speed < free_flow_speed:
                        status = "Delay Detected"
                        status_tag = "delay"
                    else:
                        status = "Traffic Flowing Normally"
                        status_tag = "normal"

                    # Display the information
                    self.results_text.insert(tk.END, f"  {direction.capitalize()}bound:\n")
                    self.results_text.insert(tk.END, f"    Free Flow Speed: {free_flow_speed} mph\n")
                    self.results_text.insert(tk.END, f"    Current Speed: {current_speed} mph\n")
                    if delay > 0:
                        self.results_text.insert(tk.END, f"    Predicted Delay: {delay} minutes per mile\n")
                    self.results_text.insert(tk.END, f"    Status: {status}\n", status_tag)
                else:
                    self.results_text.insert(tk.END, f"  {direction.capitalize()}bound:\n")
                    self.results_text.insert(tk.END, "    Status: Failed to retrieve traffic flow information\n", "error")
            self.results_text.insert(tk.END, "-" * 40 + "\n")

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Traffic Information")
    traffic_frame = TrafficFrame(root)
    traffic_frame.pack(pady=20, padx=20)
    root.mainloop()
