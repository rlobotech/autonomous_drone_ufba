#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time, sys
import ps_drone                # Imports the PS-Drone-API
import threading
import math
from gps import *
from haversine import haversine
from GPSController import GpsController
import cv2

# create the controller
gpsc = GpsController()

# Initializes the PS-Drone-API
drone = ps_drone.Drone()

# Limit angle to set the direction
LIMIT_ANGLE = 5

# Coodinate to base
coordinatesBase = (0.0, 0.0)

# Stop Mission
STOPPER = False


def checkDistance(pointB):
    try:
        if (type(pointB) != tuple):
            raise TypeError("The argument must be a tuple")
        while True:
            if (len(gpsc.satellites) > 0):
		coordinatesGPS = (gpsc.fix.latitude, gpsc.fix.longitude)
                distance = round(haversine(coordinatesGPS, pointB) * 1000)
                print "Distance: ", distance
                return distance
            else:
                print gpsc
                print "Looking for satellites..."

    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

def fixDirection(pointB):
    try:
        if (type(pointB) != tuple):
            raise TypeError("The argument must be a tuple")
        
        while True:
            if (len(gpsc.satellites) > 0):
                #heading = gpsc.fix.track      # heading = True North
		heading = drone.NavData["demo"][2][2]
                coordinatesGPS = (gpsc.fix.latitude, gpsc.fix.longitude)

                lat1 = math.radians(coordinatesGPS[0])
		lat2 = math.radians(pointB[0])
		
		diffLong = math.radians(pointB[1] - coordinatesGPS[1])
		
		x = math.sin(diffLong) * math.cos(lat2)
		y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
		        * math.cos(lat2) * math.cos(diffLong))
		
		bearing = math.atan2(x, y)
		bearing = math.degrees(bearing)


                if not math.isnan(bearing):
                    relativeBearing = round(-heading + bearing)
                    if relativeBearing > 180:
                        relativeBearing = relativeBearing - 360
                    if relativeBearing < -180:
                        relativeBearing = relativeBearing + 360
                   
                    print "CoordinatesGPS: %s PointB: %s " % (coordinatesGPS, pointB)
                    print "bearing: %s heading: %s relativeBearing: %s" % (bearing, heading, relativeBearing)
                    return relativeBearing
            else:
                print "Looking for satellites..."

    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

def getSpeed(distance):
    if distance > 100:
        speed = 1
    elif distance < 10:
        speed = 0.1
    else:
        speed = distance/100
    print "speed: ",speed
    return speed

def takePicture():
    number = len(next(os.walk("./pictures"))[2]) + 1
    urlAccess= "tcp:192.168.1.1:5555"
    file_pic = "./pictures/picture"+str(number)+".png"
    drone.setConfigAllID()                                           # Go to multiconfiguration-mode
    drone.sdVideo()                                              # Choose lower resolution (hdVideo() for...well, guess it)
    drone.groundCam() 
    cameraCapture = cv2.VideoCapture(urlAccess)
    print "Take a Picture..."
    success, frame = cameraCapture.read()
    cv2.imwrite(file_pic,frame)
    cameraCapture.release()
    drone.frontCam()

def checkBattery():
    print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])
    if drone.getBattery()[0] < 30:
        print "Battery is low"
        print "Returning to base"
        drone.stop()
        time.sleep(4)
        # Returning to base
        returnBase()

def mayday():
    print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])
    if drone.getBattery()[0] < 20:
        print "Mayday! mayday! mayday!"
        print "landing drone"
        drone.stop()
        time.sleep(4)
        # Landing the Drone
        drone.land()
        # Closing the file
        FILE.close()
        print "Stopping gps controller"
        gpsc.stopController()
        #wait for the tread to finish
        gpsc.join()
        sys.exit()

def returnBase():
    try:
        arrived = False
        while not arrived:
            mayday()
            distance = checkDistance(coordinatesBase)
            speed = getSpeed(distance)
            if distance <= 10:
                drone.stop()
                time.sleep(2)
		arrived = True
                print "Drone has been reached base..."
            else:
	        # ------- Calculing direction -------
	        direction = fixDirection(coordinatesBase)

                if abs(direction) > LIMIT_ANGLE:
                    print "Direction up to: ", LIMIT_ANGLE
                    drone.hover()
                    drone.turnAngle(direction,1)
                   
                #drone.moveTurnAngle(direction,speed)
                #drone.moveAltitude(altitude,speed)
                drone.moveForward(speed)
	
    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    finally:
        print "Stopping gps controller"
        gpsc.stopController()
        print "Pousando drone"
        drone.stop()
        time.sleep(4)
        # Landing the Drone
        drone.land()
        # Closing the file
        FILE.close()
        # wait for the tread to finish
        gpsc.join()



