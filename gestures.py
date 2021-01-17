def stopTracking(indexY, thumbY):
    if (abs(indexY - thumbY) < 0.1):
        return True
def scroll(middleX, middleY, indexX, indexY):
    if (abs(middleX - indexX) < 0.025 and abs(middleY - indexY) < 0.025):
        return True
    return False
def commandZoom(ringX, ringY, thumbX, thumbY):
    print()
    if(abs(ringX-thumbX) < 0.2 and abs(ringY-thumbY) <0.2):
        return True
 
