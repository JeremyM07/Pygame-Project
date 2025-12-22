import pygame, random

class Fighter():
    def __init__(self,x,y,flip, data, sprite_sheet, animationsteps, Player1,CPU, ability_data):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animationlist = self.load_images(sprite_sheet, animationsteps)
        self.rect = pygame.Rect(x,y,80,150)
        self.running = False
        self.action = 0 #0=idle, 1=run, 2=jump, 3=attack1, 4=attack2, 5=hit, 6=dead 
        self.frame_index = 0
        self.image = self.animationlist[self.action][self.frame_index]
        self.updateTime = pygame.time.get_ticks()
        self.player = Player1
        self.CPU = CPU
        self.jump = False
        self.attacking = False
        self.attacktype = 0
        self.hit = False
        self.dead = False
        self.vel_y = 0
        self.vel_x = 0
        self.health = 100 
        self.knockFriction = 0
        self.useAbility = False
        self.ability_charge = 0
        self.ability_cooldown = False
        self.ability = Ability(
            x=self.rect.centerx,
            y=self.rect.centery,
            data=ability_data[0],
            animationsteps=ability_data[1],
            spritesheet=ability_data[2],
            flip=flip,
        )




    def load_images(self, sprite_sheet, animationsteps):
            runningtotal = 0
            animationlist = [] #List of lists of all character animations in the spritesheet
            for y, animation in enumerate(animationsteps):
                temp_img_list = [] #List for one animation
                for x in range(animation):
                    if runningtotal > 0:#If the first frame has been already cut, then go to next frame
                        temp_img = sprite_sheet.subsurface(runningtotal+(x*self.size),0,self.size,self.size)
                    else:
                        temp_img = sprite_sheet.subsurface(x*self.size,0,self.size,self.size)
                    temp_img_list.append(pygame.transform.scale(temp_img, (self.size *self.image_scale, self.size*self.image_scale)))#Scale up frame and add to temp_list
                    if x == animation - 1:
                        runningtotal += x*self.size
                animationlist.append(temp_img_list)
            return animationlist



    def move(self, screen_width, screen_height, target, surface):
        self.running = False
        speed = 15
        gravity = 1.4
        dx = 0 #positive = going forward, negative = going backwards
        dy = 0
        knock_x = 0


        #get key pressed on keyboard
        key = pygame.key.get_pressed()

        if self.CPU: 

            if not self.attacking:

                                #if CPU can attack player
                if abs(target.rect.centerx - self.rect.centerx) < 45 and not self.dead and not target.dead:
                    self.attack(surface,target)
                    self.attacking = True
                    if random.randint(0,1) == 0:
                        self.attack_type = 4
                    else:
                        self.attack_type = 5

                if self.checkAbilityBar:
                    self.activate_ability()


                #if player is in the air, CPU jumps
                if random.randint(0,45)==7:
                    if self.rect.bottom + dy > screen_height - 0 and not self.dead and not target.dead:
                        self.vel_y = 0
                        self.jump = False
                        dy = (screen_height - 0) - self.rect.bottom
                    else:
                        self.vel_y = -30
                        self.jump = True
                #CPU chases player
                if target.rect.centerx+10 > self.rect.centerx and not self.dead and not target.dead:
                    dx = speed-5
                    self.running = True
                elif target.rect.centerx+10 < self.rect.centerx and not self.dead and not target.dead:
                    dx = -speed + 5
                    self.running = True
        else:
            if self.player:

                if not self.attacking:
    
                    if key[pygame.K_a]:
                        dx = -speed # change in speed becomes negative, moves char backwards
                        self.running = True
                    if key[pygame.K_d]:
                        dx = speed
                        self.running = True 
                    if key[pygame.K_w] and not self.jump:
                        self.vel_y = -30 #makes player jump up 
                        self.jump = True

                    #attack
                    if key[pygame.K_e] or key[pygame.K_r] or key[pygame.K_q]:
                        self.attack(surface, target)
                        self.attacking = True

                        #determine attack type used
                        if key[pygame.K_e]:
                            self.attacktype = 4
                        if key[pygame.K_r]:
                            self.attacktype = 5
                        if key[pygame.K_q] and self.ability_charge >= 1:
                            self.activate_ability()
            else:
                if not self.attacking:    
                    if key[pygame.K_LEFT]:
                        dx = -speed # change in speed becomes negative, moves char backwards
                        self.running = True
                    if key[pygame.K_RIGHT]:
                        dx = speed
                        self.running = True
                    if key[pygame.K_UP] and not self.jump:
                        self.vel_y = -30 #makes player jump up 
                        self.jump = True

                        #attack
                    if key[pygame.K_n] or key[pygame.K_m] or key[pygame.K_b]:
                        self.attack(surface, target)
                        self.attacking = True

                        #determine attack type used
                        if key[pygame.K_n]:
                            self.attacktype = 4
                        if key[pygame.K_m]:
                            self.attacktype = 5
                        if key[pygame.K_b] and self.ability_charge >= 1:
                            self.activate_ability()

        
        #update y coordinate
        self.vel_y += gravity
        dy += self.vel_y

        if self.hit:
            if not self.flip:
                self.vel_x = -self.knockFriction
                    
                if target.attacktype == 5: #extra knockback for attack 2
                    self.vel_x += self.vel_x-20
                dx += self.vel_x
                self.knockFriction -= 1


            else:
                
                self.vel_x = self.knockFriction
                if target.attacktype == 5:
                    self.vel_x += self.vel_x+20
                dx += self.vel_x
                self.knockFriction -= 1

        if self.knockFriction <= 0.25: #reset knockback and velocity to 0 when knockback is negligible
                self.knockFriction = 0
                self.vel_x = 0

        #check player on screen
        if self.rect.left + dx < 0 and not self.dead: #if the speed and position of character beyond left screen border
            dx = -self.rect.left #limit character speed to left border
        if self.rect.right + dx > screen_width and not self.dead:  #if the speed and position of character beyond right screen border
            dx = screen_width - self.rect.right #limit character speed to right border
        if self.rect.bottom + dy > screen_height and not self.dead:
            self.vel_y = 0
            self.jump = False #character can jump again
            dy = screen_height - self.rect.bottom #limit change in y
        if self.rect.top + dy < 0:
            dy = -self.rect.top
        

        
        #ensure player faces each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        
        #update player position
        if not self.dead:
            self.rect.x += dx
            self.rect.y += dy
        else:
            self.rect.y -= knock_x**2-5*knock_x - 20
            if self.player:
                if self.flip:
                    knock_x = 10
                    self.rect.x+=knock_x
                else:
                    knock_x = 10
                    self.rect.x-=knock_x

            if not self.player:
                if self.flip:
                    knock_x = 10
                    self.rect.x+=knock_x
                else:
                    knock_x = 10
                    self.rect.x-=knock_x     

    def activate_ability(self):
        if self.checkAbilityBar():  # Use instance-based charge
            self.ability.used = True
            self.ability.active = True
            self.ability.frame_index = 0
            self.ability_charge = 0  # Reset charge
            # Position ability relative to fighter
            
            # if self.flip:
            #     self.ability.rect.x = self.rect.x - 10
            # else:
            #     self.ability.rect.x = self.rect.x + 10
            # self.ability.rect.y = self.rect.centery
    
        
    def checkAbilityBar(self):
        return self.ability_charge >= 1  # True when full
    
    def updateAbilityPos(self):
        if not self.ability.active:
            self.ability.rect.x = self.rect.x
            self.ability.rect.y = self.rect.y
    def restoreHealth(self):
        self.dead = False
        self.health = 100
    def resetPosition(self,x,y):
        self.rect = pygame.Rect((x,y,80,150))



    def draw(self, surface, colour):
        #pygame.draw.rect(surface, colour, self.rect)
        img = pygame.transform.flip(self.image, self.flip, False)

        surface.blit(img, (self.rect.x - (self.offset[0]*self.image_scale),self.rect.y - (self.offset[1] * self.image_scale)))


    def update(self, target, surface):
        self.updateAbilityPos()
        if self.ability.active:
            self.ability.draw(surface)
            self.ability.update(target)
            self.update_action(4)
        if self.health<= 0:
            self.dead = True
            self.health = 0.1 
        if self.hit:
            self.knockFriction = 10
            self.update_action(7)

        elif self.attacking:
                if self.attacktype == 4:
                    self.update_action(4)
                elif self.attacktype == 5:
                    self.update_action(5)
        elif self.jump:
            self.update_action(2)
        elif self.running:
            self.update_action(1)
        else:
            self.update_action(0)





        animation_cooldown = 60 #miliseconds until next 
        if self.attacking:
            animation_cooldown = 125 #cooldown is longer for attacks

        if pygame.time.get_ticks() - self.updateTime > animation_cooldown: # if time passed has exceeded animation period, go to next frame
            self.frame_index += 1
            self.updateTime = pygame.time.get_ticks()
        if self.frame_index >= len(self.animationlist[self.action])-1: #if last frame has been reached, go back to first frame
            self.frame_index = 0
            if self.attacking:
                self.attacking = False #reset attacking status
                self.attack_type = 0 #reset attacktype
            if self.hit:
                self.hit = False
                self.attacking = False
                
        self.image = self.animationlist[self.action][self.frame_index] #current frame to be drawn


    def attack(self, surface, target):
        self.attacking = True
        attackingRect = pygame.Rect(self.rect.centerx - (2*self.rect.width*self.flip), self.rect.y, 2*self.rect.width, self.rect.height)
        if attackingRect.colliderect(target.rect) and not target.hit:
            target.health -= 6.5 #the damage players receive from attacks
            target.hit = True
            if target.flip:
                target.vel_y -= 20
            else:
                target.vel_y -= 20

            
        #pygame.draw.rect(surface,(0, 255, 0), attackingRect) #- shows the area which damage can occur to other player



    def update_action(self, newAction):

        #check if new action is different to previous
        if newAction != self.action:
            self.action = newAction

            #update animation settings
            self.frame_index = 0 
            self.updateTime = pygame.time.get_ticks()

