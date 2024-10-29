
import tkinter as tk
from serpapi import GoogleSearch
from geopy.distance import geodesic

lastMile_coords = (39.151780, -84.467130)

def apiCall():
    params = {
        "api_key": "586a053c502c92937cf5f8f5d0fefa0429293bb2fed4686eece16d476774eabd",
        "engine": "google_events",
        "q": "events around Norwood, Ohio in the next week",
        "hl": "en",
        "gl": "us"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    print("API Results: ", results)
    return results.get('events_results', [])
def assessEventImpact(event):
    large_event_keywords = ["concert", "festival", "parade", "sports"]
    peak_times = ["17:00", "18:00", "19:00", "12:00", "13:00"]
    impact = "Low"
    title = event.get('title', '').lower()
    date_info = event.get('date', {})
    start_time = date_info.get('start_time', '').lower() if isinstance(date_info, dict) else ''
    venue_info = event.get('venue', {})

    latitude = venue_info.get('latitude')
    longitude = venue_info.get('longitude')

    for keyword in large_event_keywords:
        if keyword in title:
            impact = "High"
            break
    if any(peak_time in start_time for peak_time in peak_times):
        impact = "High"

    if latitude and longitude:
        event_coords = (latitude, longitude)
        distance = geodesic(lastMile_coords, event_coords).km
        if distance < 5:
            impact = "High"
        elif distance < 10 and impact != "High":
            impact = "moderate"
    return impact, venue_info.get('name', 'venue not found')

def displayEvents(label):

    label.config(text="")
    events_data = apiCall()  
    if not events_data:
        label.config(text="No events")
        return
    events_list = []
    for event in events_data:
        title = event.get('title', 'No title')
        date = event.get('date', 'No date found')
        impact, venue = assessEventImpact(event)


        event_details = (
            f"Title: {title}\n"
            f"Date: {date}\n"
            f"Venue: {venue}\n"
            f"Predicted Traffic Impact: {impact}\n"
            + ("-" * 40) + "\n"
        )
        events_list.append(event_details)
    if events_list:
        label.config(text=''.join(events_list)) 
    else:
        label.config(text="No events found.")    
        
if __name__ == "__main__":
    events = tk.Tk()
    events.title("EventAPI GUI")
    
    title_label = tk.Label(events, text="Upcoming Events that May Affect Traffic", font=("Times New Roman", 32, "bold"), background="Light Slate Gray", foreground="white", pady=20)
    title_label.pack()

    width = events.winfo_screenwidth()
    height = events.winfo_screenheight()
    events.geometry(f"{width}x{height}")
    events.configure(background= "Light Slate Gray")

    events_label = tk.Label(events, text="", background="Light Slate Gray", foreground='white', justify="left", anchor="nw", font=("Times New Roman", 10))
    events_label.pack(fill="both", padx=20, pady=20)
    
    fetch_button = tk.Button(events, text="Click for Events", command=lambda: displayEvents(events_label), background="white", foreground="Light Slate Gray")
    fetch_button.pack(pady=20)

    events.mainloop()

