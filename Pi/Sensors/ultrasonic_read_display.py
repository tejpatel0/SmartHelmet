from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1309
import RPi.GPIO as GPIO                                                 # Import the GPIO module as 'GPIO'

import time

serial = i2c(port=1, address=0x3C)                                      # Set I2C interface
device = ssd1309(serial)                                                # load the display reference
GPIO.setmode (GPIO.BCM)                                                 # Set the GPIO mode to BCM numbering
output_ports = [23,8,5,13,21]                                           # Define the GPIO output port numbers
input_ports = [24,7,6,19,20]                                            # Define the GPIO input port numbers

trig2=23                 # mid left                                       
echo2=24                                                                 
trig1=13                 # far left                                       
echo1=19                                                                 
trig3=5                                                                 
echo3=6                                                                 
trig4=8                                                                 
echo4=7                                                                
trig5=21                 # far right                                    
echo5=20                                                                

# HC-SR04 ULTRASONIC DISTANCE SENSOR                                *
# *******************************************************************
# * Unfortunately, the HC-SR04 suffers from some inherent built-in  *
# * flaws, particularly if the reflected sound waves bounce off     *
# * objects at a distance and/or at oblique angles.  This results   *
# * in very erratic signals being generated on the 'Echo' pin.      *
# * This function filters out most erratic events. If a valid       *
# * measurement was detected, the distance is given in cm units.    *
# * If a measurement error was detected, a negative error code is   *
# * returned.                                                       *
# *******************************************************************

def get_distance(echo, trig):
    if GPIO.input (echo):                                               # If the 'Echo' pin is already high
        return (-1)                                                     # then exit with error code

    distance = 0                                                        # Set initial distance to zero

    GPIO.output (trig,False)                                            # Ensure the 'Trig' pin is low for at
    time.sleep (0.03)                                                   # least 30mS

    GPIO.output (trig,True)                                             # Turn on the 'Trig' pin for 10us
    time.sleep (1e-5)

    GPIO.output (trig,False)                                            # Turn off the 'Trig' pin
    time.sleep (1e-5)

    if GPIO.input (echo):
        distance = -2                                                   # If a sensor error has occurred
        return (distance)                                               # then exit with error code

    time1, time2 = time.time(), time.time()                             #init times

    while not GPIO.input (echo):                                        # Wait for the start of the 'Echo' pulse
        time1 = time.time()                                             # Get the time the 'Echo' pin goes high
        if time1 - time2 > 0.02:                                        # If the 'Echo' pin doesn't go high after 20mS
            distance = -3                                              # then set 'distance' to 100
            break                                                         # and break out of the loop

    if distance == -3:                                                 # If a sensor error has occurred
        return (distance)                                               # then exit with 100 (sensor fault)

    time2 = time.time()
    while GPIO.input (echo):                                            # Otherwise, wait for the 'Echo' pin to go low
        time2 = time.time()                                             # Get the time the 'Echo' pin goes low
        if (time2 - time1 > 0.02):                                      # If the 'Echo' pin doesn't go low after 20mS
            distance = -4                                              # then ignore it and set 'distance' to 100
            break                                                       # and break out of the loop

    if (time2 - time1 < 3.0e-5):                                        # If the 'Echo' pin went low too fast
        distance = -5

    if distance < 0:                                                    # If a sensor error has occurred
        return (distance)                                               # then exit with error code

                                                                        # Sound travels at approximately 2.95uS per mm
                                                                        # and the reflected sound has travelled twice
                                                                        # the distance we need to measure (sound out,
                                                                        # bounced off object, sound returned)

    distance = (time2 - time1) / 0.00000295 / 2 / 10                    # Convert the timer values into centimetres
    return (distance)                                                   # Exit with the distance in centimetres

