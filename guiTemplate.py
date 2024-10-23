import tkinter as tk

# main window
root = tk.Tk()
root.title("Dashboard Mockup")
root.geometry("600x400")

# Frame
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Function to handle button click events
def button_clicked(label):
    print(f"{label} button clicked")



# Row 1
prev_week_button = tk.Button(frame, text="Prev Week", command=lambda: button_clicked("Prev Week"))
prev_week_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

traffic_button = tk.Button(frame, text="Traffic", command=lambda: button_clicked("Traffic"))
traffic_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

week_date_button = tk.Button(frame, text="Week / Date", command=lambda: button_clicked("Week / Date"))
week_date_button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

# Row 2
weather_button = tk.Button(frame, text="Weather", command=lambda: button_clicked("Weather"))
weather_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", rowspan=2)

people_active_button = tk.Button(frame, text="How many people active today", command=lambda: button_clicked("People Active"))
people_active_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew", columnspan=2)

# Row 3
events_button = tk.Button(frame, text="Events", command=lambda: button_clicked("Events"))
events_button.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

report_button = tk.Button(frame, text="Leash Report", command=lambda: button_clicked("Leash Report"))
report_button.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

# Row 4
next_week_button = tk.Button(frame, text="Next Week", command=lambda: button_clicked("Next Week"))
next_week_button.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

# buttons resize 
for i in range(3):
    frame.grid_columnconfigure(i, weight=1)
for i in range(4):
    frame.grid_rowconfigure(i, weight=1)

# Tkinter event loop
root.mainloop()
