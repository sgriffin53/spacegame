import pygame
import sys

def detectKeyPresses(event_get, fullscreen, alt_pressed, enter_pressed, myship, enemyships, gameinfo, animations, sounds):
    for event in event_get:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
            if not fullscreen:
                screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode([width, height])
            fullscreen = not fullscreen
        if event.type == pygame.KEYDOWN:

            if (event.key == pygame.K_RALT or event.key == pygame.K_LALT):
                alt_pressed = True
            if event.key == pygame.K_RETURN:
                enter_pressed = True
            if gameinfo.alive:
                if event.key == pygame.K_t:
                    myship.nextTarget(enemyships)
                if event.key == pygame.K_c:
                    myship.closestTarget(enemyships, gameinfo)
                if event.key == pygame.K_r:
                    gameinfo.redalert = not gameinfo.redalert
                    if gameinfo.redalert == True:
                        gameinfo.timefactor = 0.5
                    else:
                        gameinfo.timefactor = 1
                if event.key == pygame.K_y:
                    myship.attackerTarget()
                if event.key == pygame.K_SPACE:
                   if myship.targeted != None:
                        myship.fireNextWeapon(enemyships, animations, sounds)
        # set alt and enter flags if the keys are pressed
    if alt_pressed and enter_pressed: # full screen with alt+enter
        if not fullscreen:
            screen = pygame.display.set_mode([width, height], pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode([width, height])
        fullscreen = not fullscreen

    keys = pygame.key.get_pressed()  # checking pressed keys

    # unset alt and enter flags if they're not pressed

    if not keys[pygame.K_RALT] and not keys[pygame.K_LALT]:
        alt_pressed = False
    if not keys[pygame.K_RETURN]:
        enter_pressed = False
    if gameinfo.alive:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            myship.rotaccel = -120
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            myship.rotaccel = 120
        else:
            myship.rotaccel = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            myship.accel = 250
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            myship.accel = -250
        else:
            myship.accel = 0
    if keys[pygame.K_ESCAPE]:
        sys.exit()
    if keys[pygame.K_SPACE]:
        pass
        #if myship.targeted != None:
         #   frameinfo.firingphasers = True
          #  frameinfo.phaserstart = time.time()