from sense_hat import SenseHat
from time import sleep
import requests
import os

sense = SenseHat()

'''
This script runs on a Raspberry Pi with a SenseHat installed.
'''

def get_data(ticker):
        
    base_url = 'https://query1.finance.yahoo.com/v8/finance/chart/'
        
    response = requests.get(base_url + ticker)
        
    if "Will be right back" in response.text:
        # raise RuntimeError("Yahoo Finance is currently down.")
        daychangeperc = 0
        scroll_c      = warning_c
        scroll        = "Yahoo Finance is currently down."
        
    elif "No data found" in response.text:
        # raise RuntimeError("No data found, check ticker!")
        daychangeperc = 0
        scroll_c      = warning_c
        scroll        = "No data found, check ticker!"
        
    else:
        prices        = response.json()
        prices        = prices.get('chart').get('result')[0].get('meta') 
            
        symbol        = prices.get('symbol')
        current       = prices.get('regularMarketPrice')
        previous      = prices.get('previousClose')
        daychangeperc = round(100 * (current - previous) / previous, 4)
        scroll_c      = up_c if daychangeperc > 0 else down_c
            
        daychangeperc = daychangeperc
        scroll_c      = scroll_c
        scroll        = symbol + ' ' + str(current) + ' '
            
    return daychangeperc, scroll_c, scroll
    
    
'''Define variables'''

nmax        = 10 # how many downloads to make in total?

ntime       = 30 # time in seconds between each download

use_ticker  = 'msft' # what equity would you like to display?


'''Set up SenseHat display colours (R, G, B)'''

down_c      = (255,0,0)
up_c        = (0,255,0)
countdown_c = (0,0,255)
warning_c   = (180,95,180)
bg_c        = (0,0,0)



try:
    '''Connect RPi to Pico via USB'''
    
    pico_path = '/dev/ttyACM0'
    
    if os.path.exists(pico_path):
        import serial
        ser = serial.Serial(pico_path, 115200)
        sleep(1)
        
        '''Main loop'''
        n = 0

        while n < nmax:
            for i in range(63,-1,-1):
                if i == 63:
                    
                    '''Download and show data'''
                    dcp, s1_c, s1 = get_data(use_ticker)
                    
                    '''Send Daily Change Percentage to Pico'''
                    command = str(dcp) + "\n"
                    print('Command sent: ' + command)
                    ser.write(bytes(command.encode('ascii')))
                    
                    '''Display current price on SenseHat'''
                    sense.show_message(s1, text_colour = s1_c)
                    
               
                '''Countdown to next download event'''
                art = [countdown_c if p <= i else bg_c for p in range(64)]
                sense.set_pixels(art)
                sleep( ntime/64 )
                   
            n += 1
                  
        else:
            sense.clear()
            
    else:
        sense.show_message('Connect Pico ' * 2, text_colour = warning_c, scroll_speed = 0.05)
        sense.clear()

except KeyboardInterrupt:
    sense.set_rotation(0) # without this the text is rotated 270 degrees (?!)
    sense.show_message('Bye!', text_colour = warning_c, scroll_speed = 0.05)
    sense.clear()
