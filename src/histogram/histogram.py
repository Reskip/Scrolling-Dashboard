#_*_coding:utf-8_*_
import math
import pygame
import time
import sys
import random
from config import *
from pygame.locals import *
import os
sys.path.append(os.getcwd())
from lib.data import *

pygame.init()

SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], RESIZABLE)
pygame.display.set_caption(TITLE)
font = pygame.font.Font('lib/SimHei.ttf', FONTSIZE)

startDate = -1
endDate = -1
curDate = startDate
curTime = 0
stop = 0
dates = list()
datemap = {}
times = list()
timemap = {}
names = list()
namemap = {}
rng_sv = list()

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


class Button(object):
    def __init__(self, name, x, y):
        self._name = name
        self._color = (255, 255, 255)
        self._state = 0 #当前是否被点击
        self._posx = x
        self._posy = y

    def show(self):
        #print("%d, %d, %d, %d" %(self._posx, self._posy, BUTTONHEIGHT, BUTTONWIDTH))
        pygame.draw.rect(screen, self._color,
                [self._posx, self._posy, BUTTONWIDTH, BUTTONHEIGHT], 0)
        name = font.render(self._name, True, (0, 0, 0))
        screen.blit(name, (self._posx, self._posy))

class inputBox(object):
    def __init__(self, title, content, x, y):
        self._title = title
        self._posx = x
        self._posy = y
        self._width = INPUTBOXWIDTH
        self._height = INPUTBOXHEIGHT
        self._state = 0 #表示当前是否处于输入状态
        self._msg = content

    
    def show(self):
        title = font.render(self._title + ":", True, (200, 200, 200))
        screen.blit(title, (self._posx - 50, self._posy))
        pygame.draw.rect(screen, (200, 200, 200),
                [self._posx - 2, self._posy - 2, self._width + 4, self._height + 4], 0)
        pygame.draw.rect(screen, (0, 0, 0),
                [self._posx, self._posy, self._width, self._height], 0)
        if self._state == 1: msg = self._msg + "|"
        else : msg = self._msg
        massage = font.render(msg, True, (200, 200, 200))
        screen.blit(massage, (self._posx, self._posy))

class inputBoxWithButton(object):
    def __init__(self, titles, contents, locx, locy):
        self._inputboxs = list()
        for i in range(len(titles) - 1):
            self._inputboxs.append(inputBox(titles[i], contents[i], locx[i], locy[i]))
        self._button = Button(titles[-1], locx[-1], locy[-1])
    
    def show(self):
        for i in range(len(self._inputboxs)):
            self._inputboxs[i].show()
        self._button.show()

class speedControl(object):
    def __init__(self, posx, posy):
        self._speed = 5.0
        self._posx = posx
        self._posy = posy
        self._width = 120
        self._height = 3
        self._state = 0 #是否正被拖动
        self._color = (200, 200, 200)
    
    def show(self):
        name = font.render("速度: ", True, self._color)
        screen.blit(name, (self._posx - 50, self._posy - 8))
        pygame.draw.rect(screen, (200, 200, 200),
                [self._posx, self._posy - self._height / 2, self._width, self._height], 0)
        pygame.draw.rect(screen, (255,140,0),
                [self._posx + self._speed / 10 * self._width - 5, self._posy - 5, 10, 10], 0)
    
    def checkMouseMove(self, event):
        global SPEED
        mousex = 0
        mousey = 0
        try:
            mousex = event.pos[0]
            mousey = event.pos[1]
        except: pass

        if event.type == pygame.MOUSEBUTTONDOWN \
            and mousex > self._posx + self._speed / 10 * self._width - 5 and mousex < self._posx + self._speed / 10 * self._width + 5 \
            and mousey > self._posy - 5 and mousey < self._posy + 5:
            self._state = 1

        elif self._state == 1:
            try:
                mousex = event.pos[0]
                mousey = event.pos[1]
                self._speed = round((mousex - self._posx) / self._width * 10, 4)
                if self._speed < 0: self._speed = 0
                if self._speed >= 10: self._speed = 9.9
                SPEED = 10 - self._speed
            except: pass

        if event.type == pygame.MOUSEBUTTONUP \
            and self._state == 1:
            self._state = 0
                
