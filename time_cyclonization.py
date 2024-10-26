import csv
import time
from datetime import datetime, timedelta
import random

# Specify the CSV file names
csv_filename_gps = 'utc_time_dummy_gps_time_pairs.csv'
csv_filename_imu = 'utc_time_random_numbers_pairs.csv'

# Specify the number of seconds to record pairs of UTC times
num_seconds = 10

def write_on_csv(which_file, writerow_title, row_list):
    # Open the file in append mode
    with open(which_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write the header row only if the file is empty
        if file.tell() == 0:
            writer.writerow(['UTC Time', writerow_title])
        # Write the data row
        writer.writerow(row_list)

# Generate data and write rows in pairs
for _ in range(num_seconds):
    # Capture the first UTC and GPS times
    utc_time_1 = datetime.utcnow()
    gps_time_1 = utc_time_1 + timedelta(seconds=18)
    random_number_1 = random.randint(1, 100)

    # Write the first pair of rows to the CSV files
    write_on_csv(csv_filename_gps, 'Dummy GPS Time', [utc_time_1.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], gps_time_1.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]])
    write_on_csv(csv_filename_imu, 'Random Number', [utc_time_1.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], random_number_1])

    # Wait for a small amount of time to ensure a different UTC time for the second reading
    time.sleep(0.5)  # 500 milliseconds

    # Capture the second UTC and GPS times
    utc_time_2 = datetime.utcnow()
    gps_time_2 = utc_time_2 + timedelta(seconds=18)
    random_number_2 = random.randint(1, 100)

    # Write the second pair of rows to the CSV files
    write_on_csv(csv_filename_gps, 'Dummy GPS Time', [utc_time_2.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], gps_time_2.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]])
    write_on_csv(csv_filename_imu, 'Random Number', [utc_time_2.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], random_number_2])

print(f"{csv_filename_gps}, {csv_filename_imu} created with {num_seconds * 2} rows of UTC, GPS times and dummy IMU data.")
