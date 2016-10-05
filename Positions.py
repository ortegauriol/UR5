# This is server.py file
import socket                      # Import socket module
import sys   
import time  
import Sanity_Checks               # Import a function to check the sanity of position and velocity     
import os   
import math              

#hostname      = socket.gethostname()
#host          = socket.gethostbyname(hostname)

host          = "192.168.56.2"     # Virtual box Network Connection IP Address 
port          = 30000              # Reserve a port for your service.
X_origin      = 0.182883           # User enters the origin of the movement
Y_origin      = 0.570082
Z_origin      = 0.282641
Pause         = 3
movement_size = 0.05
Velocity      = "0.3"              # Setting the velocity of motion
Acceleration  = "0.005"            # Setting the acceleration of motion

print "Creating socket"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
s.bind((host, port))               # Bind to the port
s.listen(5)
#os.system("cls")                  # Clear the terminal screen of previous output
c, addr = s.accept()               # Establish connection with client.
print 'Got connection from', addr  # Confirm connection
print "Begin motion? Y/N"  
exit = raw_input()

Sanity_Checks.check(Acceleration, Velocity, \
                    float(X_origin), float(Y_origin), float(Z_origin), \
                    movement_size) # Ensuring the positions, velocity and acceleration are reasonable
origin = str(X_origin) + ',' + str(Y_origin) + ',' + str(Z_origin) + ',0,0,0'
if exit != "N":
   c.send('(' + origin + ',' + Acceleration + ',' + Velocity + ')')
   message = c.recv(1024)
   print message + ' to origin'
   time.sleep(Pause)  		

Movement_Vector = [0 * movement_size, 1 * movement_size, 2 * movement_size, \
                   3 * movement_size, 4 * movement_size]
while exit != "N":
    for i in range(0,5):
        for k in range(0,5):
            position = '(' + str(X_origin + Movement_Vector[k]) + ',' + \
                str(Y_origin) + ',' + str(Z_origin + Movement_Vector[i])+ \
                ',0,0,0,' + Acceleration + ',' + Velocity + ')'
            c.send(position) 
            print position
            message = c.recv(1024)
            print message
            time.sleep(Pause)
    print "Reached Final Destination"
    print "Repeat movement? Y/N" #Checks with the user if they wish to repeat movement
    Answer = raw_input()
    if Answer == "N":
        exit = "N"
    elif Answer != "N":
#        os.system("cls") # Clear the terminal screen of previous output
        print "Repeating motion now!"

time.sleep(Pause)
print "System will now shut down"
c.close()
s.close()
sys.exit()