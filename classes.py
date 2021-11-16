
import pygame
import os
import sys
import functions

class Resolution():
    def __init__(self, index):
        self.width = 0
        self.height = 0
        self.index = index
        if index == 0:
            self.width = 800
            self.height = 600
            self.buttonfont = pygame.font.SysFont('Calibri', 21)
            self.smallbuttonfont = pygame.font.SysFont('Calibri', 16)
            self.headerfont = pygame.font.SysFont('Calibri', 40)
            self.normalfont = pygame.font.SysFont('Calibri', 18)
        elif index == 1:
            self.width = 1280
            self.height = 1024
            self.buttonfont = pygame.font.SysFont('Calibri', 34)
            self.smallbuttonfont = pygame.font.SysFont('Calibri', 26)
            self.headerfont = pygame.font.SysFont('Calibri', 65)
            self.normalfont = pygame.font.SysFont('Calibri', 28)
        elif index == 2:
            self.width = 1280
            self.height = 720
            self.buttonfont = pygame.font.SysFont('Calibri', 34)
            self.smallbuttonfont = pygame.font.SysFont('Calibri', 23)
            self.headerfont = pygame.font.SysFont('Calibri', 62)
            self.normalfont = pygame.font.SysFont('Calibri', 26)
        elif index == 3:
            self.width = 1366
            self.height = 768
            self.buttonfont = pygame.font.SysFont('Calibri', 36)
            self.smallbuttonfont = pygame.font.SysFont('Calibri', 23)
            self.headerfont = pygame.font.SysFont('Calibri', 54)
            self.normalfont = pygame.font.SysFont('Calibri', 30)
        elif index == 4:
            self.width = 2560
            self.height = 1440
            self.buttonfont = pygame.font.SysFont('Calibri', 68)
            self.smallbuttonfont = pygame.font.SysFont('Calibri', 46)
            self.headerfont = pygame.font.SysFont('Calibri', 84)
            self.normalfont = pygame.font.SysFont('Calibri', 56)