def startRoute(pointB, altitude):
    try:
        arrived = False
        initial = True
        while not arrived:
            checkBattery()
            distance = checkDistance(pointB)
            speed = getSpeed(distance)
            if distance <= 10:
                drone.stop()
                time.sleep(2)
		arrived = True
                #takePicture()
                print "The coordinate has been reached..."
            else:
	        # ------- Calculing direction -------
	        direction = fixDirection(pointB)

                if initial:
                    print "First moving to: ", direction
                    drone.turnAngle(direction,1)
                    initial = False              
                    #drone.moveAltitude(altitude,speed)
                    drone.moveForward(speed)
                elif abs(direction) > LIMIT_ANGLE:
                    print "Direction up to: ", LIMIT_ANGLE
                    drone.hover()
                    drone.turnAngle(direction,1)
                    #drone.moveTurnAngle(direction,speed)
                    #drone.moveAltitude(altitude,speed)
                    drone.moveForward(speed)
      
		# Stop mission
                if STOPPER:
                    drone.stop()
                    arrived = True
 
	
    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"
        returnBase()
    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        returnBase()
        raise

def mission(drone, gpsc):
    try:
        import cv2
        drone = drone
        gpsc = GpsController()

        gpsc = gpsc
        # Reading coordinates from mission.txt
        FILE = open('mission.txt', 'r')
        coordinates = FILE.readlines()

        # Starting the mission
        for coordinate in coordinates:
            coordinate = coordinate.split(',')
            altitude = float(coordinate[2])
            coordinate = (float(coordinate[0]), float(coordinate[1]))
            startRoute(coordinate,altitude)
            if STOPPER:
                break 
                    
        # Closing the file
        FILE.close()

        print "mission completed successfully"
        
        
	
    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    finally:
        # returning to base
        returnBase()

def stopMission():
    STOPPER = True

if __name__ == '__main__':
    try:
        # Reading coordinates from mission.txt
        FILE = open('mission.txt', 'r')
        coordinates = FILE.readlines()

        # start GPS controller
        gpsc.start()

        ##### Suggested clean drone startup sequence #####

        # Connects to the drone and starts subprocesses
        drone.startup()

        # Sets drone's status to good (LEDs turn green when red)
        drone.reset()

        # Sets drone's status to good (LEDs turn green when red)
        while (drone.getBattery()[0] == - 1):   time.sleep(0.1)

        # Gives the battery-status
        print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])

        # Give it up if battery is empty
        if drone.getBattery()[1] == "empty":
            print "Battery is empty"
            sys.exit()
        
        # Just give me 15 basic dataset per second (is default anyway)
        drone.useDemoMode(True)

        # Give it some time to awake fully after reset
        time.sleep(0.5)

        # Recalibrate sensors
        drone.trim()

        # Getting value for auto-alteration of gyroscope-sensor
        drone.getSelfRotation(5)
        print "Auto-alternation: "+str(drone.selfRotation)+" dec/sec"

        print "Espaco para iniciar"
        stop = False
        while not stop:
            key = drone.getKey()
            if key == " ":
                if drone.NavData["demo"][0][2] and not drone.NavData["demo"][0][3]:
                    stop = True
                    drone.takeoff()
                    print "Levantando voo..."                                                      
                    while drone.NavData["demo"][0][2]: time.sleep(0.1)	#Aguarda takeoff acabar
                    drone.moveUp()
                    time.sleep(3)
                    drone.stop()
                    time.sleep(1)
                   
                    # Starting the mission

                    coordinatesBase = (gpsc.fix.latitude, gpsc.fix.longitude)
                    for coordinate in coordinates:
                        coordinate = coordinate.split(',')
                        altitude = float(coordinate[2])
                        coordinate = (float(coordinate[0]), float(coordinate[1]))
                        startRoute(coordinate,altitude)
                        
                    # Closing the file
                    FILE.close()

    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    finally:
        # Returning to Base
        print "Given mission is accomplished mission!"
        print "Drone returning to base"
        returnBase()