class Ability():
    def __init__(self, x, y, data, animationsteps, spritesheet, flip, debug=False):
        self.size = data[0]  
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animationlist = self.load_images(spritesheet, animationsteps)
        frame_width = spritesheet.get_width() // animationsteps
        self.rect = pygame.Rect(
                x - (self.offset[0] * self.image_scale),  # apply X offset
                y - (self.offset[1] * self.image_scale),  # apply Y offset
                frame_width * self.image_scale - 100,  # use frame width
                spritesheet.get_height() * self.image_scale   # use frame height
            )
        self.frame_index = 0
        self.image = self.animationlist[self.frame_index]
        self.updateTime = pygame.time.get_ticks()
        self.abilityBar = 0
        self.active = False
        self.cooldown = 7000 
        self.debug = debug  # debug colour hitbox
        self.cycles = 0
        self.knocked = False
        self.used = False

    def load_images(self, sprite_sheet, animationsteps):
        #Validate input
        sheet_width, sheet_height = sprite_sheet.get_size()
        frame_width = sheet_width // animationsteps
        frame_height = sheet_height
        animationlist = []

        #Extract frames from the sprite sheet
        for frame_index in range(animationsteps):
            frame_x = frame_index * frame_width
            temp_img = sprite_sheet.subsurface((frame_x, 0, frame_width, frame_height))
            scaled_img = pygame.transform.scale(
                temp_img, (frame_width * self.image_scale, frame_height * self.image_scale)
            )
            animationlist.append(scaled_img)

        return animationlist

    def draw(self, surface):
        img = pygame.transform.flip(self.image, not self.flip, True)
        if self.debug:
            pygame.draw.rect(surface, (255, 255, 0), self.rect)  #Debug hitbox
        surface.blit(
            img, 
            (self.rect.x - (self.offset[0] * self.image_scale), 
             self.rect.y - (self.offset[1] * self.image_scale))
        )
        # if self.active:
        #     if not self.flip:
        #         self.rect.x += 20
        #     else:
        #         self.rect.x -= 20


    def update(self, target):
        #Update animation only if active
        if self.active:
            animation_cooldown = 80  #Time between frames (milliseconds)
            if pygame.time.get_ticks() - self.updateTime > animation_cooldown:
                self.frame_index += 1
                self.updateTime = pygame.time.get_ticks()

            #Reset to the first frame if the animation ends
            if self.frame_index >= len(self.animationlist)-1:
                self.cycles += 1
                self.frame_index = 0
            
            if self.cycles > 5:
                self.cycles = 0
                self.active = False
                self.used = False

            self.image = self.animationlist[self.frame_index]

            if target.rect.centerx > self.rect.centerx:
                self.rect.x += 20
            else:
                self.rect.x -= 20

            if self.rect.colliderect(target.rect):
                target.health -= 16.5#damage of ability
                target.hit = True
                self.active = False
                target.knocked = True
                self.used = False

            if self.knocked:#same knockback code as in fighter class
                if not target.flip:
                    target.vel_x = -target.knockFriction-20
                    target.rect.x += target.vel_x
                    target.knockFriction -= 1


                else:
                
                    target.vel_x = target.knockFriction+20
                    target.rect.x += target.vel_x
                    target.knockFriction -= 1

        if target.knockFriction <= 0.25: #reset knockback and velocity to 0 when knockback is negligible
                target.knockFriction = 0
                target.vel_x = 0
                target.knocked = False
                