class shadow(object):
    def __init__(self, posx, posy, score, height, color):
        self._posx = posx
        self._posy = posy
        self._score = score
        self._height = height
        self._color = color

    def show(self):
        pygame.draw.rect(screen, self._color,
                [self._posx, self._posy, self._score * BOXLEN, self._height], 0)

class user(object):
    def __init__(self, id, name, score):
        self._id = id
        self._name = name
        self._score = score
        self._targetScore = score
        self._color = randColor()
        self._height = BOXHEIGHT
        self._rank = 0
        self._nowPos = BORDER_Y
        self._seleced = 0
    
    def show(self):

        if self._seleced == 1:
            pygame.draw.rect(screen, (200, 200, 200),
                [10, self._nowPos - 1, SCREEN_WIDTH - 20, BOXHEIGHT + 2], 0)
            pygame.draw.rect(screen, (0, 0, 0),
                [11, self._nowPos, SCREEN_WIDTH - 22, BOXHEIGHT], 0)
            #print(self._name)

        score = font.render(str(round(float(self._score), 2)), True, self._color)
        name = font.render("No." + str(self._rank + 1) + " " + self._name, True, self._color)
        screen.blit(name, (BORDER_X - 135, self._nowPos))

        if self._score >= 0:
            pygame.draw.rect(screen, self._color,
                [CENTER_X, self._nowPos, self._score * BOXLEN, BOXHEIGHT], 0)
            screen.blit(score, (CENTER_X + self._score * BOXLEN + 10, self._nowPos))
        else :
            pygame.draw.rect(screen, self._color,
                [CENTER_X - abs(self._score) * BOXLEN, self._nowPos, abs(self._score) * BOXLEN, BOXHEIGHT], 0)
            screen.blit(score, (CENTER_X - abs(self._score) * BOXLEN - 70, self._nowPos))
        
    def update(self, showNum, deltatime):
        target = self._rank * RANKHEIGHT + BORDER_Y
        delta = target - self._nowPos
        if abs(delta) > FLOATSPEED * deltatime:
            delta /= abs(delta)
            delta *= FLOATSPEED * deltatime
        
        self._nowPos += delta

        delta = self._targetScore - self._score
        if abs(delta) > SCORESPEED * deltatime:
            delta /= abs(delta)
            delta *= SCORESPEED * deltatime
        
        self._score += delta

