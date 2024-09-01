import re
from datetime import datetime


# Define a function to extract timestamps from the log file
def extract_timestamps(log_file):
    timestamps = []
    timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'

    with open(log_file, 'r') as file:
        for line in file:
            match = re.search(timestamp_pattern, line)
            if match:
                timestamps.append(match.group())

    return timestamps


# Define a function to calculate the time difference
def calculate_time_difference(timestamp1, timestamp2):
    format = "%Y-%m-%d %H:%M:%S"
    datetime1 = datetime.strptime(timestamp1, format)
    datetime2 = datetime.strptime(timestamp2, format)
    time_difference = datetime2 - datetime1
    return time_difference


# Specify the log file path
log_file = 'your_log_file.log'

# Extract timestamps
timestamps = extract_timestamps(log_file)

# Check if there are at least two timestamps in the log file
if len(timestamps) >= 2:
    # Subtract the timestamps
    time_difference = calculate_time_difference(timestamps[0], timestamps[1])
    print(f'Time difference between timestamps: {time_difference}')
else:
    print('Not enough timestamps found in the log file.')
