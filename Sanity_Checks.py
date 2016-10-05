import sys
import math
def check(Acceleration, Velocity,X,Y,Z,movement_size):
   Xmax=X+movement_size*4
   Xmin=X-movement_size*4
   Ymax=Y+movement_size*4
   Zmax=Z+movement_size*4
   Ymin=Z-movement_size*4
   Zmin=Z-movement_size*4
   if float(Velocity)>0.5:
       print "Velocity Too High!"
       print "System is shutting down!"
       sys.exit()
   if float(Acceleration)>1:
       print "Acceleration Too High!"
       print "System is shutting down!"
       sys.exit()
   MaxLenght= math.sqrt((Xmax**2)+(Y**2)+(Zmax**2))
   MinLenght=math.sqrt((X**2)+(Y**2)+(Z**2))
   if MaxLenght>0.85 or MinLenght>0.85:
       print "Position Unreachable!"
       print "System is shutting down!"
       sys.exit()
	  