'''
Serial connection between Pi and Pico via USB.

pi.py (this file) generates a stream of 1 to 4 that's fed to
the Pico via the Pi's (or Mac's) serial port at a rate of 1 signal
every 2 seconds.

Run this file once the Pico is plugged into the Pi (or Mac).

pico.py enables the Pico's onboard LED to blink the received number.

Each blink takes 0.4 seconds.

'''

import time
import os

pi_pico_path = '/dev/ttyACM0'
mac_pico_path = '/dev/tty.usbmodem0000000000001'

# update as appropriate!
pico_path = pi_pico_path

serial_connected = 0

if os.path.exists(pico_path):
    import serial
    ser = serial.Serial(pico_path, 115200)
    serial_connected = 1
    time.sleep(1)

while True:
    for x in range(1, 5):
        command = str(x) + "\n"
        print('Command sent: ' + command)
        ser.write(bytes(command.encode('ascii')))
        time.sleep(2)
