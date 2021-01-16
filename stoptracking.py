def stopTracking(middleY, wristY):
    if (abs(middleY - wristY) < 0.2):
        return True
