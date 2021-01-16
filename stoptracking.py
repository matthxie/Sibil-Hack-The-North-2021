import math

def stopTracking(indexY, thumbY):
    if (math.fabs(indexY - thumbY) < 0.1):
        return True
