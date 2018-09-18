#_*_coding:utf-8_*_
'''
Author  : Reskip
Date    : 2018.8.7

Main process of ranking graph
'''
import sys
import threading
import random
import pygame
import time
from pygame.locals import *
import pygame.gfxdraw
from config import *
from rank import *
from ctrl import *

cfg = Config.instance()
pygame.init()

#cfg.setScreenSize(pygame.display.Info().current_w, pygame.display.Info().current_h)
cfg.setScreenSize(1024, 768)
screen = pygame.display.set_mode([cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT], cfg.CONFIG)
pygame.display.set_caption(cfg.TITLE)
font = pygame.font.Font('lib/SimHei.ttf', 18)
workList = list()
spc = speedControl(100, 50, screen)

if __name__ == "__main__":
    sector = sys.argv[1]

    print(sector)
    #time.sleep(5)

    db= dashboard([screen, font])
    db.loadData(sector)
    workList = [db.update, db.show, spc.show]
    bef = time.time()

    while True:
        while(time.time() - bef < 0.04):
            pass
        print(time.time() - bef)
        bef = time.time()

        screen.fill(cfg.BGCOLOR)

        for fun in workList:
            fun()

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            spc.checkMouseMove(event)
            cfg.TIME_SPEED = spc._speed * 4