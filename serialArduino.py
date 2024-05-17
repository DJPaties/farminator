from django.test import TestCase
import json
import qrcode
import requests
# Create your tests here
import secrets
import time

token = "bd7c795f8090e3812d9ecf4964639cecb27d7e34f39903b8d5be6a50527fc4b6"
    
    


data = [700,25,76]
def read_serial_data(serial_port):
    # Open serial port
    # ser = serial.Serial(serial_port, baudrate=9600, timeout=1)
    #
#  serial port until ';' delimiter is encountered
    try:
        while True:
            # Read data from serial port until newline character is encountered
            # data = ser.readline().decode('utf-8').strip()
            
            # data = data.split(';')
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
                response_json = response.json()
                # response_key = list(response_json.keys())[0]
                # response_data = json.loads(response_key)
                response_str = response_json[0]
                response = json.loads(response_str)
                print(response)
                
                if response['token_system'] == token: 
                    if response['control_flag']:
                        control_list = response['control_list']
                        print(control_list)
                    else:
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
        exit()
        # ser.close()

read_serial_data('COM5')