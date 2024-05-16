import serial
import time
import json

# Example JSON data with string value for 'success'
json_data = {
    'water_pump': 'true',
    'water_plant': 'true',
    'lamp': 'true',
    'ac': 'true',
    'heater': 'true'
             }

# Convert JSON data to string
json_string = json.dumps(json_data)

# Configure serial port
serial_port = 'COM5'  # Change this to match your Arduino's serial port
baud_rate = 9600

# Initialize serial connection
ser = serial.Serial(serial_port, baud_rate)
time.sleep(2)  # Allow time for Arduino to initialize

try:
    # Send JSON data over serial
    ser.write(json_string.encode('utf-8'))
    
    # print("JSON data sent:", json_string)
    # print(data) 
finally:
    # Close serial connection
    ser.close()