class dashboard(object):
    global datemap
    def __init__(self):
        self._users = list()
        self._inputboxswithbutton = None
        self._totalPositive = 0
        self._shadows = list()
        self._showNum = 50 #展示前多少名
        self._speedcontrol = None
        self._selectedName = None
    
    def updateRank(self, deltatime):
        self._users = sorted(self._users, key = lambda user : user._score, reverse = True)
        for i in range(len(self._users)):
            self._users[i]._rank = min(i, self._showNum + 1)
        for u in self._users:
            u.update(self._showNum, deltatime)
        
        curPositive = 0
        for u in self._users:
            if u._score > 0:
                curPositive += u._score
        if curPositive >= self._totalPositive:
            self._totalPositive = curPositive
            self._shadows.clear()
            for u in self._users:
                if u._score <= 0: break
                if u._nowPos == u._rank * RANKHEIGHT + BORDER_Y:
                    self._shadows.append(shadow(CENTER_X, u._nowPos, u._score, BOXHEIGHT, SHADOWCOLOR))
    
    def checkMouseDown(self, mousex, mousey):
        #输入框
        global startDate
        global endDate
        global curDate
        global FLOATSPEED

        #选中输入框
        for i in range(len(self._inputboxswithbutton._inputboxs)):
            self._inputboxswithbutton._inputboxs[i]._state = 0

        for i in range(len(self._inputboxswithbutton._inputboxs)):
            if mousex > self._inputboxswithbutton._inputboxs[i]._posx and mousex < self._inputboxswithbutton._inputboxs[i]._posx + INPUTBOXWIDTH \
                and mousey > self._inputboxswithbutton._inputboxs[i]._posy and mousey < self._inputboxswithbutton._inputboxs[i]._posy + INPUTBOXHEIGHT:
                for j in range(len(self._inputboxswithbutton._inputboxs)):
                    self._inputboxswithbutton._inputboxs[j]._state = 0

                self._inputboxswithbutton._inputboxs[i]._state = 1
                #print("inputbox " + str(i))
                return False

        #确定按钮
        if mousex > self._inputboxswithbutton._button._posx \
            and mousex < self._inputboxswithbutton._button._posx + BUTTONWIDTH \
            and mousey > self._inputboxswithbutton._button._posy \
            and mousey < self._inputboxswithbutton._button._posy + BUTTONHEIGHT: 
            
            print("确定")
            print(self._inputboxswithbutton._inputboxs[0]._msg)

            if len(self._inputboxswithbutton._inputboxs[0]._msg) != 0 \
                and len(self._inputboxswithbutton._inputboxs[1]._msg) != 0 \
                and len(self._inputboxswithbutton._inputboxs[2]._msg) != 0 \
                and datemap.get(int(self._inputboxswithbutton._inputboxs[1]._msg)) != None \
                and datemap.get(int(self._inputboxswithbutton._inputboxs[2]._msg)) != None \
                and int(self._inputboxswithbutton._inputboxs[2]._msg) >= int(self._inputboxswithbutton._inputboxs[1]._msg):

                self._showNum = int(self._inputboxswithbutton._inputboxs[0]._msg)
                startDate = datemap[int(self._inputboxswithbutton._inputboxs[1]._msg)]
                endDate = datemap[int(self._inputboxswithbutton._inputboxs[2]._msg)]
                curDate = startDate = startDate

                print(self._showNum)
                
                return True
        
        if mousex < SCREEN_WIDTH - BORDERX_INPUTBOX - 50 \
            or mousey < BORDERY_INPUTBOX - 50: #选中某一行, 控件部分去除

            for i in range(len(self._users)):
                if mousey > self._users[i]._nowPos \
                    and mousey < self._users[i]._nowPos + RANKHEIGHT \
                    and self._users[i]._rank < self._showNum:

                    for j in range(len(self._users)):
                        self._users[j]._seleced = 0

                    self._users[i]._seleced = 1
                    self._selectedName = self._users[i]._name
                    break
        

                    
        return False #返回False表示日期不用更新
        
    def modifyScore(self, dateid, timeid):

        for i in range(len(self._users)):
            self._users[i]._targetScore = rng_sv[self._users[i]._id][dateid * INSERTTIME + timeid]

    def show(self, date):

        global MAXLEN
        global BOXLEN #单位长度
        global MAXNLENGTH
        BOXLEN = MAXLEN / MAXNLENGTH

        for i in range(len(self._shadows)):
            if self._shadows[i]._score > 0:
                self._shadows[i].show()

        for i in range(len(self._users)):
            if i >= self._showNum: 
                self._users[i]._seleced = 0
                continue
            self._users[i].show()
        
        self._selectedName = None
        for i in range(len(self._users)):
            if self._users[i]._seleced == 1:
                self._selectedName = self._users[i]._name
        #print(self._selectedName)

        '''
        #控制控件
        pygame.draw.rect(screen, (0, 0, 0),
                [SCREEN_WIDTH - BORDERX_INPUTBOX - 50, BORDERY_INPUTBOX - 50, 200, 200], 0)
        '''

        self._inputboxswithbutton.show()
        self._speedcontrol.show()

        #提示信息
        text = font.render(str(date) + "   最大正值: " + str(round(self._totalPositive, 2)), True, (200, 200, 200))
        screen.blit(text, (BORDER_X, BORDER_Y - 15))
        
ds = dashboard()

