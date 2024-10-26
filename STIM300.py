# IMU

import serial
import numpy as np
import datetime as dt
import os

# Configuration settings
BAUDRATE = 921600
READ_LENGTH = 39
DATAGRAM_IDENTIFIER = b'\x93'
LOG_FOLDER = os.getcwd()  # Use the current working directory


def setup_serial_connection(port='COM6', baudrate=BAUDRATE):
    """Setup and return the serial connection."""
    return serial.Serial(port=port, baudrate=baudrate)


def wait_for_datagram(serial_port):
    """Wait for the start of a new datagram."""
    while True:
        if serial_port.read(1) == DATAGRAM_IDENTIFIER:
            break
    return DATAGRAM_IDENTIFIER + serial_port.read(READ_LENGTH)


def decode_sensor_data(segment, divisor):
    """Decode a 3x3 byte segment into a floating-point array."""
    segment = (segment[0:3] + b'\x00' +
               segment[3:6] + b'\x00' +
               segment[6:9] + b'\x00')
    data = np.frombuffer(segment, dtype='>i').astype(np.float32)
    return data / (2 ** (divisor + 8))


def decode_latency(data):
    """Decode the latency from the datagram."""
    return np.frombuffer(data[32:34], dtype='>u2').astype(int)


def decode_gyro_accel_latency(data):
    """Decode the gyro, accelerometer, and latency data from the datagram."""
#    gyro = decode_sensor_data(data[1:10], 14)
#    accel = decode_sensor_data(data[11:20], 19)
    gyro = [round(value, 3) for value in decode_sensor_data(data[1:10], 14)]
    accel = [round(value, 3) for value in decode_sensor_data(data[11:20], 19)]
    latency = decode_latency(data)
    cntr = ord(data[31:32])  # Counter value from the datagram
    return gyro, accel, latency, cntr


def save_sensor_data(gyro, accel, latency, cntr, folder_path):
    """Save the decoded gyro, accelerometer data, latency, and counter value to a file."""
    # Ensure the log folder exists (using the current directory)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Define the file name with the current date
    file_path = os.path.join(folder_path, f"STIM300.csv")

    # Check if file exists, if not create it with headers
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a') as file:
        if not file_exists:
            file.write("Time,Gyro_X,Gyro_Y,Gyro_Z,Accel_X,Accel_Y,Accel_Z,Latency,Counter\n")

        # Format the timestamp to only show HH:MM:SS.ss
        timestamp = dt.datetime.now()
        formatted_time = timestamp.strftime('%H:%M:%S') + f'.{timestamp.microsecond // 10000:02d}'

        # Write the sensor data to the file
        file.write(
            f"{formatted_time},{gyro[0]},{gyro[1]},{gyro[2]},{accel[0]},{accel[1]},{accel[2]},{latency[0]},{cntr}\n")


def main():
    serial_port = setup_serial_connection()

    while True:
        datagram = wait_for_datagram(serial_port)
        gyro, accel, latency, cntr = decode_gyro_accel_latency(datagram)
        save_sensor_data(gyro, accel, latency, cntr, LOG_FOLDER)


if __name__ == '__main__':
    main()
