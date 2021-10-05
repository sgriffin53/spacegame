
import pygame

class Animation():
    def __init__(self):
        self.type = None
        self.starttime = 0
        self.endtime = 0
        self.duration = 0
        self.startpos = 0
        self.endpos = 0
        self.colour = (255, 0, 0)
        self.targettype = None
        self.targetship = None
        self.firer = None
        self.target = None


class Music():
    def __init__(self):
        self.file = None

class Sound():
    def __init__(self):
        self.file = None
        self.mixer = None


class Weapon():
    def __init__(self):
        self.type = None
        self.duration = None
        self.chargetime = 0
        self.lastfired = 0
        self.range = 0

class GameInfo():
    def __init__(self):
        self.timefactor = 1
        self.redalert = False
        self.alive = True
        self.lastdied = 0
        self.myfont = pygame.font.SysFont('Fixedsys', 22)
        self.dir_label_font = pygame.font.SysFont('Courier', 12)
        self.map_title_font = pygame.font.SysFont('Calibri', 34 )
        self.screen = "game"
        self.mapstars = []
        self.selectedstation = None

class Point():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0

class FrameInfo():
    def __init__(self):
        self.firingphasers = False
        self.phaserstart = 0
        self.enemyexploding = False
        self.explodestart = 0