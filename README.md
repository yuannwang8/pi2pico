# Sending Input Signals to the Raspberry Pi Pico via USB

The repo holds simple examples where the Raspberry Pi Pico receives serial signals via USB, and acts upon the received signals to generate outputs.

Please remember to enable Micropython on the Pico (please see the official Pico documentation for instructions).


## Set 1: Simple LED blinker

The input signal is a number between 1 to 4. The Pico's onboard LED blinks this number of times as output.


### Steps

On the Pico: save `pico1.py` as `main.py` on the Pico itself to have the Pico run the code automatically once it is connected via USB to the Raspberry Pi.

On the Raspberry Pi: run `pi1.py`. Mac users: remember to update the USB's path in `pi1.py`. You may also need to install additional modules: see `requirements.txt`.


## Set 2: Share price percentage change meter

The input signal is a numeral representing percentage change of a chosen equity: this is sourced from Yahoo Finance. The Pico uses this signal to drive a servo motor pointer to show the percentage change mechanically.

This example also includes codes for displaying a 'scroll text' on the Raspberry Pi SenseHat's LED display. Mac users can comment out the relevant SenseHat codes appropriately.


### Steps

On the Pico: connect the servo motor to Pico with power via 3v3 pin, ground to ground, and data signal from GPIO 28. Note the calibration notes on `pico2.py` prior to running the codes.  

On the Raspberry Pi: run `pi2.py`. You can define the equity shown and the time between updates here. 

---

## Licence

UNLICENSE

