import pandas as pd

# Load the CSV file
df = pd.read_csv("C:/Users/toghi/OneDrive/Desktop/Condensed Last Mile Excel.csv")

# Convert the 'Rescue Date' column to datetime for easier filtering and manipulation
df["rescue_date"] = pd.to_datetime(df["rescue_date"])

# Filter data to only include dates in the range from January 1, 2023, to September 8, 2024
start_date = "2023-01-01"
end_date = "2024-09-08"
df = df[(df["rescue_date"] >= start_date) & (df["rescue_date"] <= end_date)]

# Group by date and calculate completed and total counts
daily_counts = df.groupby("rescue_date")["rescue_state"].value_counts().unstack(fill_value=0)
daily_counts["Total Rescues"] = daily_counts["Completed"] + daily_counts["Canceled"] + daily_counts["In progress"]

all_dates = pd.date_range(start=start_date, end=end_date)
daily_counts = daily_counts.reindex(all_dates, fill_value=0)

# Calculate the completion rate as Completed / (Completed + Canceled)
daily_counts["Completion Rate"] = daily_counts["Completed"] / daily_counts["Total Rescues"]

#Rename first column Rescue Date
daily_counts.columns.name = "Rescue Date"  

# Set the option to display all rows
pd.set_option("display.max_rows", None)

# Display the resulting DataFrame
print(daily_counts[["Completed", "Canceled", "Total Rescues", "Completion Rate"]])
