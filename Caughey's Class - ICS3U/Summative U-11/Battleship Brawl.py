#Kyle Button

#05/29/24

#Purpose: to create a program that will allow the player to control and move a ship and shoot enemy players aiming to reach the highest score possible.

#Current High Score -- 6570 - Round 19 --

#  -- Setting up actors and varibles --



#imports
import math
import pgzrun
import pygame
import random
import time

#window
WIDTH = 800
HEIGHT = 600

#homescreen background
homescreen = Actor("greybackground")

#play the game button
playbutton = Actor("playthegamebutton")

#background
background = Actor('background1')

#explosion for ship
explosion = Actor('shipexplosion')

#heart - full
full_heart = Actor('heart')
full_heart2 = Actor('heart')
full_heart3 = Actor('heart')

#heart - empty
empty_heart = Actor('heartempty')
empty_heart2 = Actor('heartempty')
empty_heart3 = Actor('heartempty')

#Player ship
ship = Actor('ship')
ship.pos = WIDTH / 2, HEIGHT / 2


#global variables
enemies_actors = []
bullets = []
enemy_bullets = []
score = 0
highScore = 0
lives = 3
bulletSpeed = 2
bulletSpeedbot = 1.1
maxBullets = 12
maxEnemies = 3
shiphealth = 2
damage = 1
enemySpeed = 2.2
ticks = 0
roundNumber = 1
enemiesKilled = 0
Gameover = False
hit = False
playGame = False
mainMenu = True



# -- Main Menu & Events --

#drawing main menu
def drawmainmenu():
    screen.clear()
    homescreen.draw()
    playbutton.pos = (400, 200)
    screen.draw.text(f"Battleship Brawl", (200, 60), fontsize=70, color="red")
    screen.draw.text(f"High Score: {highScore}", (240, 300), fontsize=70, color="red")
    screen.draw.text("Controls", (345, 400), fontsize=30, color="red")
    screen.draw.text("Press W A S D to move the ship around", (200, 430), fontsize=30, color="red")
    screen.draw.text("Use Arrow Keys to change the ships direction", (170, 460), fontsize=30, color="red")
    screen.draw.text("Press Space to fire!" , (295, 490), fontsize=30, color="red")
    playbutton.draw()
    

#function connected to main menu - touching play again button
def on_mouse_down(pos, button):
    global mainMenu, playGame
    if mainMenu and button == mouse.LEFT and playbutton.collidepoint(pos):
        mainMenu = False
        playGame = True
        screen.clear()


#next round
def nextRound():
    global roundNumber, enemySpeed, enemiesKilled, shiphealth
    if enemiesKilled >= maxEnemies:
        roundNumber += 1
        shiphealth = 5
        upgradeRound()
        enemySpeed += 0.3
        enemiesKilled = 0
        enemies_actors.clear()
        bullets.clear()
        enemy_bullets.clear()
        addEnemy()
        increaseMaxEnemies()


#rounds to upgrade ship
def upgradeRound():
    global roundNumber, lives, bulletSpeed, shiphealth, damage, enemies_actors

    addLives = Actor('addheart')
    addDamage = Actor('adddmg')
    addBulletSpeed = Actor('addbulletspeed')

    addLives.pos = (150, 400)
    addDamage.pos = (400, 400)
    addBulletSpeed.pos = (650, 400)

    if roundNumber in [4, 8, 12, 16]:
        enemies_actors.clear()
        if ship.colliderect(addLives):
            lives += 1
            addLives.pos = (0, 0)
            addDamage.pos = (0, 0)
            addBulletSpeed.pos = (-100, 0)
            roundNumber += 1



        if ship.colliderect(addDamage):
            damage += 1
            addLives.pos = (0, 0)
            addDamage.pos = (0, 0)
            addBulletSpeed.pos = (-100, 0)
            roundNumber += 1
            return damage



        if ship.colliderect(addBulletSpeed):
            bulletSpeed += 1
            addLives.pos = (0, 0)
            addDamage.pos = (0, 0)
            addBulletSpeed.pos = (-100, 0)
            roundNumber += 1



    addDamage.draw()
    addLives.draw()
    addBulletSpeed.draw()


#clear enemies and state gameover as true!
def gameOver():
    global lives, roundNumber, shiphealth, gameOver, Gameover
    if lives <= 0:
        enemies_actors.clear()
        enemy_bullets.clear()
        bullets.clear()
        Gameover = True
    return False


#play again (reset everything)
def playAgain():
    global Gameover, lives, roundNumber,shiphealth, gameOver, highScore, score, maxEnemies
    Gameover = False
    highScore = score 
    score = 0
    lives = 3
    roundNumber = 1
    shiphealth = 5
    maxEnemies = 3
    enemies_actors.clear()
    bullets.clear()
    enemy_bullets.clear()
    if ticks % 60 == 0:
        addEnemy()





