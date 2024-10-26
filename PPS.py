# Receiver

import serial
import datetime as dt

# Setup serial port to read GPS data on Windows
gps_serial = serial.Serial(
    port='COM10',
    baudrate=9600
)

# Continuously read and process GPS data
while True:
    line = gps_serial.readline().decode('ascii', errors='replace').strip()
    if line.startswith('$GPRMC'):
        parts = line.split(',')
        gps_time = parts[1]  # Extract GPS time from the NMEA sentence
        utc_time = dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]  # Use dt.datetime

        # Print the computer time (UTC) and GPS time to the console
        print(f"Computer time (UTC): {utc_time}\tGPS Time: {gps_time}")