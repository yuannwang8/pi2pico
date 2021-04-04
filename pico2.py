import machine
from utime import sleep
from math import floor

import select
import sys

servo = machine.PWM(machine.Pin(28))
servo.freq(50)

led_pwm = machine.PWM(machine.Pin(25))
led_pwm.freq(1000)

'''
Define variables

Here we set up the callibration needed for the servo motor to become a useful meter.

For example, we wish to show a 0% change at the 90 degree ('up') point,
a maximum of 1% change by rotating clockwise by 90 degrees,
a minimum of a -1% change by rotating anticlockwise by 90 degrees.

We need to define the percentage change range to be shown, a useful (or rather usable)
servo angle range, and the associated duty cycle value for the servo.

Here, symmetrical percentage and degree ranges are used for simplicity.
Please update the functions if non-symmertrical ranges are chosen.

A 180-degree toy servo motor is used. This servo rotates anticlockwise.
For reference, the servo pointer is parallel to the motor's
long edge at 180 degrees and 'up' at 90 degrees. Unfortunately this servo motor
is unable to produce a 0-to-90-to-180 angle sweep reliably so we settled
for a smaller range.

'''

# percentage change to be shown
low_perc = -0.5 
high_perc = 0.5 

# servo duty
min_duty = 2200 
max_duty = 7000 

# servo's angles of deflection
min_degree = 30 
max_degree = 150



def bound_minmax(v, min_v, max_v):
    '''return a value v that is bound by min_v and max_v'''
    return min(max(v, min_v), max_v)


def perc_to_deg(perc):
    # incremental degree per perc
    degree_step = (max_degree - min_degree) / (low_perc - high_perc)
    
    # bound perc within selected range
    perc = bound_minmax(v = perc, min_v = low_perc, max_v = high_perc)
    
    # get degree for perc: note the zero point at 90 degrees
    degree = floor(degree_step * perc + 90)
        
    return degree


def deg_to_duty(degree):
    # increment duty per degree
    duty_step = (max_duty - min_duty) / (max_degree - min_degree)
    
    # bound degree within stable range
    degree = bound_minmax(v = degree, min_v = min_degree, max_v = max_degree)
        
    # get duty value for degree
    duty = floor(duty_step * (degree - min_degree) + min_duty)
    
    # bound duty within stable range
    duty = bound_minmax(v = duty, min_v = min_duty, max_v = max_duty)
        
    return duty

try:
    
    if True:
        '''Start-up eyeball calibration sequence'''
        servo.duty_u16(0)
        sleep(0.1)

        servo.duty_u16(1700)
        sleep(1)

        servo.duty_u16(4500)
        sleep(1)

        servo.duty_u16(8100)
        sleep(1)

        servo.duty_u16(deg_to_duty(45))
        sleep(1)

        servo.duty_u16(deg_to_duty(135))
        sleep(1)

        servo.duty_u16(deg_to_duty(90))
        sleep(1)

        servo.duty_u16(0)
        sleep(0.1)
    
    
    while True:
         
        if select.select([sys.stdin], [], [], 0)[0]:
            msg = float(sys.stdin.readline())
            msg_deg = perc_to_deg(msg)
            print(str(msg) + ' ' + str(msg_deg))
            
            led_pwm.duty_u16(0)
            
            '''Move servo pointer. Reset to angle zero for better visual impact'''
            servo.duty_u16(deg_to_duty(perc_to_deg(0)))
            sleep(0.5)
            servo.duty_u16(deg_to_duty(msg_deg))
            sleep(0.1)
            servo.duty_u16(0)
            sleep(0.1)
        
        else:
            
            '''Pulse onboard LED while we wait'''  
            for duty_led in range(65025):
                led_pwm.duty_u16(duty_led)
                sleep(0.0001)
            for duty_led in range(65025,0,-1):
                led_pwm.duty_u16(duty_led)
                sleep(0.0001)    
                
except KeyboardInterrupt:
    '''Return pointer to storage position'''
    led_pwm.duty_u16(0)
    servo.duty_u16(8100)
    sleep(0.5)
    servo.duty_u16(0)
    sleep(0.1)


    