#  -- Hearts For Player -- 

#drawing hearts
def drawHearts():
    full_heart = Actor('heart')
    full_heart2 = Actor('heart')
    full_heart3 = Actor('heart')
    full_heart.pos = (30, 30)
    full_heart2.pos = (85, 30)
    full_heart3.pos = (140, 30)

    if lives >= 3:
        full_heart3.image = "heart"
        full_heart2.image = "heart"
        full_heart.image = "heart"
    elif lives == 2:
        full_heart3.image = "heartempty"
        full_heart2.image = "heart"
        full_heart.image = "heart"
    elif lives == 1:
        full_heart3.image = "heartempty"
        full_heart2.image = "heartempty"
        full_heart.image = "heart"
    elif lives <= 0:
        full_heart3.image = "heartempty"
        full_heart2.image = "heartempty"
        full_heart.image = "heartempty"

    full_heart.draw()
    full_heart2.draw()
    full_heart3.draw()





#  -- Enemy Functions --

#adding enemy ships
def addEnemy():
    global enemiesKilled, lives
    while len(enemies_actors) < maxEnemies:
        whatKindofEnemy()
        
    nextRound()


# gather which type of enemy to add
def whatKindofEnemy():
    global enemies_actors
    #randomly decide what enemy to spawn and location
    what_enemy = random.randint(1, 4) 
    rany = random.randint(0, 600)
    ranx = random.randint(0, 800)
    
    #setting spawn distance from player
    distance = math.sqrt((ranx - ship.x)**2 + (rany - ship.y)**2)
    safe_distance = 150    #83 TO 86 was found online !!!


    if distance > safe_distance:

        #spawning enemy 1 (3/4 spawn rate)
        if what_enemy == 1 or what_enemy == 2 or what_enemy == 3:
            basic_enemy = Actor('enemyship1')
            basic_enemy.pos = (ranx, rany)
            if not ship.colliderect(basic_enemy):  
                enemies_actors.append(basic_enemy)
                
        #spawning enemy 2 (1/4 spawn rate)
        elif what_enemy == 4:
            shooting_enemy = Actor('enemyship2')
            shooting_enemy.pos = (ranx, rany)
            if not ship.colliderect(shooting_enemy):  
                enemies_actors.append(shooting_enemy)

        
#Moving the enemy ship towards player
def enemyMovement():
    global lives, gameOver, Gameover, forceField
    forceField = None
    for enemy in enemies_actors:
        angle = math.atan2(ship.y - enemy.y, ship.x - enemy.x)
        enemy.x += math.cos(angle) * enemySpeed
        enemy.y += math.sin(angle) * enemySpeed

    #if enemy bullets hit player ship
    for e in enemies_actors:
        if ship.colliderect(e):
            lives -= 1
            bullets.clear()
            enemy_bullets.clear()
            enemies_actors.remove(e)
            if gameOver():
                Gameover = True


#enemy shooting
def enemyShooting():
    global bulletSpeedbot, ship, bullets, e
    for e in enemies_actors:
        if isinstance(e, Actor) and e.image == "enemyship2":
            angletoship = math.atan2(ship.y - e.y, ship.x - e.x)
            bdx2 = bulletSpeedbot * math.cos(angletoship)
            bdy2 = bulletSpeedbot * math.sin(angletoship)
            fireBullet2(e.x, e.y, bdx2, bdy2)


#max enemies increasing per round
def increaseMaxEnemies():
    global maxEnemies
    maxEnemies = min(5, maxEnemies + 1)






#  -- Handling Firing Bullets -- 

#find bullet capacity and fire in direction of the ship using cauhey's fancy math
def fireBullet(posx, posy, dx, dy, theta):
    numBullets = len(bullets)
    if (numBullets < maxBullets):
        t = []
        b = Actor('gunbullet')
        b.angle = theta
        b.pos = posx, posy
        t.append(b)
        t.append(dx)
        t.append(dy)
        bullets.append(t)


#Fire bullet from enemy ship
def fireBullet2(x, y, dx, dy):
    if ticks%60 == 0:
        t1 = []
        b1 = Actor('gunbullet')
        b1.pos = x,y
        t1.append(b1)
        t1.append(dx)
        t1.append(dy)
        enemy_bullets.append(t1)


#Fire on space bar
def on_key_up(key):
    if key == keys.SPACE:
        shipDegrees = ship.angle + 90
        shipRadians = math.radians(shipDegrees)
        bdx = bulletSpeed * math.cos(shipRadians)
        bdy = bulletSpeed * math.sin(-shipRadians)
        fireBullet(ship.x, ship.y, bdx, bdy, shipDegrees)


