
def scroll(middleX, middleY, indexX, indexY):
    if (abs(middleX - indexX) < 0.025 and abs(middleY - indexY) < 0.025):
        return True
    return False