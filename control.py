#!/usr/bin/env python
#==========================================================
# MOVEMENT CONTROL SCRIPT                              v3.1
#==========================================================
import sys
from time import sleep
from time import time
import RPi.GPIO as GPIO
#==========================================================
GPIO.setmode(GPIO.BCM)
#==========================================================
if (len(sys.argv) == 4):
    
    command = int(sys.argv[1])
    value = float(sys.argv[2])
    duc = int(sys.argv[3])
    #=======================
    GPIO.setwarnings(False)
    #=======================
    GPIO.setup( 5, GPIO.OUT)
    pwm = GPIO.PWM(5, 15)
    pup = False
    #=======================
    GPIO.setup( 4, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)
    #-----------------------
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    #=======================
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    #-----------------------
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    #=======================
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21,  GPIO.IN)
    #-----------------------
    GPIO.output(20, False)
    #=======================

    def PWMToggle():
        global pup
        if (pup != True):
            if (duc != 100):
                pwm.start(duc)
                pup = True
            else:
                GPIO.output(5, GPIO.HIGH)
                pup = True
        else:
            pwm.stop()
            pup = False

    def stop():
        GPIO.output( 4, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(17, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)
        print("STOP")

    def TraceRoute(VT):
        ST = 0.05
        if (VT == 0):
            VT = 3600
        while (VT > 0):
            GPIO.output(20, True)
            sleep(0.00001)
            GPIO.output(20, False)
            while GPIO.input(21) == 0:
                pulse_start = time()
            while GPIO.input(21) == 1:
                pulse_end = time()
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            print distance," cm\n"
            if (distance < 5+duc*0.2):
                stop()
                VT = 0
            if (VT > ST):
                VT = VT - ST
                sleep(ST)
            else:
                sleep(VT)
                VT = 0
        stop()

    def forward(val):
        PWMToggle()
        GPIO.output(17, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)
        GPIO.output( 4, GPIO.HIGH)
        GPIO.output(27, GPIO.HIGH)
        GPIO.output(18, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        print("FORWARD")
        TraceRoute(val)
        PWMToggle()

    def backward(val):
        PWMToggle()
        GPIO.output( 4, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(22, GPIO.HIGH)
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(25, GPIO.HIGH)
        print("BACKWARD")
        if (val != 0):
	    sleep(val)
            stop()
        PWMToggle()			

    def left(val):    
        PWMToggle()
        GPIO.output(17, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        GPIO.output( 4, GPIO.HIGH)
        GPIO.output(27, GPIO.HIGH)
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(25, GPIO.HIGH)
        print("LEFT")
        if (val != 0):
            sleep(val)
            stop()
        PWMToggle()

    def right(val):
        PWMToggle()   	
        GPIO.output( 4, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(25, GPIO.LOW)
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(22, GPIO.HIGH)
        GPIO.output(18, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        print("RIGHT")
        if (val != 0):
	    sleep(val)
	    stop()
        PWMToggle()			
			
    if (command == 1):
        forward(value)
    elif (command == 2):
        backward(value)
    elif (command == 3):
        left(value)
    elif (command == 4):
        right(value)
    elif (command == 0):
        stop()
    else:
        print("Unknown command")

else:
    print("Usage: python control.py {0|1|2|3|4} SEC DC{0-100}");
#==========================================================
#                                              By SnipGhost
#==========================================================