pygame.init()
pygame.mixer.init()


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)
BLUE = (0,0,200)

#game window
screen_width = 1000
screen_height = 600 
screen = pygame.display.set_mode( ( screen_width, screen_height ) )

# defining menu font  
TitleFont = pygame.font.SysFont('Corbel',70,True)
MenuFont = pygame.font.SysFont('Corbel',35 )
#render menu font
text1 = MenuFont.render('Start Game' , True , WHITE)
text2 = MenuFont.render('Options' , True , WHITE)
text3 = MenuFont.render('Quit' , True , WHITE)
text4 = TitleFont.render('Untitled Fighter Game' , True , WHITE)
text5 = MenuFont.render('CPU' , True , WHITE)
text6 = MenuFont.render('Start Battle!' , True , WHITE)
text7 = MenuFont.render('P1 Wins!' , True , WHITE)
text8 = MenuFont.render('P2 Wins!' , True , WHITE)
text9 = MenuFont.render('Restart' , True , WHITE)
text10 = MenuFont.render('Main Menu' , True , WHITE)
text11 = MenuFont.render('Time ran out!', True, WHITE)
text12 = MenuFont.render('Its a Draw!' , True , WHITE)




#menu buttons y pos
starttextY = (screen_height/2) - 150
optionsY = starttextY + 75
quitY = optionsY + 75