#collison check for bullet to enemy ship & moving the bullets
def moveBullets():
    global shiphealth, enemiesKilled, hit, lives, score, damage

    #ship bullets
    for b in bullets[:]:
        bullet = b[0]
        movex = b[1]
        movey = b[2]
        nx = bullet.x + movex
        ny = bullet.y + movey

        #player bullets out of bounds
        if (nx < 0 or ny < 0 or nx > WIDTH or ny > HEIGHT):
            bullets.remove(b)
        else:
            b[0].pos = nx, ny

            #bullet collison with enemy
            for e in enemies_actors[:]: 
                if bullet.colliderect(e):
                    score += 10
                    shiphealth -= damage
                    bullets.remove(b)

                    #checking for dead enemy
                    if shiphealth <= 0 and isinstance(e, Actor):
                        enemies_actors.remove(e)
                        score += 50
                        enemiesKilled += 1
                        shiphealth = 5

    #enemy bullets
    for eb in enemy_bullets[:]:
        bullet = eb[0]
        movex = eb[1]
        movey = eb[2]
        nx = bullet.x + movex
        ny = bullet.y + movey
        
        #enemy bullet out of bounds
        if (nx < 0 or ny < 0 or nx > WIDTH or ny > HEIGHT):
            enemy_bullets.remove(eb)
        else:
            eb[0].pos = nx, ny

            #enemy bullet collison with player ship
            if bullet.colliderect(ship):
                enemy_bullets.remove(eb)
                lives -= 1
                gameOver()


#Drawing the bullets
def drawBullets():
    for b in bullets:
        b[0].draw()

    for b in enemy_bullets:
        b[0].draw()






#  -- Drawing & Updating Screen

#update the screen
def update():
    global ticks, Gameover, ship, playGame, mainMenu, lives 
    
    if mainMenu == True:
        drawmainmenu()
    
    
    if playGame == True:
        #timer in game
        ticks += 1
        

        #check if round == upgrade round
        upgradeRound()


        #wasd and arrow keys
        if keyboard.w:
            ship.y -= 2.2
        if keyboard.s:
            ship.y += 2.2
        if keyboard.a:
            ship.x -= 2.2
        if keyboard.d:
            ship.x += 2.2
        if keyboard.left:
            ship.angle += 3
        if keyboard.right:
            ship.angle += -3
    
    
        #barriers for screen
        if ship.right > WIDTH:
            ship.right = WIDTH
        if ship.left < 0:
            ship.left = 0
        if ship.bottom > HEIGHT:
            ship.bottom = HEIGHT
        if ship.top < 0:
            ship.top = 0


        #change actor of ship and start play again on death
        if Gameover == True:
            ship.image = "shipexplosion"
            if keyboard.RETURN:
                playAgain()
                ship.image = "ship"
            if keyboard.BACKSPACE:
                playAgain()
                ship.image = ('ship')
                playGame = False
                mainMenu = True
            return

    
        #fire bullets from shooting_ship
        enemyShooting()
    
        #move bullets
        moveBullets()
    
        #enemy movement 
        if ticks%5 == 0:      
            enemyMovement()
    
        #add enemies every two seconds
        if ticks%120 == 0:
            addEnemy()
    
        #checks if all enemies are killed to start next round
        if not enemies_actors:
            nextRound()


#draw the fuction onto the screen
def draw():
    global roundNumber, Gameover


#home screen
    if mainMenu == True:
        drawmainmenu()
 #if would you like to play == True

# game play
    if playGame == True:
        background.draw()
        drawHearts()
        numBullets = maxBullets - len(bullets)

        
        #text
        screen.draw.text(f"Round: {roundNumber}", (350, 10), color="orange", fontsize = 35)
        screen.draw.text(f"Bullets: {numBullets}", (650, 480), color="orange")
        screen.draw.text(f"Score: {score}", (650, 500), color="orange")
        screen.draw.text(f"High Score: {highScore}", (650, 520), color="orange")

        
        #text when game over is displayed
        if Gameover == True:
            screen.draw.text("Game Over - Press Enter to Play Again!", (210, 200), color="orange", fontsize = 30)
            screen.draw.text("Press 'BackSpace' to return to the menu", (220, 230), fontsize = 30, color="orange")
            screen.draw.text(f"Score: {score}", (340, 260), color="orange", fontsize = 30)
    
        #drawing ship & enemies
        ship.draw()
        for e in enemies_actors:
            e.draw()
    
        #drawing bullets
        drawBullets()

        if roundNumber in [4, 8, 12, 16]:
            upgradeRound()





#run the game
pgzrun.go()





#assets I snagged :)
#https://opengameart.org/content/purple-space-ship
#https://opengameart.org/content/spaceship-tutorial-0