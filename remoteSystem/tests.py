import qrcode
import requests
import json
import secrets
import time
import serial

base_url = "http://192.168.27.31:3000/"

conditions_loaded={}
def createQR():
    url = f"{base_url}register_system/"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    system_data_register = {"token": token}

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img.save("qrcode_test.png")

def read_token_from_file():
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

token = read_token_from_file()

if token is not None:
    print("Token:", token)
    system_data = {"token": token}
    response = requests.post(f'{base_url}system/auth_system/', json=system_data)
    response = response.json()
    if response['success']:
        print("Authenticated")
else:
    token_length = 32
    token = secrets.token_hex(token_length)
    system_data = {'token': token}
    response = requests.post(f'{base_url}system/register/', json=system_data)
    print(response.json())
    if response.json()['success']:
        with open('token.txt', 'w') as f:
            f.write(token)
        createQR()
with open("conditions.json","r") as condition_file:
    conditions_loaded = json.load(condition_file)
    print(f"JSON data\n {conditions_loaded}")
        


print("Initializing serial connection")
ser = serial.Serial('/dev/ttyACM0', baudrate=9600)
time.sleep(2)  # Allow time for Arduino to initialize

def read_serial_data(serial_port):
    try:
        global token
        global conditions_loaded
        conditions_loaded = json.loads(conditions_loaded)
        while True:
            
            
            
            ser.write(('1000000').encode())
            time.sleep(1)
            data = ser.readline().decode('utf-8').strip()
            print("Received from Arduino:", data)
            data = data.split(';')
            
            if len(data) > 2:
                soil_moisture = data[0]
                temperature = data[1]
                distance_water_level = data[2]
                light_intensity = data[3]
            #   condition function 
            message = {}
            
                if conditions_loaded['water_level'] != 'null':
                    if conditions_loaded['water_level']['rule'] == 'greater_than' and int(light_intensity) > int(conditions_loaded['water_level']['value']): 
                        message['water_level'] = "The Water Level is Greater Than " + conditions_loaded['water_level']['value']
                    if conditions_loaded['water_level']['rule'] == 'less_than' and int(light_intensity) < int(conditions_loaded['water_level']['value']): 
                        message['water_level'] = "The Water Level is Less Than " + conditions_loaded['water_level']['value']
                    if conditions_loaded['water_level']['rule'] == 'equal' and int(light_intensity) = int(conditions_loaded['water_level']['value']):
                        message['water_level'] = "The Water Level is Equal To " + conditions_loaded['water_level']['value']
                 if conditions_loaded['soil_moisture'] != 'null':
                    if conditions_loaded['soil_moisture']['rule'] == 'greater_than' and int(light_intensity) > int(conditions_loaded['soil_moisture']['value']): 
                        message['soil_moisture'] = "The Soil Moisture is Greater Than " + conditions_loaded['soil_moisture']['value']
                    if conditions_loaded['soil_moisture']['rule'] == 'less_than' and int(light_intensity) < int(conditions_loaded['soil_moisture']['value']): 
                        message['soil_moisture'] = "The Soil Moisture is Less Than " + conditions_loaded['soil_moisture']['value']
                    if conditions_loaded['soil_moisture']['rule'] == 'equal' and int(light_intensity) = int(conditions_loaded['soil_moisture']['value']):
                        message['soil_moisture'] = "The Soil Moisture is Equal To " + conditions_loaded['soil_moisture']['value']
                if conditions_loaded['temperature'] != 'null':
                    if conditions_loaded['temperature']['rule'] == 'greater_than' and int(light_intensity) > int(conditions_loaded['temperature']['value']): 
                        message['temperature'] = "The Temperature is Greater Than " + conditions_loaded['temperature']['value']
                    if conditions_loaded['temperature']['rule'] == 'less_than' and int(light_intensity) < int(conditions_loaded['temperature']['value']): 
                        message['temperature'] = "The Temperature is Less Than " + conditions_loaded['temperature']['value']
                    if conditions_loaded['temperature']['rule'] == 'equal' and int(light_intensity) = int(conditions_loaded['temperature']['value']):
                        message['temperature'] = "The Temperature is Equal To " + conditions_loaded['temperature']['value']
                if conditions_loaded['light_intensity'] != 'null':
                    if conditions_loaded['light_intensity']['rule'] == 'greater_than' and int(light_intensity) > int(conditions_loaded['light_intensity']['value']): 
                        message['light_intensity'] = "The Light Intensity is Greater Than " + conditions_loaded['light_intensity']['value']
                    if conditions_loaded['light_intensity']['rule'] == 'less_than' and int(light_intensity) < int(conditions_loaded['light_intensity']['value']): 
                        message['light_intensity'] = "The Light Intensity is Less Than " + conditions_loaded['light_intensity']['value']
                    if conditions_loaded['light_intensity']['rule'] == 'equal' and int(light_intensity) = int(conditions_loaded['light_intensity']['value']):
                        message['light_intensity'] = "The Light Intensity is Equal To " + conditions_loaded['light_intensity']['value']
                if len(message) >0:
                    requests.post(f"{base_url}farm/notifyCondition/", data={'farm_token':token,'message':message})
                    message={}
            else:
                continue
                
            response = requests.post(f"{base_url}system/checktokenRaspi/")
            if response.status_code == 200:
                response = response.json()
                response = response[0]
                response = json.loads(response)

                print(response)
                if response['token_system'] == token: 
                    if response['data_flag'] == 'true':
                
                        instantData = {
                            'soil_moisture': soil_moisture,
                            'temperature': temperature,
                            'distance_water_level': distance_water_level,
                            'light_intensity': light_intensity,
                            'token_system': token
                        }
                        requests.post(f"{base_url}system/sendData/", data=instantData)
                        

                        print("Received:", data)
                    elif response['control_flag'] == 'true':
                        control_list = response['control_list']
                        print(control_list)
                        try:
                            ser.write(control_list.encode())
                            time.sleep(2)
                            response = ser.readline().decode('utf-8').strip()
                            print("Response from Arduino:", response)
                            requests.post(f"{base_url}system/execDone/", data={'executed_flag':True})
                
                        except:
                            print("Failed to send control list to Arduino")
                        time.sleep(2)
                        
                    elif response['condition_flag'] =="true":
                        condition_list = response['condition_list']
                        print("Conditions Saving")
                        print(condition_list)
                        with open("conditions.json","w") as file:
                            json.dump(condition_list,file,indent=4)
                          
                        requests.post(f"{base_url}system/saveConditions/", data={'saved_condition_flag':True})
                    
                else:
                    print("No Flag")
                    #time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting program...")
        ser.close()

try:
    read_serial_data('/dev/ttyACM0')
except serial.serialutil.SerialException as e:
    print("Error:", e)
    print("Serial port not found. Make sure the Arduino is connected and the correct port is specified.")
