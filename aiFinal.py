import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

# Load your data
file_path = "/Users/rufarotafamombe/Desktop/Projects/RatioPredict.xlsx"
df = pd.read_excel(file_path)

# Convert 'rescue_date' to datetime format and extract day of the week
df['rescue_date'] = pd.to_datetime(df['rescue_date'])
df['day_of_week'] = df['rescue_date'].dt.day_name()

# Group data by date and rescue_state to calculate daily counts
daily_counts = df.groupby(['rescue_date', 'rescue_state']).size().unstack(fill_value=0)
daily_counts = daily_counts.reindex(columns=['Completed', 'Canceled'], fill_value=0)

# Calculate daily required pickups and completion ratio
daily_counts['daily_required_pickups'] = daily_counts['Completed'] + daily_counts['Canceled']
daily_counts['completion_ratio'] = daily_counts['Completed'] / (daily_counts['Completed'] + daily_counts['Canceled'])

# Fill NaN values in 'completion_ratio' with 0, if there were no required pickups
daily_counts['completion_ratio'].fillna(0, inplace=True)

# Merge day of week back into daily_counts
daily_counts = daily_counts.merge(df[['rescue_date', 'day_of_week']].drop_duplicates(), on='rescue_date')

# Use one-hot encoding for the day of the week
daily_counts = pd.get_dummies(daily_counts, columns=['day_of_week'])

# Define features and target
X = daily_counts[['daily_required_pickups'] + [col for col in daily_counts.columns if 'day_of_week' in col]]
y = daily_counts['completion_ratio']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data for normalization
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define and train the model
model = RandomForestRegressor(random_state=42)
model.fit(X_train_scaled, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test_scaled)

# Evaluate model performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Display results in a user-friendly format
print("=== Model Evaluation Results ===")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"R-squared Score (R²): {r2:.4f}")
print("\\nThe MSE gives the average squared error, where lower values indicate better accuracy.")
print("The R-squared score shows how well the model explains the variance in the data. Values closer to 1 mean a better fit.\\n")

# Predict for today's date or any specified date
prediction_date = datetime.now()  # Use the current date and time
day_of_week = prediction_date.strftime('%A')  # Get the day of the week name

# Prepare the new data point
new_data = {'daily_required_pickups': [105]}  # Example number for required pickups
for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
    new_data[f'day_of_week_{day}'] = [1 if day == day_of_week else 0]

# Convert new_data to DataFrame and ensure it has the same columns as X_train
new_data_df = pd.DataFrame(new_data)

# Align new_data_df with X_train columns to ensure consistent ordering
new_data_df = new_data_df.reindex(columns=X_train.columns, fill_value=0)

# Scale the aligned new data
new_data_scaled = scaler.transform(new_data_df)
predicted_ratio = model.predict(new_data_scaled)

print("=== Prediction for New Data ===")
print(f"For {day_of_week}, {prediction_date.strftime('%B %d, %Y')}, with 105 required pickups, the predicted completion ratio is:")
print(f"{predicted_ratio[0]:.2f} (out of 1.0)")

print("\\nThis ratio represents the model's estimate of the likelihood that pickups will be completed for this day.")

# Adding volunteer prediction based on provided statistics
volunteer_stats = {
    "Monday": (77, 82),
    "Tuesday": (72, 81),
    "Wednesday": (64, 73),
    "Thursday": (68, 77),
    "Friday": (92, 101),
    "Saturday": (9, 17),
    "Sunday": (1, 4)
}

# Predict volunteer availability for the specified day
predicted_volunteers = volunteer_stats.get(day_of_week, (0, 0))  # Default to (0, 0) if day not found
print("=== Volunteer Availability Prediction ===")
print(f"For {day_of_week}, {prediction_date.strftime('%B %d, %Y')}, the predicted volunteer range is:")
print(f"{predicted_volunteers[0]} to {predicted_volunteers[1]} volunteers")
print("\\nThis range is based on historical data provided in the PDF.")

