#_*_coding:utf-8_*_
from config import *
import pygame.gfxdraw
import random
import pygame
import math
import copy
import numpy as np
import sys
import os
sys.path.append(os.getcwd())
from lib.utils import *
from lib.data import *

CLOCK = 0
cfg = Config.instance()

def randColor():
    color = [
    (130, 166, 245),
    (234, 240, 72),
    (159, 240, 72),
    (224, 54, 54),
    (237, 208, 190),
    (134, 155, 116),
    (255, 235, 204)
    ]
    return color[random.randint(0, len(color) - 1)]

def drawLine(screen, color, start, end, width):
    if start == end:
        return
    width /= 2.0
    start = np.array(start)
    end = np.array(end)
    dirc = end - start
    dirx = np.array([dirc[1], -1 * dirc[0]])
    dirx = dirx / math.sqrt(dirx[0] * dirx[0] + dirx[1] * dirx[1])
    point1 = start + dirx * width
    point2 = end + dirx * width
    start -= dirx * width
    end -= dirx * width

    points = [start, end, point2, point1]

    pygame.gfxdraw.filled_polygon(screen, points, color)
    pygame.gfxdraw.aapolygon(screen, points, color)
    # print(points)

class user(object):
    def __init__(self, data, db):
        self._data = data
        self._score = 0
        self._targetScore = 0
        self._color = randColor()
        self._name = data._code
        self._db = db
        self._snapShot = list()
        self._last = None
        self._lastPoint = None

        self._blingTime = 0.0

        self._update = True
        self._visual = False
    
    def name(self):
        if self._visual == False:
            return 0
        pos = lineMapping(self._db._minScore, self._db._maxScore, cfg.SCREEN_HEIGHT - cfg.BORDER_Y_DOWN,
                            cfg.BORDER_Y_TOP, self._score)

        endX = -100
        if self._last != None:
            endX = lineMapping(self._db._minDate, self._db._maxDate, cfg.BORDER_X_LEFT,
                                cfg.SCREEN_WIDTH - cfg.BORDER_X_RIGHT, self._last[0])
        text = self._db._text.render(self._name, True, self._color)
        if self._update:
            self._db._screen.blit(text, (cfg.POINT_X_LEFT + 10, pos - cfg.POINTRADIO))
        else:
            self._db._screen.blit(text, (endX + 10, pos - cfg.POINTRADIO))
        return 1

    def bling(self):
        if self._visual == False:
            return
        if self._blingTime <= 0.001:
            self._blingTime = 0
            return
        
        blingTime = 1.0 - self._blingTime
        radio = blingTime * cfg.BLINGRADIO
        pos = lineMapping(self._db._minScore, self._db._maxScore, cfg.SCREEN_HEIGHT - cfg.BORDER_Y_DOWN,
                            cfg.BORDER_Y_TOP, self._score)
        pos = int(pos)
        color = mergeColor(cfg.BGCOLOR, self._color, blingTime)
        pygame.gfxdraw.filled_circle(self._db._screen, cfg.POINT_X_LEFT, pos, int(radio), color)
        pygame.gfxdraw.aacircle(self._db._screen, cfg.POINT_X_LEFT, pos, int(radio), color)
        self._blingTime -= cfg.BLINGSPEED

        if radio >= cfg.BLINGRADIO:
            self._blingTime = 0.0
        return

    def show(self):
        if self._visual == False:
            return 0
        global CLOCK

        if CLOCK % cfg.LINE_SAMPLE_RATE == 0 and self._update == True:
            self._snapShot.append((self._db._nowDate, self._score))
        if self._update == True:
            self._last = (self._db._nowDate, self._score)
        
        poss = lineMapping(self._db._minScore, self._db._maxScore, cfg.SCREEN_HEIGHT - cfg.BORDER_Y_DOWN,
                            cfg.BORDER_Y_TOP, self._score)
        endX = -100
        if self._last != None:
            endX = lineMapping(self._db._minDate, self._db._maxDate, cfg.BORDER_X_LEFT,
                                cfg.SCREEN_WIDTH - cfg.BORDER_X_RIGHT, self._last[0])

        for i in range(len(self._snapShot) - 1):
            pos = lineMapping(self._db._minScore, self._db._maxScore, cfg.SCREEN_HEIGHT - cfg.BORDER_Y_DOWN, 
                                cfg.BORDER_Y_TOP, self._snapShot[i][1])
            pos1 = lineMapping(self._db._minScore, self._db._maxScore, cfg.SCREEN_HEIGHT - cfg.BORDER_Y_DOWN,
                                cfg.BORDER_Y_TOP, self._snapShot[i + 1][1])
            xpos = lineMapping(self._db._minDate, self._db._maxDate, cfg.BORDER_X_LEFT,
                                cfg.SCREEN_WIDTH - cfg.BORDER_X_RIGHT, self._snapShot[i][0])
            xpos1 = lineMapping(self._db._minDate, self._db._maxDate, cfg.BORDER_X_LEFT,
                                cfg.SCREEN_WIDTH - cfg.BORDER_X_RIGHT, self._snapShot[i + 1][0])
            #pygame.draw.line(self._db._screen, self._color, (xpos, pos), (xpos1, pos1), cfg.POINTLINE_WIDTH)
            drawLine(self._db._screen, self._color, (xpos, pos), (xpos1, pos1), cfg.POINTLINE_WIDTH)

            if i == len(self._snapShot) - 2:
                if self._update:
                    drawLine(self._db._screen, self._color, (xpos1, pos1), (cfg.POINT_X_LEFT, poss), cfg.POINTLINE_WIDTH)
                else:
                    drawLine(self._db._screen, self._color, (xpos1, pos1), (endX, poss), cfg.POINTLINE_WIDTH)

        poss = int(poss)
        endX = int(endX)
        if self._update:
            pygame.gfxdraw.aacircle(self._db._screen, cfg.POINT_X_LEFT, poss, cfg.POINTRADIO, self._color)
            pygame.gfxdraw.filled_circle(self._db._screen, cfg.POINT_X_LEFT, poss, cfg.POINTRADIO, self._color)
        else:
            pygame.gfxdraw.aacircle(self._db._screen, endX, poss, cfg.POINTRADIO, self._color)
            pygame.gfxdraw.filled_circle(self._db._screen, endX, poss, cfg.POINTRADIO, self._color)
        #pygame.draw.circle(self._db._screen, self._color, (cfg.POINT_X_LEFT, pos), cfg.POINTRADIO, 0)
        #text = self._db._text.render(str(int(self._score)), True, (200, 200, 200), self._color)
        #self._db._screen.blit(text, (cfg.BORDER_X_LEFT + self._score * BOXLEN - 40, self._nowPos))
        return 1

    def update(self):
        if len(self._snapShot) == 0:
            self._visual = False
        
        while self._snapShot and self._db._minDate - 500 > self._snapShot[0][0]:
            self._snapShot.remove(self._snapShot[0])
        
        if len(self._data._lst) == 0 or self._update == False:
            self._update = False
            return 0
        now = self._db._nowDate

        delta = 0
        if now >= self._data._lst[0]._value:

            if self._visual == False:
                self._blingTime = 1.0
                self._db._blingList.append(self)
            
            self._lastPoint = self._data._lst[0]
            self._data._lst.pop(0)

        if self._lastPoint != None and len(self._data._lst) != 0:
            self._score = sig(self._lastPoint._value, self._lastPoint._score, self._data._lst[0]._value, self._data._lst[0]._score, now)
            slopeValue = slope(self._lastPoint._value, self._lastPoint._score, self._data._lst[0]._value, self._data._lst[0]._score, now)

            if slopeValue * 10000 >  self._db._scoreRange and self._blingTime <= 0.0:
                self._blingTime = 1.0
                self._db._blingList.append(self)

        # delta = self._targetScore - self._score
        # if abs(delta) > SCORESPEED:
        #     delta /= abs(delta)
        #     delta *= SCORESPEED
        
        # self._score += delta
        if self._visual == True:
            self._db._minScore = min(self._db._minScore, self._score)
            self._db._maxScore = max(self._db._maxScore, self._score)
        
        return 1
        
