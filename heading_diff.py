def getHeadingDiff(init, final): # var används getHeadDiff?
    if init > 360 or init < 0 or final > 360 or final < 0:
        raise Exception("out of range")
    diff = final - init
    absDiff = abs(diff)

    if absDiff == 180:
        return absDiff
    elif absDiff < 180:
        return diff
    elif final > init:
        return absDiff - 360
    else:
        return 360 - absDiff