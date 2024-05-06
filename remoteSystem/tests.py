from django.test import TestCase
import qrcode
import requests
# Create your tests here
import secrets
import time

def createQR():
    url = "http://127.0.0.1:8000/register_system/"

    qr = qrcode.QRCode(
        version=1,
        error_correction = qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    system_data_register ={
        "token": token
    }

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black",back_color="white")

    img.save("qrcode_test.png")
    
    
    
    
def read_token_from_file():
    try:
        # Open the file in read mode
        with open('token.txt', 'r') as file:
            # Read all lines from the file and join them into a single string
            token_data = ''.join(file.readlines())

            # Remove any leading or trailing whitespace characters
            token_data = token_data.strip()

            if token_data:
                # If there is data inside the file, return the token
                return token_data
            else:
                # If the file is empty, return None
                return None
    except FileNotFoundError:
        # If the file does not exist, return None
        return None

# Test the function
token = read_token_from_file()

if token is not None:
    print("Token:", token)
    system_data = {"token":token}
    response = requests.post('http://localhost:8000/system/auth_system/',json=system_data)
    response = response.json()
    if response['success']:
        print("authenticated")
else:
    # Generate a random token with a specified length (e.g., 32 characters)
    token_length = 32
    token = secrets.token_hex(token_length)
    system_data = {'token': token}
    response = requests.post('http://localhost:8000/system/register/',json=system_data)
    print(response.json())
    if response.json()['success']:
        with open('token.txt','w') as f:
            f.write(token)
        createQR()
        
    
    
    

import serial

def read_serial_data(serial_port):
    # Open serial port
    ser = serial.Serial(serial_port, baudrate=9600, timeout=1)
    
#  serial port until ';' delimiter is encountered
    try:
        while True:
            # Read data from serial port until newline character is encountered
            data = ser.readline().decode('utf-8').strip()
            
            data = data.split(';')
            if len(data)>2:
                soil_moisture = data[0]
                temperature = data[1]
                distance_water_level = data[2]
            else:
                continue    
            # Process received line
            print("Received:", data)
            response = requests.post("http://127.0.0.1:8000/system/checktokenRaspi/")
            if response.status_code == 200:
                response = response.json()
                print(response)
                if response['token_system'] == token: 
                    instantData = {
                        'soil_moisture':soil_moisture,
                        'temperature':temperature,
                        'distance_water_level':distance_water_level,
                        'token_system':token
                    }              
                    requests.post("http://127.0.0.1:8000/system/sendData/",data=instantData)
                else:
                    print("No Flag")
                    time.sleep(2)
            
    except KeyboardInterrupt:
        # Close serial port on KeyboardInterrupt
        ser.close()

read_serial_data('COM5')

# if __name__ == "__main__":
#     # Replace 'COM3' with the actual serial port on your system
#     serial_port = 'COM5'
#     read_serial_data(serial_port)