restart = 0
def frameDraw(deltatime):
    global FLOATSPEED
    global SCORESPEED
    global SCREEN_WIDTH
    global SCREEN_SIZE
    global CENTER_X
    global BORDERY_INPUTBOX
    global MAXLEN
    global screen
    global font
    global startDate
    global endDate
    global stop
    global curDate
    global curTime
    global rng_sv
    global dates
    global names
    global ds
    global restart

    returnState = 0 #返回零表示继续显示，返回1表示重新显示

    screen.fill(BGCOLOR)
    ds.updateRank(deltatime)
    ds.show("当前时间:" + str(dates[curDate]) + " " + times[curTime] + "    开始时间:" + str(dates[startDate]) + "    结束时间:" + str(dates[endDate]))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == VIDEORESIZE: #调整屏幕大小
            # get the size of the window
            SCREEN_WIDTH, SCREEN_HEIGHT = event.size
            CENTER_X = SCREEN_WIDTH / 2
            MAXLEN = SCREEN_WIDTH * 0.4
            BORDERY_INPUTBOX = SCREEN_HEIGHT - 100
            # set the mode of the window
            screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], RESIZABLE)
            pygame.display.set_caption(TITLE)
            font = pygame.font.Font('lib/SimHei.ttf', FONTSIZE)

            #初始化dashboard
            ds._inputboxswithbutton = inputBoxWithButton(
                ["排名", "开始", "结束", "确定"],
                [str(ds._showNum), str(dates[startDate]), str(dates[endDate])],
                [SCREEN_WIDTH - BORDERX_INPUTBOX, SCREEN_WIDTH - BORDERX_INPUTBOX, SCREEN_WIDTH - BORDERX_INPUTBOX, (SCREEN_WIDTH - BORDERX_INPUTBOX) + INPUTBOXWIDTH + 10],
                [BORDERY_INPUTBOX, BORDERY_INPUTBOX + INPUTBOXHEIGHT + 10, BORDERY_INPUTBOX + 2 * (INPUTBOXHEIGHT + 10), BORDERY_INPUTBOX]
            )
            ds._speedcontrol = speedControl(SCREEN_WIDTH - BORDERX_INPUTBOX, BORDERY_INPUTBOX -20)

        elif event.type == pygame.MOUSEBUTTONDOWN \
            and event.button == 1: #左键
            updateDate = ds.checkMouseDown(event.pos[0], event.pos[1])
            if updateDate == True: returnState = 1

        elif event.type == KEYDOWN: #键盘输入
            for j in range(len(ds._inputboxswithbutton._inputboxs)):
                if ds._inputboxswithbutton._inputboxs[j]._state == 0: continue
                if event.key == K_BACKSPACE:
                    ds._inputboxswithbutton._inputboxs[j]._msg = ds._inputboxswithbutton._inputboxs[j]._msg[0: -1]
                elif event.key >= 48 and event.key <= 57:
                    ds._inputboxswithbutton._inputboxs[j]._msg = ds._inputboxswithbutton._inputboxs[j]._msg + chr(event.key)
            if event.key == ord('s') or event.key == ord('S'):
                prestop = stop
                stop = stop ^ 1
                if prestop == 1 and stop == 0: restart = 1

        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        ds._speedcontrol.checkMouseMove(event)

    return returnState

