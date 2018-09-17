#_*_coding:utf-8_*_
from config import *
import time, datetime
import math

def lineMapping(left1, right1, left2, right2, mid1):
    delta1 = right1 - left1
    delta2 = right2 - left2

    scale = delta2 / delta1
    trueDelta = scale * (mid1 - left1)
    realPos = trueDelta + left2
    return realPos

def mergeColor(backGround, upper, alpha):
    return (backGround[0] * alpha + upper[0] * (1 - alpha),
            backGround[1] * alpha + upper[1] * (1 - alpha),
            backGround[2] * alpha + upper[2] * (1 - alpha)
            )

def date2Stamp(date):
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    hour = date[8:10]
    newDate = "%s-%s-%s-%s" % (year, month, day, hour)
    timearray = time.strptime(newDate, "%Y-%m-%d-%H")
    timeStamp = int(time.mktime(timearray))
    #print(year, month, day, hour)
    return timeStamp

def stamp2Date(stamp, form):
    # "%Y-%m-%d %H:%M:%S"
    timeArray = time.localtime(stamp)
    otherStyleTime = time.strftime(form, timeArray)
    return otherStyleTime

def sigmoid(x):
    # if x > 0:
    #     x = math.log(x + 1.0)
    # else:
    #     x = -1.0 * math.log((-1.0 * x) + 1.0)
    return 1.0 / (1.0 + math.exp(-1.0 * x))

def sig(x1, y1, x2, y2, t):
    delta = y2 - y1
    sigDelta = sigmoid(5.0) - sigmoid(-5.0)
    x = lineMapping(x1, x2, -5.0, 5.0, t)
    y = sigmoid(x) * delta / sigDelta + y1
    return y

def slope(x1, y1, x2, y2, t):
    dx = 0.01
    dy = sig(x1, y1, x2, y2, t + dx) - sig(x1, y1, x2, y2, t)
    return dy / dx

if __name__ == "__main__":
    stamp = date2Stamp("2018052007")
    print(stamp)
    print(stamp2Date(stamp+50, "%Y-%m-%d %H:%M:%S"))

    for i in range(5):
        print(sigmoid(i))