class dashboard(object):
    def __init__(self, screen):
        self._users = list()
        self._screen = screen[0]
        self._text = screen[1]

        self._minDate = 0
        self._maxDate = 300
        self._minScore = -100
        self._maxScore = 100
        self._scoreRange = 200

        self._nowDate = 0

        self._select = None
        self._sector = "Default"
        self._blingList = list()
        
        self._dateFont = pygame.font.Font('lib/SimHei.ttf', 60)
    
    def loadData(self, sector):
        self._sector = sector
        data, self._time = get_data(sector)
        for s in data:
            self._users.append(user(data[s], self))
        
        self._minDate = self._time[0] - (cfg.DATE_WIDTH / 2.0)
        self._maxDate = self._minDate + cfg.DATE_WIDTH
        self._nowDate = self._time[0]

    def nowTime(self):
        showStr = stamp2Date(self._nowDate, "%Y-%m-%d %H:%M")
        text = self._dateFont.render(self._sector + "  " + showStr, True, cfg.TIMECOLOR)
        self._screen.blit(text, (cfg.SCREEN_WIDTH - cfg.BORDER_X_RIGHT - 800, cfg.BORDER_Y_TOP))

    def update(self):
        global CLOCK
        CLOCK += 1

        self._minDate += cfg.TIME_SPEED
        self._maxDate += cfg.TIME_SPEED
        self._nowDate = lineMapping(cfg.BORDER_X_LEFT, cfg.SCREEN_WIDTH - cfg.BORDER_X_RIGHT, self._minDate,
                                    self._maxDate, cfg.POINT_X_LEFT)

        minScore = self._minScore
        maxScore = self._maxScore
        midScore = (minScore + maxScore) / 2.0
        befDelta = maxScore - minScore

        self._minScore = 99999
        self._maxScore = -99999
        self._select = self._users[0]
        for u in self._users:
            u.update()

        if self._minScore != 99999 and self._maxScore != -99999:
        
            mmidScore = (self._minScore + self._maxScore) / 2.0 #新分数中点
            midDelta = (mmidScore - midScore) * cfg.MID_MOV_SPEED   #中点移动距离
            delta = self._maxScore - self._minScore             #新分数距离
            minDelta = midScore - minScore                      #min 向 mid 移动方向
            maxDelta = midScore - maxScore                #max 向 mid 移动方向

            if befDelta > delta * 2.0:
                rate = ((befDelta / delta) - 2.0) * cfg.BOX_MOV_RATIO   #线性插值变化率
                rate = stdRate(rate)
                minScore += minDelta * rate
                maxScore += maxDelta * rate
            elif befDelta < delta * 1.5:
                rate = (1.5 - (befDelta / delta)) * cfg.BOX_MOV_RATIO
                rate = stdRate(rate)
                minScore -= minDelta * rate
                maxScore -= maxDelta * rate
            
            minScore += midDelta
            maxScore += midDelta

        self._minScore = minScore
        self._maxScore = maxScore

        self._users.sort(key = lambda u: u._score, reverse = True)
        cnt = 0
        for u in self._users:
            if u._visual == True:
                cnt += 1
        for u in self._users:
            if cnt < cfg.TOP and u._update == True and u._visual == False:
                u._visual = True
                cnt += 1
        self._scoreRange = self._maxScore - self._minScore
    
    def rands(self):
        if random.randint(0, cfg.RANDSRATE) == 0:
            u = random.randint(0, len(self._users) - 1)
            if self._users[u]._score > 400:
                self._users[u]._a = -0.05
            elif self._users[u]._score < 0:
                self._users[u]._a = 0.05
            elif self._users[u]._v > 0:
                self._users[u]._a = -0.05
            else:
                self._users[u]._a = 0.05


    def bling(self):
        for u in self._blingList:
            u.bling()
        
        for b in self._blingList:
            if b._blingTime <= 0.0:
                self._blingTime = 0.0
                self._blingList.remove(b)

    def name(self):
        for u in self._users:
            u.name()
        
    def show(self):
        self.bling()
        self.auxLine()
        self.name()
        for u in self._users:
            u.show()
        self.block()
        self.unit()
        self.nowTime()

    def block(self):
        pygame.draw.rect(self._screen, cfg.BGCOLOR, [0, 0, cfg.BORDER_X_LEFT, cfg.SCREEN_HEIGHT], 0)
        pygame.draw.rect(self._screen, cfg.BGCOLOR, [0, 0, cfg.SCREEN_WIDTH, cfg.BORDER_Y_TOP], 0)
        pygame.draw.rect(self._screen, cfg.BGCOLOR, [0, cfg.SCREEN_HEIGHT - cfg.BORDER_Y_DOWN, cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT], 0)

    def auxLine(self):
        ind = 0
        for interval in cfg.AUXLINE_INTERVAL_DATE:
            start = int(self._minDate / interval)
            while start * interval < self._maxDate:
                if start * interval > self._minDate:
                    pos = lineMapping(self._minDate, self._maxDate, cfg.BORDER_X_LEFT, 
                                        cfg.SCREEN_WIDTH - cfg.BORDER_X_RIGHT, start * interval)
                    pygame.draw.line(self._screen, cfg.AUXLINE_COLOR, (pos, cfg.BORDER_Y_TOP),
                                        (pos, cfg.SCREEN_HEIGHT - cfg.BORDER_Y_DOWN), cfg.AUXLINE_WIDTH_DATE[ind])
                start += 1
            ind += 1
        
        ind = 0
        for interval in cfg.AUXLINE_INTERVAL_SCOR:
            start = int(self._minScore / interval)
            while start * interval < self._maxScore:
                if start * interval > self._minScore:
                    pos = lineMapping(self._minScore, self._maxScore, cfg.SCREEN_HEIGHT - cfg.BORDER_Y_DOWN,
                                        cfg.BORDER_Y_TOP, start * interval)
                    pygame.draw.line(self._screen, cfg.AUXLINE_COLOR, (cfg.BORDER_X_LEFT, pos),
                                        (cfg.SCREEN_WIDTH - cfg.BORDER_X_RIGHT, pos), cfg.AUXLINE_WIDTH_SCOR[ind])
                start += 1
            ind += 1

    def unit(self):
        ind = 0
        for interval in cfg.AUXLINE_INTERVAL_DATE:
            start = int(self._minDate / interval)
            while start * interval < self._maxDate:
                if start * interval > self._minDate:
                    pos = lineMapping(self._minDate, self._maxDate, cfg.BORDER_X_LEFT, 
                                        cfg.SCREEN_WIDTH - cfg.BORDER_X_RIGHT, start * interval)
                    text = self._text.render(stamp2Date(int(start * interval), "%m-%d %H"), True, (200, 200, 200), cfg.BGCOLOR)
                    self._screen.blit(text, (pos, cfg.SCREEN_HEIGHT - cfg.BORDER_Y_DOWN))
                start += 1
            ind += 1
        
        ind = 0
        for interval in cfg.AUXLINE_INTERVAL_SCOR:
            start = int(self._minScore / interval)
            while start * interval < self._maxScore:
                if start * interval > self._minScore:
                    pos = lineMapping(self._minScore, self._maxScore, cfg.SCREEN_HEIGHT - cfg.BORDER_Y_DOWN,
                                        cfg.BORDER_Y_TOP, start * interval)
                    text = self._text.render(str(int(start * interval)), True, (200, 200, 200), cfg.BGCOLOR)
                    self._screen.blit(text, (cfg.BORDER_X_LEFT - 30, pos))
                start += 1
            ind += 1
        
    def addTestUser(self):
        self._users.append(user(230, self))
        self._users.append(user(430, self))
        self._users.append(user(330, self))
        self._users.append(user(230, self))
        self._users.append(user(430, self))
        self._users.append(user(330, self))
        self._users.append(user(230, self))
        self._users.append(user(130, self))