menuColor1 = BLACK
menuColor2 = BLACK
menuColor3 = BLACK
menuColor4 = BLACK
menuColor5 = BLACK
menuColor6 = BLACK
menuColor7 = BLACK
menuColor8 = BLACK
menuColor9 = BLACK


#define game variables
MainMenu = False
firstLaunch = True
charSelect = False
startBattle = False
timerStart = False 
TimeOut = False
battleDone = False
musicPlaying = False
P1sound = False
P2Sound = False
MainMenuMusic = False
battleMusic = False
P1Picked = False
P2Picked = False
shinobiPicked = False
samuraiPicked = False
CPU1 = False
CPU2 = False
switchedChar = False
restart = False
#load music and sound effects
pygame.mixer.set_num_channels(10)

mainMusic = pygame.mixer.music.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Audio\\Main Menu Music.mp3")

punch1 = pygame.mixer.Sound("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Audio\\Punch 1.mp3")
punch2 = pygame.mixer.Sound("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Audio\\Punch 2.mp3")
punch_swing = pygame.mixer.Sound("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Audio\\Punch Swing.mp3")
sword1 = pygame.mixer.Sound("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Audio\\Sword Hit.mp3")
sword2 = pygame.mixer.Sound("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Audio\\Sword 2.mp3")
sword_swing = pygame.mixer.Sound("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Audio\\Sword swing.mp3")
ability_fire = pygame.mixer.Sound("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Audio\\Ability Shoot.mp3")
ability_hit = pygame.mixer.Sound("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Audio\\Ability Hit.mp3")

P1channelAttack = pygame.mixer.Channel(1)
P1channelSwing = pygame.mixer.Channel(2)

P2channelAttack = pygame.mixer.Channel(3)
P2channelSwing = pygame.mixer.Channel(4)

P1AbilityFly = pygame.mixer.Channel(6)
P2AbilityFly = pygame.mixer.Channel(5)

P1AbilityHit = pygame.mixer.Channel(8)
P2AbilityHit = pygame.mixer.Channel(7)


# fighter variables
Shinobi_Size = 128 #size of animation image in pixels
ShinobiScale = 3 #scaling up image size to be visible
ShinobiOffset = [48, 78] #offsetting original blitted image to be on the ground
ShinobiData = [Shinobi_Size, ShinobiScale, ShinobiOffset]
Samurai_size = 128
SamuraiScale = 3
SamuraiOffset = [52, 78]
SamuraiData = [Samurai_size, SamuraiScale, SamuraiOffset] 


#set the game window caption
pygame.display.set_caption("Untitled Fighter Game")

#load background - from: https://wallpapercave.com/landscape-pixel-art-wallpapers
bg_image = pygame.image.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Images\\ImageBG.jpg").convert_alpha()


#load sprite sheets - from: https://craftpix.net/freebies/free-shinobi-sprites-pixel-art/
shinobi_spritesheet = pygame.image.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Images\\spritesheet (1).png").convert_alpha()
#shinobi_attacksheet = pygame.image.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Images\\ShinobiAttackSheet.png").convert_alpha()
samurai_spritesheet = pygame.image.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Images\\samuraisheet.png").convert_alpha()



#red punch sprite sheet
redpunch_spritesheet = pygame.image.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Images\\Red Fire\\red_fire_projectile.png")

#num of animation steps (Idle,Run,Jump, Attack1, Attack2, Attack3, Hurt, Dead)
shinobi_Animationsteps = (6,8,10,6,3,4,6,3)

samurai_Animationsteps = (6,8,12,6,4,4,5,3)


ability_data = [(32,5,[25,20]), 4, redpunch_spritesheet]




