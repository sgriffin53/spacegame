import functions

def objectCollisionDetection(object1, object2):
    '''
    obj1_centre_x = object1.x
    obj1_centre_y = object1.y
    obj2_centre_x = object2.x
    obj2_centre_y = object2.y
    dx = obj1_centre_x - obj2_centre_x
    dy = obj1_centre_y - obj2_centre_y
    dist = math.sqrt(dx * dx + dy * dy)
    '''
    dist = functions.distance(object1, object2)
    if dist < object1.radius + object2.radius:
        return True
    return False

def collisionDetection(myship, enemyships, spacestations):
    for enemyship in enemyships:
        for spacestation in spacestations:
            if objectCollisionDetection(enemyship, spacestation):
                enemyship.vel = 0
                enemyship.accel = 0
                enemyship.substate = enemyship.state
                enemyship.state = "leavestation_rot"
                enemyship.x = enemyship.lastx
                enemyship.y = enemyship.lasty
                enemyship.startLeaveStation_rot()
    if not myship.warping:
        for spacestation in spacestations:
            if objectCollisionDetection(myship, spacestation):
                myship.vel = 0
                myship.accel = 0
                myship.x = myship.lastx
                myship.y = myship.lasty
