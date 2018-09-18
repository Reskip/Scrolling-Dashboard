import pygame

class speedControl(object):
    def __init__(self, posx, posy, screen):
        self._speed = 5.0
        self._posx = posx
        self._posy = posy
        self._width = 120
        self._height = 3
        self._state = 0 #是否正被拖动
        self._color = (200, 200, 200)
        self._screen = screen
    
    def show(self):
        font = pygame.font.Font('lib/SimHei.ttf', 18)
        name = font.render("速度: ", True, self._color)
        self._screen.blit(name, (self._posx - 50, self._posy - 8))
        pygame.draw.rect(self._screen, (200, 200, 200),
                [self._posx, self._posy - self._height / 2, self._width, self._height], 0)
        pygame.draw.rect(self._screen, (255,140,0),
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
