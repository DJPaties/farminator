from django.test import TestCase  # Importing necessary module 'TestCase' from Django test.
import qrcode  # Importing qrcode module for generating QR codes.
import requests  # Importing requests module for making HTTP requests.
import secrets  # Importing secrets module for generating secure tokens.
import time  # Importing time module for time-related operations.
import serial  # Importing serial module for serial communication.

def createQR(product_id):
    """
    Function to generate QR code for a given product ID.
    """
    url = product_id

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img.save("qrcode_test.png")

def read_token_from_file():
    """
    Function to read token from a file.
    """
    try:
        with open('token.txt', 'r') as file:
            token_data = ''.join(file.readlines())
            token_data = token_data.strip()

            if token_data:
                return token_data
            else:
                return None
    except FileNotFoundError:
        return None

# Test the function
token = read_token_from_file()

if token is not None:
    print("Token:", token)
    system_data = {"token": token}
    response = requests.post('http://localhost:8000/system/auth_system/', json=system_data)
    response = response.json()
    if response['success']:
        print("authenticated")
else:
    token_length = 32
    token = secrets.token_hex(token_length)
    system_data = {'token': token}
    response = requests.post('http://localhost:8000/system/register/', json=system_data)
    print(response.json())
    response = response.json()
    if response['success']:
        with open('token.txt', 'w') as f:
            f.write(token)
        createQR(response['data']['id'])

def read_serial_data(serial_port):
    """
    Function to read data from a serial port and send it to a web server.
    """
    ser = serial.Serial(serial_port, baudrate=9600, timeout=1)

    try:
        while True:
            data = ser.readline().decode('utf-8').strip()
            data = data.split(';')
            if len(data) > 2:
                soil_moisture = data[0]
                temperature = data[1]
                distance_water_level = data[2]
            else:
                continue
            print("Received:", data)
            response = requests.post("http://127.0.0.1:8000/system/checktokenRaspi/")
            if response.status_code == 200:
                response = response.json()
                print(response)
                if response['token_system'] == token:
                    instantData = {
                        'soil_moisture': soil_moisture,
                        'temperature': temperature,
                        'distance_water_level': distance_water_level,
                        'token_system': token
                    }
                    requests.post("http://127.0.0.1:8000/system/sendData/", data=instantData)
                else:
                    print("No Flag")
                    time.sleep(2)
    except KeyboardInterrupt:
        ser.close()

# Replace 'COM5' with the actual serial port on your system
read_serial_data('COM5')
