def stopTracking(indexY, indexX, thumbY, thumbX):
    if (abs(indexY - thumbY) < 0.15 and abs(indexX - thumbY) < 0.15):
        return True
