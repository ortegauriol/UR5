import sys
import math

def check(Acceleration, Velocity,X,Y,Z):
    if Velocity > 2.:
        print "Velocity Too High!"
        return False
    if Acceleration > 1:
        print "Acceleration Too High!"
        return False
    Length = math.sqrt((X**2)+(Y**2)+(Z**2))
    if Length > 1.2:
        print "Position Unreachable!"
        return False
    return True