def draw():
    global FLOATSPEED
    global SCORESPEED
    global SCREEN_WIDTH
    global SCREEN_SIZE
    global CENTER_X
    global BORDERY_INPUTBOX
    global MAXLEN
    global screen
    global startDate
    global endDate
    global stop
    global curDate
    global curTime
    global rng_sv
    global dates
    global names
    global ds
    global restart

    ds._totalPositive = 0
    ds._users.clear()
    ds._shadows.clear()
    for i in range(len(names)):
        ds._users.append(user(i, names[i], 0))

    global SPEED
    global FLOATSPEED
    global SCORESPEED

    FLOATSPEED = (ds._showNum) * RANKHEIGHT / SPEED / 0.8
    
    global MAXNLENGTH
    MAXNLENGTH = 1
    for i in range(startDate, endDate + 1):
        for j in range(INSERTTIME):
            if i * INSERTTIME + j >= len(rng_sv[0]): break
            for k in range(len(names)):
                if abs(rng_sv[k][i * INSERTTIME + j]) > MAXNLENGTH:
                    MAXNLENGTH = abs(rng_sv[k][i * INSERTTIME + j])

    curTime = 0
    stop = 0
    restart = 0
    while curTime < INSERTTIME:
        restart = 0
        if stop == 0:
            if curDate * INSERTTIME + curTime >= len(rng_sv[0]):
                break
            ds.modifyScore(curDate, curTime)
            maxdiff = 0
            for i in range(len(names)):
                if abs(ds._users[i]._score - ds._users[i]._targetScore) > maxdiff:
                    maxdiff = abs(ds._users[i]._score - ds._users[i]._targetScore)
            SCORESPEED = maxdiff / SPEED / 0.7
            FLOATSPEED = (ds._showNum) * RANKHEIGHT / SPEED / 0.8

        pretime = time.time()
        last = pretime
        while True:
            now = time.time()
            if now - pretime > SPEED: break
            returnState = frameDraw(now - last)
            if returnState == 1: return

            if restart == 1: break
            last = now
        if stop == 0:
            curTime = curTime + 1
    
    curDate = curDate + 1
    if(curDate > endDate):
        curDate -=1
        if curTime == INSERTTIME: curTime -= 1
        curDate = startDate
        pretime = time.time()
        nowtime = time.time()
        last = pretime
        while nowtime - pretime < 180:
            nowtime = time.time()
            returnState = frameDraw(nowtime - last)
            if returnState == 1: return
            last = nowtime
        return
    curDate += 1
        
def innerDraw(sector):
    global rng_sv
    global dates
    global times
    global names

    datas, stamps = get_data(sector)
    
    tot = 0
    for stamp in stamps:
        times.append(stamp2Date(stamp, "%H:%M"))
        timemap[stamp2Date(stamp, "%H:%M")] = tot
        tot += 1
    print('***************************')
    print(times)

    #获取日期
    dates = distinctDate(stamps)
    for i in range(len(dates)):
        datemap[int(dates[i])] = i
    print('***************************')
    print(dates)
    #获取名称
    names = list(datas.keys())
    for i in range(len(names)):
        namemap[names[i]] = i
    print('***************************')
    print(names)
    print(namemap)

    #获取rng_sv
    for i in range(len(names)):
        samples = datas[names[i]]._lst 
        rng_sv.append([0] * len(samples))
        for j in range(len(samples)):
            score = samples[j]._score
            rng_sv[i][j] = score
    print(rng_sv)

    #初始化dashboard
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global CENTER_X
    global MAXNLE
    global BORDERX_INPUTBOX

    CENTER_X = SCREEN_WIDTH / 2
    MAXLEN = SCREEN_WIDTH * 0.4
    BORDERY_INPUTBOX = SCREEN_HEIGHT - 130

    ds._inputboxswithbutton = inputBoxWithButton(
        ["排名", "开始", "结束", "确定"],
        ["50", str(dates[-1]), str(dates[-1])],
        [SCREEN_WIDTH - BORDERX_INPUTBOX, SCREEN_WIDTH - BORDERX_INPUTBOX, SCREEN_WIDTH - BORDERX_INPUTBOX, (SCREEN_WIDTH - BORDERX_INPUTBOX) + INPUTBOXWIDTH + 10],
        [BORDERY_INPUTBOX, BORDERY_INPUTBOX + INPUTBOXHEIGHT + 10, BORDERY_INPUTBOX + 2 * (INPUTBOXHEIGHT + 10), BORDERY_INPUTBOX]
    )
    ds._speedcontrol = speedControl(SCREEN_WIDTH - BORDERX_INPUTBOX, BORDERY_INPUTBOX -20)

    
    while True:
        draw()
    


if __name__ == "__main__":
    #sector = argv[1]
    sector = "电气设备"
    innerDraw(sector)