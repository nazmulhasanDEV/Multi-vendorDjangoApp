import datetime
import math


def dateTime_conversion(milliseconds):
    if milliseconds >= 86400000:
        days = math.trunc(milliseconds/86400000)
        hours = math.trunc((milliseconds%86400000)/3600000)
        minutes = math.trunc(((milliseconds%86400000)%3600000)/60000)
        return days, hours, minutes
    elif milliseconds>=3600000:
        hours = math.trunc(milliseconds/3600000)
        minutes = math.trunc((milliseconds%3600000)/60000)
        return hours, minutes
    elif milliseconds >= 60000:
        minutes = math.trunc(milliseconds/60000)
        return minutes
    elif milliseconds >= 1000:
        seconds = math.trunc(milliseconds/1000)
        return seconds
    else:
        return math.trunc(milliseconds)


print(dateTime_conversion(3700000))