#check punch sound
def AttackSound(P1,P2):
    key = pygame.key.get_pressed()
    if P1.attacking:
        if key[pygame.K_e] or key[pygame.K_r] or P1.attacktype == 4 or P1.attacktype == 5:
            if not P1channelSwing.get_busy():
                P1channelSwing.queue(punch_swing)
                P1channelSwing.play(punch_swing)
            if (key[pygame.K_e] or P1.attacktype == 4) and P2.hit:
                if not P1channelAttack.get_busy():
                    P1channelAttack.queue(punch1)
                    P1channelAttack.play(punch1)
            if (key[pygame.K_r] or P1.attacktype == 5) and P2.hit:
                if not P1channelAttack.get_busy():
                    P1channelAttack.queue(punch2)
                    P1channelAttack.play(punch2)
        if P1.ability.used and not P1AbilityFly.get_busy():
            P1AbilityFly.queue(ability_fire)
            P1AbilityFly.play(ability_fire)
    if P1.ability.rect.colliderect(P2.rect) and P1.ability.used and not P1AbilityHit.get_busy():
        P1AbilityHit.queue(ability_hit)
        P1AbilityHit.play(ability_hit)

    if P2.attacking:
        if  key[pygame.K_n] or key[pygame.K_m] or P2.attacktype == 4 or P2.attacktype == 5:
            if not P2channelSwing.get_busy():
                P2channelSwing.queue(sword_swing)
                P2channelSwing.play(sword_swing)
            if (key[pygame.K_n] or P2.attacktype == 4) and P1.hit:
                if not P2channelAttack.get_busy():
                    P2channelAttack.queue(sword1)
                    P2channelAttack.play(sword1)
            if (key[pygame.K_m] or P2.attacktype == 5) and P1.hit:
                if not P2channelAttack.get_busy():
                    P2channelAttack.queue(sword2)
                    P2channelAttack.play(sword2)
        if P2.ability.used and not P2AbilityFly.get_busy():
            P2AbilityFly.queue(ability_fire)
            P2AbilityFly.play(ability_fire)
    if P2.ability.rect.colliderect(P1.rect) and P2.ability.used and not P2AbilityHit.get_busy():
        P2AbilityHit.queue(ability_hit)
        P2AbilityHit.play(ability_hit)


 
#define background drawing function
scaled_bg = pygame.transform.scale(bg_image,(screen_width,screen_height))
def drawBG():
    global scaled_bg
    screen.blit(scaled_bg,(0,0)) #draws the image from the top left of the window




startTicks = pygame.time.get_ticks()

#draw timer function
def drawTimer():
    global startTicks
    global battleDone
    global TimeOut
    global timerStart
    global startBattle
    if not timerStart and startBattle: #when the battle starts, start the timer
        startTicks = pygame.time.get_ticks()
        timerStart = True
    if startBattle: #while the battle is ongoing, keep updating the value of seconds
        seconds = (pygame.time.get_ticks()-startTicks)//1000 

    if battleDone:
        seconds = 0
        del seconds
    if restart:
        seconds = 0
    if seconds > 45 and startBattle: # if the timer goes over 45 seconds, end the battle
        startTicks = pygame.time.get_ticks()
        battleDone = True
        TimeOut = True
        startBattle = False
        timerStart = False
    if not battleDone: #While the battle is ongoing, keep outputing seconds on screen
        timer = MenuFont.render(str(seconds), True, BLACK)
        screen.blit(timer, (screen_width/2 - 12, screen_height/50))

#define health bar function
def drawHealth(health,x,y):
    ratio = health / 100

    pygame.draw.rect(screen, WHITE, (x-5,y-5, 410,40))
    pygame.draw.rect(screen, RED, (x,y,400,30))
    pygame.draw.rect(screen, GREEN, (x,y,400*ratio,30))



#draw ability bar
def drawAbilityBar(x, y, charge):  #add charge parameter
    pygame.draw.rect(screen, WHITE, (x-5, y-5, 210, 40)) # Bar outline, increase visibility
    pygame.draw.rect(screen, BLUE, (x, y, 200 * charge, 30))  # use charge to control how much bar is filled







portraitY = 200
#character selection
def charPortraits():
    global menuColor1
    global menuColor2
    global menuColor3
    global menuColor4
    global menuColor5
    global menuColor6
    global menuColor7
    portraitWidth, portraitHeight = 125, 175
    global portraitY
    global P2
    global P1
    P1.update_action(0) #image for character button
    P2.update_action(0)
    P1image = pygame.transform.flip(P1.image, False, False) #image face each other
    P2image = pygame.transform.flip(P2.image, True, False)

    #left side
    portrait1 = pygame.transform.scale(P1image,(portraitWidth,portraitHeight))
    portrait2 = pygame.transform.scale(P2image,(portraitWidth,portraitHeight))
    pygame.draw.rect(screen,menuColor1,(50,200,portraitWidth,portraitHeight))
    pygame.draw.rect(screen,menuColor2,(250,200,portraitWidth,portraitHeight))
    screen.blit(portrait1,(50,portraitY))
    screen.blit(portrait2,(250,portraitY))
    #highlight buttons
    if not P1Picked:
        if 50 <= mouse[0] <= 180 and portraitY <= mouse[1] <= portraitY+180:
            menuColor1 = BLUE
        else:
            menuColor1 = BLACK
        if 250 <= mouse[0] <= 380 and portraitY <= mouse[1] <= portraitY+180:
            menuColor2 = BLUE
        else:
            menuColor2 = BLACK


    #right side
    portrait3 = pygame.transform.scale(P1image,(portraitWidth,portraitHeight))
    portrait4 = pygame.transform.scale(P2image,(portraitWidth,portraitHeight))
    pygame.draw.rect(screen,menuColor3,(650,200,portraitWidth,portraitHeight))
    pygame.draw.rect(screen,menuColor4,(850,200,portraitWidth,portraitHeight))
    screen.blit(portrait3,(650,portraitY))
    screen.blit(portrait4,(850,portraitY))
    if not P2Picked:
        if 650 <= mouse[0] <= 780 and portraitY <= mouse[1] <= portraitY+180:
            menuColor3 = BLUE
        else:
            menuColor3 = BLACK
        if 850 <= mouse[0] <= 980 and portraitY <= mouse[1] <= portraitY+180:
            menuColor4 = BLUE
        else:
            menuColor4 = BLACK
    #CPU Buttons
    pygame.draw.rect(screen,menuColor5,(125,450,175,50))
    screen.blit(text5,(140,460))
    pygame.draw.rect(screen,menuColor6,(725,447,175,50))
    screen.blit(text5,(740,457))
    if not CPU1:
        if 125 <= mouse[0] <= 300 and 450 <= mouse[1] <= 500:
            menuColor5 = BLUE
        else:
            menuColor5 = BLACK

    if not CPU2:
        if 725 <= mouse[0] <= 900 and 450 <= mouse[1] <= 500:
            menuColor6 = BLUE
        else:
            menuColor6 = BLACK

    #start battle button
    pygame.draw.rect(screen,menuColor7,(420,550,180,50))
    screen.blit(text6,(425,555))
    if 420 <= mouse[0] <= 600 and 550 <= mouse[1] <= 600:
        menuColor7 = BLUE
    else:
        menuColor7 = BLACK