def draw_display(dist1, dist2, dist3, dist4, dist5):
    try:
        with canvas(device) as draw:
            # First we check for 9-12 ft range, then 6-9, then 0-6.
            #print("sensor 1 is:", dist1)
            #print("sensor 2 is:", dist2)
            #print("sensor 3 is:", dist3)
            #print("sensor 4 is:", dist4)
            if(dist1<350 and dist1>275 and dist1>0):
                draw.polygon([(0, 0), (0, 10), (10, 0)], outline="yellow", fill="black")
            elif(dist1>180 and dist1<=275 and dist1>0):
                draw.polygon([(0, 0), (0, 15), (15, 0)], outline="yellow", fill="black")
            elif(dist1>100 and dist1<=180 and dist1>0):
                draw.polygon([(0, 0), (0,20), (20, 0)], outline="yellow", fill="black")
            elif(dist1>1 and dist1<=100 and dist1>0):
                draw.polygon([(0, 0), (0,20), (20, 0)], outline="yellow", fill="white")
                
            if(dist2<350 and dist2>275 and dist2>0):
                draw.polygon([(0, 55), (0, 45), (10, 55)], outline="yellow", fill="black")
            elif(dist2>180 and dist2<=275 and dist2>0):
                draw.polygon([(0, 55), (0, 40), (15, 55)], outline="yellow", fill="black")
            elif(dist2>100 and dist2<=180 and dist2>0):
                draw.polygon([(0, 55), (0, 35), (20, 55)], outline="yellow", fill="black")
            elif(dist2>1 and dist2<=100 and dist2>0):
                draw.polygon([(0, 55), (0,35), (20, 55)], outline="yellow", fill="white")
            
            if(dist3<350 and dist3>275 and dist3>0):
                draw.polygon([(125, 0), (115, 0), (125, 10)], outline="yellow", fill="black")
            elif(dist3>180 and dist3<=275 and dist3>0):
                draw.polygon([(125, 0), (110, 0), (125, 15)], outline="yellow", fill="black")
            elif(dist3>100 and dist3<=180 and dist3>0):
                draw.polygon([(125, 0), (105, 0), (125, 20)], outline="yellow", fill="black")
            elif(dist3>1 and dist3<=100 and dist3>0):
                draw.polygon([(125, 0), (105, 0), (125, 20)], outline="yellow", fill="white")

            if(dist4<350 and dist4>275 and dist4>0):
                draw.polygon([(125, 55), (115, 55), (125, 45)], outline="yellow", fill="black")
            elif(dist4>180 and dist4<=275 and dist4>0):
                draw.polygon([(125, 55), (110, 55), (125, 40)], outline="yellow", fill="black")
            elif(dist4>100 and dist4<=180 and dist4>0):
                draw.polygon([(125, 55), (105, 55), (125, 35)], outline="yellow", fill="black")
            elif(dist4>1 and dist4<=100 and dist4>0):
                draw.polygon([(125, 55), (105, 55), (125, 35)], outline="yellow", fill="white")

    except:
        #call the draw function again
        time.sleep(0.01)
        draw_display(dist1, dist2, dist3, dist4)

if __name__ == "__main__":
    distance1 = 1
    distance2 = 1
    distance3 = 1
    distance4 = 1
    for bit in output_ports:                                                # Set up the six output bits
        GPIO.setup (bit,GPIO.OUT)
        GPIO.output (bit,False)                                             # Initially turn them all off

    for bit in input_ports:                                                 # Set up the six input bits
        GPIO.setup (bit,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)              # Set the inputs as normally low
    while True:
        temp1 = get_distance(echo1, trig1)
        temp2 = get_distance(echo2, trig2)
        temp3 = get_distance(echo3, trig3)
        temp4 = get_distance(echo4, trig4)
        temp5 = get_distance(echo5, trig5)
        #if temp1>0:
        distance1 = round(temp1)
        #if temp2>0:
        distance2 = round(temp2)
        #if temp3>0:
        distance3 = round(temp3)
        #if temp4>0:
        distance4 = round(temp4)
        
        time.sleep(0.01)
        draw_display(distance1, distance2, distance3, distance4)