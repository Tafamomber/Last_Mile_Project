import tkinter as tk
from serpapi import GoogleSearch
from geopy.distance import geodesic

 
class EventsFrame(tk.Frame):
    # Coordinates of Last Mile
    lastMile_coords = (39.151780, -84.467130)
 
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
 
        # Title for the Events
        title_label = tk.Label(
            self, text="Events",
            font=("Times New Roman", 12, "bold"),
            pady=10
        )
        title_label.pack()
 
        # Create a scrollable Text widget for displaying events
        self.events_text = tk.Text(
            self, wrap="word", font=("Times New Roman", 10), height=20, width=80
        )
        self.events_text.tag_configure("event_title", foreground="black", font=("Times New Roman", 10, "bold"))
        self.events_text.tag_configure("event_details", foreground="black", font=("Times New Roman", 10))
        self.events_text.tag_configure("delay_high", foreground="red", font=("Times New Roman", 10))
        self.events_text.tag_configure("delay_low", foreground="green", font=("Times New Roman", 10))
        self.events_text.pack(fill="both", expand=True, padx=10, pady=10)
 
        # Refresh events button
        refresh_button = tk.Button(
            self, text="Refresh Events", command=self.display_events
        )
        refresh_button.pack(pady=10)
 
        # Automatically display events on initialization
        self.display_events()
        
    def apiCall(self):
        params = {
            "api_key": "586a053c502c92937cf5f8f5d0fefa0429293bb2fed4686eece16d476774eabd",
            "engine": "google_events",
            "q": "Major events in Cincinnati Ohio",
            "hl": "en",
            "gl": "us"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results.get('events_results', [])
    
    def assess_event_impact(self, event):
        large_event_keywords = ["concert", "festival", "parade", "sports"]
        peak_times = ["17:00", "18:00", "19:00", "12:00", "13:00"]
        impact = "Low"
        title = event.get('title', '').lower()
        start_time = event.get('date', {}).get('start_time', '').lower()
        venue_info = event.get('venue', {})
        latitude = venue_info.get('latitude')
        longitude = venue_info.get('longitude')
        
        # impact of traffic depending on timing
        for keyword in large_event_keywords:
            if keyword in title:
                impact = "High"
                break
        if any(peak_time in start_time for peak_time in peak_times):
            impact = "High"
        
        # Check distance from Last Mile
        if latitude and longitude:
            event_coords = (latitude, longitude)
            distance = geodesic(self.lastMile_coords, event_coords).km
            if distance < 5:
                impact = "High"
            elif distance < 10 and impact != "High":
                impact = "Moderate"
        return impact, venue_info.get('name', 'venue not found')
    
    def display_events(self):
        self.events_text.delete("1.0", tk.END)
        events_data = self.apiCall()
        
        if not events_data:
            self.events_text.insert(tk.END, "No events found")
            return

        for event in events_data:
            title = event.get('title', 'No title')
            date = event.get('date', {}).get('start_date', 'No date found')
            impact, venue = self.assess_event_impact(event)
            event_title = f"Title: {title}\n"
            event_details = f"Date: {date}\nVenue: {venue}\n"
 
            # Insert event title
            self.events_text.insert(tk.END, event_title, "event_title")
            # Insert event details
            self.events_text.insert(tk.END, event_details, "event_details")
 
            # Traffic impact
            if impact == "High":
                self.events_text.insert(
                    tk.END,
                    f"Predicted Traffic Impact: High\n",
                    "delay_high"
                )
            else:
                self.events_text.insert(
                    tk.END,
                    f"Predicted Traffic Impact: Low\n",
                    "delay_low"
                )
            self.events_text.insert(tk.END, "-" * 40 + "\n", "event_details")

        
if __name__ == "__main__":
    # activate GUI
    events = tk.Tk()
    # Title
    events.title("EventAPI GUI")

    # set height and width
    width = events.winfo_screenwidth()
    height = events.winfo_screenheight()
    events.geometry(f"{width}x{height}")

    #Fit event frame in dashboard
    events_frame = EventsFrame(events)
    events_frame.pack(fill="both", expand=True)

    events.mainloop()