#Win screen
def drawBattleDone(P1):
    global menuColor8
    global menuColor9

    if P1: #If P1 wins, print 'P1 wins'
        screen.blit(text7 , (screen_width/2-80,screen_height/2 - 80))
    else: #Else print 'P2 wins'
        screen.blit(text8 , (screen_width/2-80,screen_height/2 - 80))
    pygame.draw.rect(screen,menuColor8,(screen_width/2-80,screen_height/2,158,40))
    screen.blit(text9 , (screen_width/2-80,screen_height/2))
    pygame.draw.rect(screen,menuColor9,(screen_width/2-80,screen_height/2 + 50,158,40))
    screen.blit(text10 , (screen_width/2-80,screen_height/2 + 50))

    if (screen_width/2)-95 <= mouse[0] <= (screen_width/2)+85 and screen_height/2 <= mouse[1] <= screen_height/2 +48:#restart button area for highlight
        menuColor8 = BLUE
    else:
        menuColor8 = BLACK
    if (screen_width/2)-95 <= mouse[0] <= (screen_width/2)+85 and screen_height/2 + 50 <= mouse[1] <= screen_height/2 + 98:#main menu button area for highlight
        menuColor9 = BLUE
    else:
        menuColor9 = BLACK


#Time out screen
def drawTimeOut():
    global menuColor8
    global menuColor9
    if P1.health > P2.health:
        screen.blit(text7 , (screen_width/2-80,screen_height/2 - 80))
    elif P2.health > P1.health:
        screen.blit(text8 , (screen_width/2-80,screen_height/2 - 80))
    else:
        screen.blit(text12 , (screen_width/2-80,screen_height/2 - 80))


    screen.blit(text11 , (screen_width/2-80,screen_height/2 - 140))

    pygame.draw.rect(screen,menuColor8,(screen_width/2-80,screen_height/2,158,40))
    screen.blit(text9 , (screen_width/2-80,screen_height/2))
    pygame.draw.rect(screen,menuColor9,(screen_width/2-80,screen_height/2 + 50,158,40))
    screen.blit(text10 , (screen_width/2-80,screen_height/2 + 50))

    if (screen_width/2)-95 <= mouse[0] <= (screen_width/2)+85 and screen_height/2 <= mouse[1] <= screen_height/2 +48:
        menuColor8 = BLUE
    else:
        menuColor8 = BLACK
    if (screen_width/2)-95 <= mouse[0] <= (screen_width/2)+85 and screen_height/2 + 50 <= mouse[1] <= screen_height/2 + 98:
        menuColor9 = BLUE
    else:
        menuColor9 = BLACK



