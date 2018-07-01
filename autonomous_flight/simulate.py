#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, sys
import ps_drone                # Imports the PS-Drone-API
import threading
import math
from gps import *
from haversine import haversine
from GPSController import GpsController

# create the controller
gpsc = GpsController()

# Initializes the PS-Drone-API
drone = ps_drone.Drone()

# Limit angle to set the direction
LIMIT_ANGLE = 10

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

def fixDirection(pointB,gpsc):
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
                    relativeBeading = round(-heading + bearing)
                    if relativeBeading > 180:
                        relativeBeading = relativeBeading - 360
                    if relativeBeading < -180:
                        relativeBeading = relativeBeading + 360
                   
                    print "CoordinatesGPS: %s PointB: %s " % (coordinatesGPS, pointB)
                    print "bearing: %s heading: %s relativeBeading: %s" % (bearing, heading, relativeBeading)
                    return relativeBeading
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
    elif distance < 20:
        speed = 0.2
    else:
        speed = distance/100
    print "speed: ",speed
    return speed

def takePicture():
    print "Take a Picture"

def checkBattery(gpsc):
    print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])
    if drone.getBattery()[0] < 20:
        print "Battery is empty"
        print "Stopping gps controller"
        gpsc.stopController()
        print "landing drone"
        drone.stop()
        time.sleep(4)
        # Landing the Drone
        drone.land()
        # Closing the file
        FILE.close()
        #wait for the tread to finish
        gpsc.join()
        sys.exit()


def startRoute(pointB, altitude):
    try:
        arrived = False
        initial = True
        while not arrived:
            checkBattery(gpsc)
            distance = checkDistance(pointB)
            speed = getSpeed(distance)
            if distance <= 2:
                print "drone.stop()"
                time.sleep(2)
		arrived = True
                takePicture()
                print "The coordinate has been reached..."
            else:
	        # ------- Calculing direction -------
	        direction = fixDirection(pointB,gpsc)

                if initial:
                    print "First moving to: ", direction
                    print "drone.turnAngle("+str(direction)+",1)"
                    initial = False              
                    print "drone.moveAltitude("+str(altitude)+","+str(speed)+")"
                elif abs(direction) > LIMIT_ANGLE:
                    print "Direction up to: ", LIMIT_ANGLE
                    print "drone.moveTurnAngle("+str(direction)+","+str(speed)+")"
                    print "drone.moveAltitude("+str(altitude)+","+str(speed)+")"

		
                # Stop mission
                if STOPPER:
                    drone.stop()
                    arrived = True

                raw_input("Press Enter to continue...")
                print "waiting 3 second..."
                time.sleep(3)
	
    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    #finally:
        #print "FINALLY"
        #print "Stopping gps controller"
        #gpsc.stopController()
        #print "Pousando drone"
        #drone.stop()
        #time.sleep(4)
        # Landing the Drone
        #drone.land()
        # Closing the file
        #FILE.close()
        #wait for the tread to finish
        #gpsc.join()

def mission(drone):
    try:
        drone = drone
        gpsc = GpsController()
        
        # Reading coordinates from mission.txt
        FILE = open('mission.txt', 'r')
        coordinates = FILE.readlines()

        # Starting the mission
        for coordinate in coordinates:
            coordinate = coordinate.split(',')
            altitude = float(coordinate[2])
            coordinate = (float(coordinate[0]), float(coordinate[1]))
            startRoute(coordinate,altitude,drone,gpsc)
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
        print "FINALLY 2"
        print "Stopping gps controller"
        gpsc.stopController()
        print "Pousando drone"
        drone.stop()
        time.sleep(4)
        # Landing the Drone
        drone.land()
        # Closing the file
        FILE.close()
        #wait for the tread to finish
        gpsc.join()

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
        #if drone.getBattery()[1] == "empty":
        #    print "Battery is empty"
        #    sys.exit()
        
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
                    print "drone.takeoff()"
                    print "Levantando voo..."                                                      
                    print "drone.moveUp()"
                    print "time.sleep(3)\ndrone.stop()\ntime.sleep(1)"
                   
                    # Starting the mission
                    for coordinate in coordinates:
                        coordinate = coordinate.split(',')
                        altitude = float(coordinate[2])
                        coordinate = (float(coordinate[0]), float(coordinate[1]))
                        startRoute(coordinate,altitude)
                    
                    # Closing the file
                    FILE.close()

                    "LAND 3"
                    # Landing the Drone
                    drone.land()

    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    finally:
        print "LAND 4"
        print "Stopping gps controller"
        gpsc.stopController()
        print "Pousando drone"
        drone.stop()
        time.sleep(4)
        # Landing the Drone
        drone.land()
        # Closing the file
        FILE.close()
        #wait for the tread to finish
        gpsc.join()

