import serial
import json
import time

# Configure the serial connection
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino port

def send_json_to_arduino(json_data):
    ser.write((json_data + '\n').encode())

def receive_from_arduino():
    while ser.in_waiting == 0:
        pass  # Wait until there is data available to read
    data = ser.readline().decode().strip()
    return data

# Example usage
if __name__ == "__main__":
    try:
        # Test case 1: Request sensor data
        sensor_data_request = json.dumps({
            "data_flag": "true",
            "control_flag": "false"
        })
        send_json_to_arduino(sensor_data_request)
        print("Requesting sensor data...")
        sensor_data = receive_from_arduino()
        print("Received sensor data:", sensor_data)

        # Allow some time before the next command
        time.sleep(2)

        # Test case 2: Control the devices
        control_command = json.dumps({
            "data_flag": "false",
            "control_flag": "true",
            "water_pump": "true",
            "water_plant": "false",
            "uv": "true",
            "ac": "false",
            "heater": "true"
        })
        send_json_to_arduino(control_command)
        print("Sent control command to Arduino.")

        # Allow some time before the next command
        time.sleep(2)

        # Test case 3: Turn off all devices
        control_command_off = json.dumps({
            "data_flag": "false",
            "control_flag": "true",
            "water_pump": "false",
            "water_plant": "false",
            "uv": "false",
            "ac": "false",
            "heater": "false"
        })
        send_json_to_arduino(control_command_off)
        print("Sent command to turn off all devices.")
    except KeyboardInterrupt:
        print("Program interrupted by the user.")
    finally:
        ser.close()
