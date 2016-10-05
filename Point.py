# This is server.py file
import socket              			                                   # Import socket module
import sys   
import time  
import Sanity     					                                   #Import a function to check the sanity of position and velocity     
import os   
import math              

def Move_UR5(X,Y,Z):
  host           = "192.168.56.2"     			                        # Virtual box Network Connection IP Address 
  port           = 30000               			                        # Reserve a port for your service.
  Pause          = 3
  Velocity       = "0.3"                                                # Setting the velocity of motion
  Acceleration   = "0.005"                                              # Setting the acceleration of motion

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 # Create a socket object
  s.bind((host, port))                                                  # Bind to the port
  s.listen(5)
  c, addr = s.accept()                                                  # Establish connection with client.
  print 'Got connection from', addr                                     #Confirm connection

  Sanity.check(Acceleration, Velocity,X,Y,Z)                            # Ensuring the positions, velocity and acceleration are reasonable
  origin = str(X_origin)+','+str(Y_origin)+','+str(Z_origin)+',0,0,0'
  position = '('+X+','+Y+','+Z+',0,0,0,'+Acceleration+','+Velocity+')'
  c.send(position) 
  print position
  message = c.recv(1024)
  print message
  time.sleep(Pause)
  c.close()
  s.close()
  return message

