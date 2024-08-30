# Import libraries

import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)

# Setup GPIO that will be used for control relay
GPIO.setup(18, GPIO.OUT) 

def open_garage_door():
    GPIO.output(18, GPIO.HIGH)
    time.sleep(2)  # Keep the relay activated for 2 seconds
    GPIO.output(18, GPIO.LOW)
    