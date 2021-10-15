
import pygame
import os
import sys
import functions

class Button():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.textx = 0
        self.texty = 0
        self.text = ""
        self.textcol = (0, 0, 0)
        self.font = pygame.font.SysFont('Calibri', 34 )
        self.image = pygame.image.load(os.path.join('images','GUI','Button1.png'))
        self.screen = ""
        self.onclick = ""
    def render(self, screen, gameinfo):
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        screen.blit(self.image, (self.x, self.y))
        buttonText = self.font.render(self.text, False,
                                     self.textcol)
        screen.blit(buttonText, (self.x + self.textx, self.y + self.texty))
    def onClick(self, gameinfo, myship, enemyships, spacestations, music):
        if self.onclick == "startgame":
            functions.startGame(gameinfo, myship, enemyships, spacestations, music)
        if self.onclick == "exit":
            sys.exit()
        if self.onclick == "warpclick":
            if gameinfo.selectedstation == None: return
            myship.autostate = "warp_rot"
            myship.warping = True
            myship.startWarpRot(spacestations[gameinfo.selectedstation])
            gameinfo.screen = "game"
        if self.onclick == "creditsclick":
            gameinfo.screen = "credits"
        if self.onclick == "creditsbackclick":
            gameinfo.screen = "mainmenu"


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
        self.angle = 0


class Music():
    def __init__(self):
        self.file = None

class Sound():
    def __init__(self):
        self.file = None
        self.mixer = None

class Shield():
    def __init__(self):
        self.maxcharge = 100
        self.charge = 100

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
        self.buttons = []

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