#draw menu buttons + box around it
def drawStart():
    global menuColor1
    global menuColor2
    global menuColor3
    screen.blit(text4, (screen_width/2-310,screen_height/2-250))
    pygame.draw.rect(screen,menuColor1,(screen_width/2-80,starttextY,158,40))
    screen.blit(text1 , (screen_width/2-80,starttextY))
    pygame.draw.rect(screen,menuColor2,(screen_width/2-80,optionsY,158,40))
    screen.blit(text2 , (screen_width/2-80,optionsY))
    pygame.draw.rect(screen,menuColor3,(screen_width/2-80,quitY,158,40))
    screen.blit(text3 , (screen_width/2-80,quitY))


    if (screen_width/2)-95 <= mouse[0] <= (screen_width/2)+85 and starttextY <= mouse[1] <= starttextY+40:
        menuColor1 = BLUE
    else:
        menuColor1 = BLACK
    if (screen_width/2)-95 <= mouse[0] <= (screen_width/2)+85 and optionsY <= mouse[1] <= optionsY+40:
        menuColor2 = BLUE
    else:
        menuColor2 = BLACK
    if (screen_width/2)-95 <= mouse[0] <= (screen_width/2)+85 and quitY <= mouse[1] <= quitY+40:
        menuColor3 = BLUE
    else:
        menuColor3 = BLACK

P1 = Fighter(200,450, False, ShinobiData, shinobi_spritesheet,shinobi_Animationsteps, True,CPU1, ability_data)
P2 = Fighter(700,450,True, SamuraiData, samurai_spritesheet, samurai_Animationsteps, False,CPU2, ability_data)


