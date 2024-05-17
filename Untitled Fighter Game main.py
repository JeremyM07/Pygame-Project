import pygame
from UntitledFighterGamefighter import Fighter

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)

# defining menu font  
MenuFont = pygame.font.SysFont('Corbel',35) 
#render menu font
text = MenuFont.render('Start Game' , True , WHITE)  
#draw box around start text
def drawStart():
    pygame.draw.rect(screen,GREEN,(screen_width/2-80,textYpos,160,40))
#define game start
gameStart = False

#define fighter variables
#Player 1
Shinobi_Size = 128 #size of animation image in pixels
ShinobiScale = 3 #scaling up image size to be visible
ShinobiOffset = [48, 78] #offsetting original blitted image to be on the ground
ShinobiData = [Shinobi_Size, ShinobiScale, ShinobiOffset]
Samurai_size = 128
SamuraiScale = 3
SamuraiOffset = [52, 78]
SamuraiData = [Samurai_size, SamuraiScale, SamuraiOffset]

#game window
screen_width = 1000
screen_height = 600 

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Untitled Fighter Game")
#menu y pos
textYpos = screen_height/2

#load background - from: https://wallpapercave.com/landscape-pixel-art-wallpapers
bg_image = pygame.image.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Images\\ImageBG.jpg").convert_alpha()

#load sprite sheets - from: https://craftpix.net/freebies/free-shinobi-sprites-pixel-art/
shinobi_spritesheet = pygame.image.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Images\\spritesheet (1).png").convert_alpha()
samurai_spritesheet = pygame.image.load("C:\\Users\\MatinaJ\\OneDrive - Dulwich College\\Desktop\\Untitled Fighter Game\\Images\\samuraisheet.png").convert_alpha()

#num of animation steps (Idle,Run,Jump, Attack1, Attack2, Attack3, Hurt, Dead)
shinobi_Animationsteps = [6,8,10,6,3,4,3,3]
samurai_Animationsteps = [6,8,12,6,4,3,2,3]
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

#create instances of fighters
P1 = Fighter(200,450, False, ShinobiData, shinobi_spritesheet, shinobi_Animationsteps, True)
P2 = Fighter(700,450,True, SamuraiData, samurai_spritesheet, samurai_Animationsteps, False)


# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#game loop
done = False
while not done:


    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
             if screen_width/2-80 <= mouse[0] <= screen_width/2+100 and screen_height/2 <= mouse[1] <= screen_height/2+40:
                textYpos += 900
                gameStart = True
                 


        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_q or event.key == pygame.K_e:
        #         if P1.attacking:
        #             P1.attacking = False

                


    mouse = pygame.mouse.get_pos()  
    #drawing code --------
            
    #draw bg
    drawBG()

    if gameStart:
        #draw health bar
        drawHealth(P1.health,20,20)
        drawHealth(P2.health,580,20)

        #move fighter
        P1.move(screen_width, screen_height, screen, P2)
        P2.move(screen_width, screen_height, screen, P1)

        #update fighters
        P1.update()
        P2.update()
        #draw fightersd
        P1.draw(screen)
        P2.draw(screen)
    #draw menu text
    drawStart()
    screen.blit(text , (screen_width/2-80,textYpos))
    


    


    #update display
    pygame.display.flip()

    #60 frames per second
    clock.tick(60)




#exit pygame
pygame.quit()