class Button():
    def __init__(self, x , y, width, height, textx, texty, text, textcol, screen, onclick, font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.textx = textx
        self.texty = texty
        self.text = text
        self.textcol = textcol
        self.font = font
        self.image = pygame.image.load(os.path.join('images','GUI','Button1.png'))
        self.screen = screen
        self.onclick = onclick
        self.visible = True
    def render(self, screen, gameinfo):
        scaled_width = self.width * (gameinfo.width / gameinfo.nativewidth)
        scaled_height = self.height * (gameinfo.height / gameinfo.nativeheight)
        scaled_x = self.x * (gameinfo.width / gameinfo.nativewidth)
        scaled_y = self.y * (gameinfo.height / gameinfo.nativeheight)
        scaled_textx = self.textx * (gameinfo.width / gameinfo.nativewidth)
        scaled_texty = self.texty * (gameinfo.height / gameinfo.nativeheight)
        newimg = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        screen.blit(newimg, (scaled_x, scaled_y))
        buttonText = self.font.render(self.text, False,
                                     self.textcol)
        screen.blit(buttonText, (scaled_x + scaled_textx, scaled_y + scaled_texty))
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
        if self.onclick == "repairclick":
            myship.repair(gameinfo)
        if self.onclick == "stationbackclick":
            gameinfo.messages[0].visible = False
            gameinfo.screen = "game"
        if self.onclick == "upgradeclick":
            gameinfo.screen = "upgrademenu"
        if self.onclick == "upgradebackclick":
            gameinfo.screen = "stationmenu"
        if self.onclick == "upgradeshieldsclick":
            gameinfo.shieldsel = myship.shields[0].classnum
            gameinfo.screen = "shieldsupgrademenu"
        if self.onclick == "shieldsupgradebackclick":
            gameinfo.messages[1].visible = False
            gameinfo.screen = "upgrademenu"
        if self.onclick == "shieldselectionleft":
            if gameinfo.shieldsel == None:
                gameinfo.shieldsel = myship.shields[0].classnum
            if gameinfo.shieldsel > 1:
                gameinfo.shieldsel -= 1
        if self.onclick == "shieldselectionright":
            if gameinfo.shieldsel <= 9:
                gameinfo.shieldsel += 1
        if self.onclick == "shieldsupgradeclick":
            gameinfo.messages[1].visible = True
            gameinfo.messages[1].message = "Shields upgraded."
            currentvalue = myship.shields[0].cost
            truecost = gameinfo.allshields[gameinfo.shieldsel - 1].cost - currentvalue
            currentshield = myship.shields[0].classnum
            shieldstring = "shield-c" + str(gameinfo.shieldsel)
            if currentshield > gameinfo.shieldsel:
                gameinfo.messages[1].message = "Shields downgraded."
            for i in range(4):
                myship.shields[i] = Shield(shieldstring)
            gameinfo.credits -= truecost

class Message():
    def __init__(self, x, y, message, screen, font):
        self.x = x
        self.y = y
        self.message = message
        self.visible = False
        self.screen = screen
        self.font = font

class Animation():
    def __init__(self):
        self.type = None
        self.starttime = 0
        self.endtime = 0
        self.duration = 0
        self.startpos = 0
        self.endpos = [0, 0]
        self.colour = (0, 255, 0)
        self.targettype = None
        self.targetship = None
        self.firer = None
        self.target = None
        self.angle = 0
        self.damage = 0
        self.classnum = 0
        self.range = 0
        self.hitpoint = []
        self.hitship = None
        self.hit = False
        self.shielddown = False
        self.missed = False
        self.x = 0
        self.y = 0
        self.velocity = 0
        self.points = [] # for flux ray
        self.t = 0
        self.offset = 0
        self.imgrot = 0
        self.hashit = False
        self.hitships = []

class Music():
    def __init__(self):
        self.file = None

class Sound():
    def __init__(self):
        self.file = None
        self.mixer = None

class ShipShield():
    def __init__(self):
        self.maxcharge = 100
        self.charge = 100

class Shield():
    def __init__(self, type):
        if type == "shield-c1":
            self.maxcharge = 100
            self.charge = 100
            self.classnum = 1
            self.fullname = "Shield (Class 1)"
            self.cost = 500
        elif type == "shield-c2":
            self.maxcharge = 250
            self.charge = 250
            self.classnum = 2
            self.fullname = "Shield (Class 2)"
            self.cost = 1500
        elif type == "shield-c3":
            self.maxcharge = 350
            self.charge = 350
            self.classnum = 3
            self.fullname = "Shield (Class 3)"
            self.cost = 2500
        elif type == "shield-c4":
            self.maxcharge = 500
            self.charge = 500
            self.classnum = 4
            self.fullname = "Shield (Class 4)"
            self.cost = 5000
        elif type == "shield-c5":
            self.maxcharge = 650
            self.charge = 650
            self.classnum = 5
            self.fullname = "Shield (Class 5)"
            self.cost = 15000
        elif type == "shield-c6":
            self.maxcharge = 800
            self.charge = 800
            self.classnum = 2
            self.fullname = "Shield (Class 6)"
            self.cost = 30000
        elif type == "shield-c7":
            self.maxcharge = 1000
            self.charge = 1000
            self.classnum = 7
            self.fullname = "Shield (Class 7)"
            self.cost = 50000
        elif type == "shield-c8":
            self.maxcharge = 1200
            self.charge = 1200
            self.classnum = 8
            self.fullname = "Shield (Class 8)"
            self.cost = 65000
        elif type == "shield-c9":
            self.maxcharge = 1500
            self.charge = 1500
            self.classnum = 9
            self.fullname = "Shield (Class 9)"
            self.cost = 80000
        elif type == "shield-c10":
            self.maxcharge = 2000
            self.charge = 2000
            self.classnum = 10
            self.fullname = "Shield (Class 10)"
            self.cost = 125000


class Weapon():
    def __init__(self, fulltype):
        self.fulltype = fulltype
        self.velocity = 200
        self.damage = 0
        self.type = None
        self.classnum = 1
        self.fullname = "None"
        self.duration = 0
        self.chargetime = 0
        self.lastfired = 0
        self.range = 0
        self.velocity = 1500
        if fulltype == "particlebeam-c1":
            self.damage = 40
            self.type = "particlebeam"
            self.classnum = 1
            self.fullname = "Particle Beam (Class 1)"
            self.duration = 0.5
            self.chargetime = 1.5
            self.lastfired = 0
            self.range = 1600
            self.velocity = 500
        if fulltype == "radialburst-c1":
            self.damage = 20
            self.type = "radialburst"
            self.classnum = 1
            self.fullname = "Radial Burst (Class 1)"
            self.duration = 0.5
            self.chargetime = 1.5
            self.lastfired = 0
            self.range = 600
            self.velocity = 500
        if fulltype == "disruptor-c1":
            self.damage = 35
            self.type = "disruptor"
            self.classnum = 1
            self.fullname = "Disruptor (Class 1)"
            self.duration = 0.5
            self.chargetime = 1.5
            self.lastfired = 0
            self.range = 600
            self.velocity = 1500
        if fulltype == "fluxray-c1":
            self.damage = 20
            self.type = "fluxray"
            self.classnum = 1
            self.fullname = "Flux Ray (Class 1)"
            self.duration = 0.5
            self.chargetime = 1.5
            self.lastfired = 0
            self.range = 600
            self.velocity = 1500
        if fulltype == "fluxray-c2":
            self.damage = 60
            self.type = "fluxray"
            self.classnum = 2
            self.fullname = "Flux Ray (Class 2)"
            self.duration = 0.5
            self.chargetime = 1.5
            self.lastfired = 0
            self.range = 600
            self.velocity = 1500
        if fulltype == "fluxray-c3":
            self.damage = 6000
            self.type = "fluxray"
            self.classnum = 2
            self.fullname = "Flux Ray (Class 3)"
            self.duration = 0.5
            self.chargetime = 1.5
            self.lastfired = 0
            self.range = 600
            self.velocity = 1500
        if fulltype == "torpedo-c1":
            self.damage = 20
            self.type = "torpedo"
            self.classnum = 1
            self.fullname = "Torpedo (Class 1)"
            self.duration = 5
            self.chargetime = 1
            self.lastfired = 0
            self.range = 600
            self.velocity = 800
        elif fulltype == "torpedo-c2":
            self.damage = 35
            self.type = "torpedo"
            self.classnum = 2
            self.fullname = "Torpedo (Class 2)"
            self.duration = 5
            self.chargetime = 3
            self.lastfired = 0
            self.range = 600
            self.velocity = 500
        elif fulltype == "bullet-c1":
            self.damage = 1
            self.type = "bullet"
            self.classnum = 1
            self.fullname = "Bullet (Class 1)"
            self.duration = 2
            self.chargetime = 0.05
            self.lastfired = 0
            self.range = 600
            self.velocity = 1500
        elif fulltype == "laser-c1":
            self.damage = 10
            self.type = "laser"
            self.classnum = 1
            self.fullname = "Laser (Class 1)"
            self.duration = 0.2
            self.chargetime = 1
            self.lastfired = 0
            self.range = 600
        elif fulltype == "laser-c2":
            self.damage = 20
            self.type = "laser"
            self.classnum = 2
            self.fullname = "Laser (Class 2)"
            self.duration = 0.3
            self.chargetime = 1.2
            self.lastfired = 0
            self.range = 600

class ShipWeapon():
    def __init__(self):
        self.type = None
        self.duration = None
        self.chargetime = 0
        self.lastfired = 0
        self.range = 0
        self.damage = 0
        self.fullname = ""

class GameInfo():
    def __init__(self):
        self.timefactor = 1
        self.redalert = False
        self.alive = True
        self.lastdied = 0
        self.myfont = pygame.font.SysFont('Fixedsys', 22)
        self.dir_label_font = pygame.font.SysFont('Courier', 12)
        self.map_title_font = pygame.font.SysFont('Calibri', 34 )
        self.gamemessage_font = pygame.font.SysFont('Calibri', 34)
        self.screen = "game"
        self.mapstars = []
        self.selectedstation = None
        self.buttons = []
        self.messages = []
        self.credits = 0
        self.gamemessage = ""
        self.gamemessagedisplayed = 0
        self.checkships = []
        self.nativeheight = 0
        self.nativewidth = 0
        self.fullscreen = False
        self.resolutions = []
        self.resolution = 0
        self.resindex = 0
        self.shieldsel = 1
        self.allshields = []

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