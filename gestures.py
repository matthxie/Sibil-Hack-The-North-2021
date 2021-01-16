def stopTracking(indexY, indexX, thumbY, thumbX):
    if (abs(indexY - thumbY) < 0.15 and abs(indexX - thumbY) < 0.15):
        return True

def scroll(middleX, middleY, indexX, indexY):
    if (abs(middleX - indexX) < 0.025 and abs(middleY - indexY) < 0.025):
        return True
    return False
