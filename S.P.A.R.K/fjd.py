import serial, time

arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

while True:
    if arduino.in_waiting > 0:
        linea = arduino.readline().decode(errors="ignore").strip()
        print("Distancia:", linea)
