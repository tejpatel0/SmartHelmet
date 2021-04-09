from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1309
import RPi.GPIO as GPIO                                                 # Import the GPIO module as 'GPIO'
from hcsr04sensor import sensor

import time

serial = i2c(port=1, address=0x3C)                                      # Set I2C interface
device = ssd1309(serial)                                                # load the display reference
GPIO.setmode (GPIO.BCM)                                                 # Set the GPIO mode to BCM numbering

trig4=23                 # mid right                                       
echo4=24                                                                 
trig5=13                 # far right                                       
echo5=19                                                                 
trig3=5                  # behind                                               
echo3=6                                                                 
trig2=8                  # mid left                                              
echo2=7                                                                
trig1=21                 # far left                                    
echo1=20                             
configFill = "black"                                   

def draw_display(dist1, dist2, dist3, dist4, dist5):
    try:
        with canvas(device) as draw:
            # First we check for 9-12 ft range, then 6-9, then 0-6.
            #print("sensor 1 is: ", dist1)
            #print("sensor 2 is: ", dist2)
            #print("sensor 3 is: ", dist3)
            #print("sensor 4 is: ", dist4)
            #print("sensor 5 is: ", dist5)
            if(dist1<350 and dist1>275 and dist1>0):
                draw.polygon([(12.5, 6.875), (0, 13.75), (12.5, 20.625)], outline="yellow", fill=configFill)
            elif(dist1>180 and dist1<=275 and dist1>0):
                draw.polygon([(17.5, 4.125), (0, 13.75), (17.5, 23.375)], outline="yellow", fill=configFill)
            elif(dist1>100 and dist1<=180 and dist1>0):
                draw.polygon([(25, 0), (0,13.75), (25, 27.5)], outline="yellow", fill=configFill)
            elif(dist1>1 and dist1<=100 and dist1>0):
                draw.polygon([(25, 0), (0,13.75), (25, 27.5)], outline="yellow", fill=configFill)
                
            if(dist2<350 and dist2>275 and dist2>0):
                draw.polygon([(12.5, 48.125), (0, 41.25), (12.5, 34.375)], outline="yellow", fill=configFill)
            elif(dist2>180 and dist2<=275 and dist2>0):
                draw.polygon([(17.5, 50.875), (0, 41.25), (17.5, 31.625)], outline="yellow", fill=configFill)
            elif(dist2>100 and dist2<=180 and dist2>0):
                draw.polygon([(25, 55), (0,41.25), (25, 27.5)], outline="yellow", fill=configFill)
            elif(dist2>1 and dist2<=100 and dist2>0):
                draw.polygon([(25, 55), (0,41.25), (25, 27.5)], outline="yellow", fill=configFill)

            if(dist3<350 and dist3>275 and dist3>0):
                draw.polygon([(62.5, 55), (55.625,42.5), (69.375, 42.5)], outline="yellow", fill=configFill)
            elif(dist3>180 and dist3<=275 and dist3>0):
                draw.polygon([(62.5, 55), (52.875,37.5), (72.125, 37.5)], outline="yellow", fill=configFill)
            elif(dist3>100 and dist3<=180 and dist3>0):
                draw.polygon([(62.5, 55), (48.75,30), (76.25, 30)], outline="yellow", fill=configFill)
            elif(dist3>1 and dist3<=100 and dist3>0):
                draw.polygon([(62.5, 55), (48.75,30), (76.25, 30)], outline="yellow", fill=configFill)

            if(dist4<350 and dist4>275 and dist4>0):
                draw.polygon([(112.5, 48.125), (125, 41.25), (112.5, 34.375)], outline="yellow", fill=configFill)
            elif(dist4>180 and dist4<=275 and dist4>0):
                draw.polygon([(107.5, 50.875), (125, 41.25), (107.5, 31.625)], outline="yellow", fill=configFill)
            elif(dist4>100 and dist4<=180 and dist4>0):
                draw.polygon([(100, 55), (125, 41.25), (100, 27.5)], outline="yellow", fill=configFill)
            elif(dist4>1 and dist4<=100 and dist4>0):
                draw.polygon([(100, 55), (125, 41.25), (100, 27.5)], outline="yellow", fill=configFill)

            if(dist5<350 and dist5>275 and dist5>0):
                draw.polygon([(112.5, 6.875), (125, 13.75), (112.5, 20.625)], outline="yellow", fill=configFill)
            elif(dist5>180 and dist5<=275 and dist5>0):
                draw.polygon([(107.5, 4.125), (125, 13.75), (107.5, 23.375)], outline="yellow", fill=configFill)
            elif(dist5>100 and dist5<=180 and dist5>0):
                draw.polygon([(100, 0), (125, 13.75), (100, 27.5)], outline="yellow", fill=configFill)
            elif(dist5>1 and dist5<=100 and dist5>0):
                draw.polygon([(100, 0), (125, 13.75), (100, 27.5)], outline="yellow", fill=configFill)

    except:
        #call the draw function again
        time.sleep(0.01)
        draw_display(dist1, dist2, dist3, dist4, dist5)

if __name__ == "__main__":
    # read from config files
    try:
        f = open('/etc/sensing/design.config','r')
        design = f.readline().rstrip()
        if design=="fill":
            configFill = "white"
        else:
            configFill = "black"
    except FileNotFoundError:
        # file does not exist, continue as is.
        configFill = "black"
        pass
    value1 = sensor.Measurement(trig1, echo1)
    value2 = sensor.Measurement(trig2, echo2)
    value3 = sensor.Measurement(trig3, echo3)
    value4 = sensor.Measurement(trig4, echo4)
    value5 = sensor.Measurement(trig5, echo5)
    samples = 2 # number of samples taken at once
    speed = 0.05 # time between individual readings
    while True:
        distance1 = value1.raw_distance(sample_size=samples, sample_wait=speed)
        distance2 = value2.raw_distance(sample_size=samples, sample_wait=speed)
        distance3 = value3.raw_distance(sample_size=samples, sample_wait=speed)
        distance4 = value4.raw_distance(sample_size=samples, sample_wait=speed)
        distance5 = value5.raw_distance(sample_size=samples, sample_wait=speed)
        metric_distance1 = value1.distance_metric(distance1) # get distance in cm
        metric_distance2 = value2.distance_metric(distance2) # get distance in cm
        metric_distance3 = value3.distance_metric(distance3) # get distance in cm
        metric_distance4 = value4.distance_metric(distance4) # get distance in cm
        metric_distance5 = value5.distance_metric(distance5) # get distance in cm
        """
        if(metric_distance > 360):
            # out of range
            print("Out of range")
        else:
            print(distance3,"cm")
        """
        draw_display(metric_distance1, metric_distance2, metric_distance3, metric_distance4, metric_distance5)