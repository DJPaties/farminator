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
            if len(data)>0:
                soil_moisture = data[0]
                temperature = data[1]
                distance_water_level = data[2]
            else:
                continue    
            # Process received line
            print("Received:", data)
            
    except KeyboardInterrupt:
        # Close serial port on KeyboardInterrupt
        ser.close()


if __name__ == "__main__":
    # Replace 'COM3' with the actual serial port on your system
    serial_port = 'COM5'
    read_serial_data(serial_port)
