import tkinter as tk
from serpapi import GoogleSearch
from geopy.distance import geodesic

class EventsFrame(tk.Frame):
    # coordinates of Last Mile
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
        
        # Display the events details when button clicked
        self.events_label = tk.Label(
            self, text="", justify="left", anchor="nw", font=("Times New Roman", 10)
        )
        self.events_label.pack(fill="both", padx=10, pady=10)
        
        # Displays events when button clicked
        fetch_button = tk.Button(
            self, text="Get Events", command=self.display_events
        )
        fetch_button.pack(pady=10)
        
    def apiCall(self):
        params = {
            "api_key": "586a053c502c92937cf5f8f5d0fefa0429293bb2fed4686eece16d476774eabd",
            "engine": "google_events",
            "q": "Upcoming Major sporting events in Cincinnati, Ohio From November",
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
        self.events_label.config(text="")
        events_data = self.apiCall()
        
        if not events_data:
            self.events_label.config(text="No events found")
            return
        
        events_list = []
        for event in events_data:
            title = event.get('title', 'No title')
            date = event.get('date', 'No date found')
            impact, venue = self.assess_event_impact(event)
            event_details = (
                f"Title: {title}\n"
                f"Date: {date}\n"
                f"Venue: {venue}\n"
                f"Predicted Traffic Impact: {impact}\n"
                + ("-" * 40) + "\n"
            )
            events_list.append(event_details)
        
        if events_list:
            self.events_label.config(text=''.join(events_list))
        else:
            self.events_label.config(text="No events found.")   
        
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




