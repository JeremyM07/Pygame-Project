import pygame
from UntitledFighterGamefighter import Fighter

pygame.init()

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

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Untitled Fighter Game")


# defining menu font  
MenuFont = pygame.font.SysFont('Corbel',35) 
#render menu font
text1 = MenuFont.render('Start Game' , True , WHITE)
text2 = MenuFont.render('Options' , True , WHITE)
text3 = MenuFont.render('Quit' , True , WHITE)
#menu buttons y pos
starttextY = (screen_height/2)-150
optionsY = starttextY+75
quitY = optionsY+75

menuColor1 = BLACK
menuColor2 = BLACK
menuColor3 = BLACK
menuColor4 = BLACK



#define game variables
MainMenu = False
startBattle = False
battleDone = False
restart = False
returnMenu = False
options = False
charSelect = False
P1Picked = False
P2Picked = False
shinobiPicked = False
samuraiPicked = False
CPU = False

#define fighter variables
Shinobi_Size = 128 #size of animation image in pixels
ShinobiScale = 3 #scaling up image size to be visible
ShinobiOffset = [48, 78] #offsetting original blitted image to be on the ground
ShinobiData = [Shinobi_Size, ShinobiScale, ShinobiOffset]
Samurai_size = 128
SamuraiScale = 3
SamuraiOffset = [52, 78]
SamuraiData = [Samurai_size, SamuraiScale, SamuraiOffset] 




#load background - from: https://wallpapercave.com/landscape-pixel-art-wallpapers
bg_image = pygame.image.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Images\\ImageBG.jpg").convert_alpha()

#load sprite sheets - from: https://craftpix.net/freebies/free-shinobi-sprites-pixel-art/
shinobi_spritesheet = pygame.image.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Images\\spritesheet (1).png").convert_alpha()
#shinobi_attacksheet = pygame.image.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Images\\ShinobiAttackSheet.png").convert_alpha()
samurai_spritesheet = pygame.image.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Images\\samuraisheet.png").convert_alpha()

#num of animation steps (Idle,Run,Jump, Attack1(disabled), Attack2, Attack3, Hurt, Dead(disabled))
shinobi_Animationsteps = (6,8,10,6,3,4,6,3)
#shinobi_attacksteps = (4,4,3)
samurai_Animationsteps = (6,8,12,6,4,4,5,3)


#create instances of fighters
P1 = Fighter(200,450, False, ShinobiData, shinobi_spritesheet, shinobi_Animationsteps, True)
P2 = Fighter(700,450,True, SamuraiData, samurai_spritesheet, samurai_Animationsteps, False)


#draw menu buttons + box around it
def drawStart():
    global MainMenu; MainMenu = True
    global menuColor1
    global menuColor2
    global menuColor3
    global menuColor4
    pygame.draw.rect(screen,menuColor1,(screen_width/2-80,starttextY,158,40))
    screen.blit(text1 , (screen_width/2-80,starttextY))
    pygame.draw.rect(screen,menuColor2,(screen_width/2-80,optionsY,158,40))
    screen.blit(text2 , (screen_width/2-80,optionsY))
    pygame.draw.rect(screen,menuColor3,(screen_width/2-80,quitY,158,40))
    screen.blit(text3 , (screen_width/2-80,quitY))

    #if mouse hovers over buttons, they are highlighted
    if (screen_width/2)-95 <= mouse[0] <= (screen_width/2)+85 and starttextY <= mouse[1] <= starttextY+48:
        menuColor1 = BLUE
    else:
        menuColor1 = BLACK
    if (screen_width/2)-95 <= mouse[0] <= (screen_width/2)+85 and optionsY <= mouse[1] <= optionsY+48:
        menuColor2 = BLUE
    else:
        menuColor2 = BLACK
    if (screen_width/2)-95 <= mouse[0] <= (screen_width/2)+85 and quitY <= mouse[1] <= quitY+48:
        menuColor3 = BLUE
    else:
        menuColor3 = BLACK

portraitY = 200
def charPortraits():
    global menuColor1
    global menuColor2
    global menuColor3
    global menuColor4
    global portraitY
    global P2Picked
    global P1Picked
    portraitWidth, portraitHeight = 125, 175
    P1.update_action(0)
    P2.update_action(0)
    P1image = pygame.transform.flip(P1.image, False, False)
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


    


#bg draw function
def drawBG():
    scaled_bg = pygame.transform.scale(bg_image,(screen_width,screen_height))
    screen.blit(scaled_bg,(0,0))

#define health bar function
def drawHealth(health,x,y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x-5,y-5, 410,40))
    pygame.draw.rect(screen, RED, (x,y,400,30))
    pygame.draw.rect(screen, GREEN, (x,y,400*ratio,30))




firstLaunch = True

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#game loop
done = False
while not done:


    #events + game logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        #logic
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (screen_width/2)-95 <= mouse[0] <= (screen_width/2)+85 and starttextY <= mouse[1] <= starttextY+48:#pressed start game
                if startBattle:#check if game already started
                    pass
                elif MainMenu:
                    charSelect = True
                    MainMenu = False
                    menuColor1 = BLACK
            
            elif (screen_width/2)-95 <= mouse[0] <= (screen_width/2)+85 and quitY <= mouse[1] <= quitY+50:#PRESSED QUIT
                if MainMenu: #CHECKS IF ON MAIN MENU SCREEN
                    done = True 
            
    
                 
            if 50 <= mouse[0] <= 180 and portraitY <= mouse[1] <= portraitY+180:
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
                

            if 250 <= mouse[0] <= 380 and portraitY <= mouse[1] <= portraitY+180:
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


            if 650 <= mouse[0] <= 780 and portraitY <= mouse[1] <= portraitY+180:
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

            if 850 <= mouse[0] <= 980 and portraitY <= mouse[1] <= portraitY+180:
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
            if P1Picked and P2Picked:
                charSelect = False
                if menuColor2 == GREEN or menuColor3 == GREEN:
                    P1 = Fighter(200,450,False, SamuraiData, samurai_spritesheet, samurai_Animationsteps, True)
                    P2 = Fighter(700,450, True, ShinobiData, shinobi_spritesheet, shinobi_Animationsteps, False)
                startBattle = True
 
                
    if firstLaunch:
        MainMenu = True
        firstLaunch = False

    mouse = pygame.mouse.get_pos()  
    #drawing code --------

    #draw bg
    drawBG()

    if MainMenu:
        #draw menu text
        drawStart()


    
    if charSelect:
        charPortraits()




    if startBattle:

        #draw health bar
        drawHealth(P1.health,20,20)
        drawHealth(P2.health,580,20)

        #move fighter
        P1.move(screen_width, screen_height, screen, P2)
        P2.move(screen_width, screen_height, screen, P1)

        #update fighters
        P1.update()
        P2.update()
        #draw fighters
        P1.draw(screen)
        P2.draw(screen)





    


    


    #update display
    pygame.display.flip()

    #60 frames per second
    clock.tick(60)




#exit pygame
pygame.quit()
