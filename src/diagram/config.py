#_*_coding:utf-8_*_
import pygame
#import win32api
class Config(object):
    def __init__(self):
        self.SCREEN_WIDTH = 1366
        self.SCREEN_HEIGHT = 768
        self.CENTER_X = int(self.SCREEN_WIDTH / 2)
        self.CENTER_Y = int(self.SCREEN_HEIGHT / 2)
        self.BORDER_X_LEFT = 100
        self.BORDER_X_RIGHT = 100
        self.BORDER_Y_TOP = 100
        self.BORDER_Y_DOWN = 100

        self.POINT_X_LEFT = int(self.SCREEN_WIDTH * 0.618)

        self.TITLE = "Diagram"
        self.BGCOLOR = (0, 0, 0)

        self.POINTCOLOR = (130, 166, 245)
        self.LINECOLOR = (159, 240, 72)
        self.POINTRADIO = 6
        self.BLINGRADIO = 50
        self.BLINGSPEED = 0.01
        self.POINTLINE_WIDTH = 3
        self.LINE_SAMPLE_RATE = 5

        self.FLOATSPEED = 0.2
        self.SCORESPEED = 0.2

        self.RANDSRATE = 1

        self.AUXLINE_COLOR = (100, 100, 100)
        self.AUXLINE_INTERVAL_DATE = [3600]
        self.AUXLINE_WIDTH_DATE = [2]
        self.AUXLINE_INTERVAL_SCOR = [100, 200]
        self.AUXLINE_WIDTH_SCOR = [2, 3]

        self.BOX_MOV_RATIO = 0.3
        self.MID_MOV_SPEED = 0.01

        self.TIME_SPEED = 20.0
        self.TIMECOLOR = (240, 240, 240)
        self.DATE_WIDTH = 10000
        self.TOP = 10

        self.CONFIG = pygame.HWSURFACE | pygame.DOUBLEBUF# | pygame.FULLSCREEN

    def setScreenSize(self, width, height):
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height

        self.CENTER_X = int(self.SCREEN_WIDTH / 2)
        self.CENTER_Y = int(self.SCREEN_HEIGHT / 2)
        self.POINT_X_LEFT = int(self.SCREEN_WIDTH * 0.618)

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Config, "_instance"):
            Config._instance = Config(*args, **kwargs)
        return Config._instance