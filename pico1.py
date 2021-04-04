'''
Serial connection between Pi and Pico via USB.

pi.py generates a stream of 1 to 4 that are fed to the Pico
via the serial port at a rate of 1 signal every 2 seconds.

pico.py (this file) enables the Pico's onboard LED to blink the
received number.

Save this file as main.py on the Pico to have the Pico run this
automatically once plugged into a Pi (or a Mac).

Each blink takes 0.4 seconds.

'''

import select
import sys
import machine
import utime

led = machine.Pin(25, machine.Pin.OUT)

p = 0

while p < 50:
    if select.select([sys.stdin], [], [], 0)[0]:
        blinkn = int(sys.stdin.readline())
        for n in range(1, blinkn + 1):
            led.value(1)
            utime.sleep(0.2)
            led.value(0)
            utime.sleep(0.2)
        p += 1
        utime.sleep(2 - 0.4 * blinkn)

    else:
        # print('waiting...')
        utime.sleep(0.2)

else:
    led.value(0)