# Used to manage how fast the screen updates
clock = pygame.time.Clock()
#game loop
done = False
while not done:

    #get mouse position
    mouse = pygame.mouse.get_pos()


    #events + game logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        #logic
        if event.type == pygame.MOUSEBUTTONDOWN:

            if (screen_width/2)-100 <= mouse[0] <= (screen_width/2)+100 and starttextY <= mouse[1] <= starttextY+75:#pressed start game
                if startBattle:#check if game already started
                    pass
                elif MainMenu:
                    menuColor1 = BLACK
                    charSelect = True
                    MainMenu = False
                     

            if (screen_width/2)-95 <= mouse[0] <= (screen_width/2)+85 and quitY <= mouse[1] <= quitY+50:#PRESSED QUIT
                if MainMenu: #CHECKS IF ON MAIN MENU SCREEN
                    done = True


            if 50 <= mouse[0] <= 180 and portraitY <= mouse[1] <= portraitY+180: #Character 1 Button for Player 1(Shinobi)
                if charSelect:
                    if not P1Picked:
                        if not P2Picked:
                            shinobiPicked = True
                            P1Picked = True
                            menuColor1 = GREEN
                        elif P2Picked and not shinobiPicked:
                            shinobiPicked = True
                            P1Picked = True
                            menuColor1 = GREEN
                    else:
                        if not P2Picked:
                            shinobiPicked = False
                            P1Picked = False
                            menuColor1 = BLACK
                

            if 250 <= mouse[0] <= 380 and portraitY <= mouse[1] <= portraitY+180: #Character 2 Button for Player 1(Samurai)
                if charSelect:
                    if not P1Picked:
                        if not P2Picked:
                            samuraiPicked = True
                            P1Picked = True
                            menuColor2 = GREEN
                        elif P2Picked and not samuraiPicked:
                            samuraiPicked = True
                            P1Picked = True
                            menuColor2 = GREEN
                    else:
                        if not P2Picked:
                            samuraiPicked = False
                            P1Picked = False
                            menuColor1 = BLACK

            if 650 <= mouse[0] <= 780 and portraitY <= mouse[1] <= portraitY+180: #Character 1 Button for Player 2
                if charSelect:
                    if not P2Picked:
                        if not P1Picked:
                            shinobiPicked = True
                            P2Picked = True
                            menuColor3 = GREEN
                        elif P1Picked and not shinobiPicked:
                            shinobiPicked = True
                            P2Picked = True
                            menuColor3 = GREEN
                    else:
                        if not P1Picked:
                            shinobiPicked = False
                            P2Picked = False
                            menuColor1 = BLACK

            if 850 <= mouse[0] <= 980 and portraitY <= mouse[1] <= portraitY+180: #Character 2 Button for Player 2
                if charSelect:
                    if not P2Picked:
                        if not P1Picked:
                            samuraiPicked = True
                            P2Picked = True
                            menuColor4 = GREEN
                        elif P1Picked and not samuraiPicked:
                            samuraiPicked = True
                            P2Picked = True
                            menuColor4 = GREEN
                    else:
                        if not P1Picked:
                            samuraiPicked = False
                            P2Picked = False
                            menuColor1 = BLACK



            if 125 <= mouse[0] <= 300 and 450 <= mouse[1] <= 500:#player 1 CPU toggle
                if charSelect:
                    if not CPU1:
                        CPU1 = True
                        menuColor5 = GREEN
                    else:
                        CPU1 = False
                        menuColor5 = BLACK

            if 725 <= mouse[0] <= 900 and 450 <= mouse[1] <= 500:#player 2 CPU toggle
                if charSelect:
                    if not CPU2:
                        CPU2 = True
                        menuColor6 = GREEN
                    else:
                        CPU2 = False
                        menuColor6 = BLACK


            if 420 <= mouse[0] <= 600 and 550 <= mouse[1] <= 600:#start game after characters picked
                if P1Picked and P2Picked:
                    menuColor7 = GREEN
                    charSelect = False
                    if menuColor2 == GREEN or menuColor3 == GREEN:
                        del P1
                        del P2
                        P1 = Fighter(200,450,False, SamuraiData, samurai_spritesheet, samurai_Animationsteps, True,CPU1, ability_data)
                        P2 = Fighter(700,450, True, ShinobiData, shinobi_spritesheet, shinobi_Animationsteps, False,CPU2,ability_data)
                        switchedChar = True
                    else:
                        switchedChar = False
                    startBattle = True




            if (screen_width/2)-95 <= mouse[0] <= (screen_width/2)+85 and screen_height/2 <= mouse[1] <= screen_height/2 +48:#restart game
                if battleDone:
                    P1.restoreHealth()
                    P2.restoreHealth()
                    if P1.player:
                        P1.resetPosition(200,450)
                    else:
                        P1.resetPosition(700,450)
                    if P2.player:
                        P2.resetPosition(200,450)
                    else:
                        P2.resetPosition(700,450)
                    restart = True


            if (screen_width/2)-95 <= mouse[0] <= (screen_width/2)+85 and screen_height/2 + 50 <= mouse[1] <= screen_height/2 + 98:#return to menu
                if battleDone:
                    P1.restoreHealth()
                    P2.restoreHealth()
                    MainMenu = True
                    del P1
                    del P2
                    P1 = Fighter(200,450, False, ShinobiData, shinobi_spritesheet, shinobi_Animationsteps, True,CPU1,ability_data)
                    P2 = Fighter(700,450,True, SamuraiData, samurai_spritesheet, samurai_Animationsteps, False,CPU2, ability_data)
                    P1Picked = False
                    P2Picked = False
                    samuraiPicked = False
                    shinobiPicked = False
                    menuColor1,menuColor2,menuColor3,menuColor4,menuColor5,menuColor6,menuColor7,menuColor8,menuColor9 = BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK
                    battleDone = False



 
    #drawing code ----------------------
    if firstLaunch:
        MainMenu = True
        MainMenuMusic = True
        firstLaunch = False


    drawBG()



    if MainMenu:
        #draw start menu
        drawStart()

        if battleMusic:
            pygame.mixer.music.unload() 
            MainMenuMusic = True
            musicPlaying = False
            battleMusic = False

        if not musicPlaying and MainMenuMusic:
            mainMusic = pygame.mixer.music.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Audio\\Main Menu Music.mp3")
            pygame.mixer.music.set_volume(0.8) #set volume to 80%
            pygame.mixer.music.play(-1)#loop music      
            musicPlaying = True   

    if charSelect:
        charPortraits()

    

    if startBattle:
        if not switchedChar:
            AttackSound(P1,P2)
        else:
            AttackSound(P2,P1)
        if MainMenuMusic:
            pygame.mixer.music.unload()
            MainMenuMusic = False
            musicPlaying = False
            battleMusic = True
        
        if not musicPlaying and battleMusic:
            Musicbattle = pygame.mixer.music.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Audio\\Battle Music.mp3")
            pygame.mixer.music.set_volume(0.8) #set volume to 80%
            pygame.mixer.music.play(-1)#loop 
            startTicks = pygame.time.get_ticks()
            musicPlaying = True

        drawTimer()

        P1.draw(screen,YELLOW)
        P2.draw(screen,YELLOW)

        drawHealth(P1.health,20,20)
        drawHealth(P2.health,580,20)

        drawAbilityBar(20, 80, P1.ability_charge)  
        drawAbilityBar(580, 80, P2.ability_charge)

        
        P1.ability_charge = min(P1.ability_charge + 0.0025, 1)

        P2.ability_charge = min(P2.ability_charge + 0.0025, 1)

        P1.move(screen_width,screen_height, P2, screen)
        P2.move(screen_width,screen_height, P1, screen)

        P1.update(P2, screen)
        P2.update(P1, screen)


    if restart:
        drawTimer()
        startBattle = True
        battleDone = False
        restart = False
        timerStart = False
        P1.ability_charge = 0
        P2.ability_charge = 0

    if P1.dead or P2.dead:
        startBattle = False
        battleDone = True

    if battleDone:
        if P1.dead:
            drawBattleDone(False)
        elif P2.dead:
            drawBattleDone(True)
        elif TimeOut:
            drawTimeOut()

        P1.update(P2, screen)
        P2.update(P1, screen)

        P1.draw(screen, YELLOW)
        P2.draw(screen, YELLOW)

        # #move fighter
        
        P1.move(screen_width,screen_height, P2, screen)
        P2.move(screen_width,screen_height, P1, screen)

        drawHealth(P1.health,20,20)
        drawHealth(P2.health,580,20)


    #update display
    pygame.display.flip()

    #60 frames per second
    clock.tick(60)


#exit pygame
pygame.quit() 
