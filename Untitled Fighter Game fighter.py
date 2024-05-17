import pygame

class Fighter():
    def __init__(self,x,y, flip, data, sprite_sheet, animationsteps, Player1):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animationlist = self.load_images(sprite_sheet, animationsteps)
        self.rect = pygame.Rect((x,y,80,150))
        self.vel_y = 0 
        self.running = False
        self.action = 0 #0=idle, 1=run, 2=jump, 3=attack1, 4=attack2, 5=attack3, 6=hit, 7=dead
        self.frame_index = 0
        self.image = self.animationlist[self.action][self.frame_index]
        self.currentFrame = 0
        self.updateTime = pygame.time.get_ticks()
        self.jump = False
        self.attacking = False
        self.attacktype = 0
        self.hit = False
        self.health = 100
        self.player = Player1 #boolean, player 1 uses WASD, player 2 uses arrow keys

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255,255,0), self.rect) - Removes yellow hitbox of player
        surface.blit(img,(self.rect.x - (self.offset[0]*self.image_scale),self.rect.y - (self.offset[1] * self.image_scale)))
    
    def load_images(self, sprite_sheet, animationsteps):
            runningtotal = 0
            animationlist = []
            for y, animation in enumerate(animationsteps):
                temp_img_list = []
                for x in range(animation):
                    if runningtotal > 0:
                        temp_img = sprite_sheet.subsurface(runningtotal+(x*self.size),0,self.size,self.size)
                    else:
                        temp_img = sprite_sheet.subsurface(x*self.size,0,self.size,self.size)
                    temp_img_list.append(pygame.transform.scale(temp_img, (self.size *self.image_scale, self.size*self.image_scale)))
                    if x == animation - 1:
                        runningtotal += x*self.size
                animationlist.append(temp_img_list)
            return animationlist

    def move(self, screen_width, screen_height, surface, target):
        speed = 15
        gravity = 1.4
        dx = 0 #positive = going forward, negative = going backwards
        dy = 0
        self.running = False
        self.attacktype = 0
        

        #get keypress
        key = pygame.key.get_pressed()

        #check if attacking to postpone other actions
        if not self.attacking:
            #If player is player 1
            if self.player:
            

                #movement key pressed
                if key[pygame.K_a]:
                    dx = -speed # change in speed becomes negative, moves char backwards
                    self.running = True
                if key[pygame.K_d]:
                    dx = speed
                    self.running = True
                #jumping
                if key[pygame.K_w] and not self.jump:
                    self.vel_y = -30 #adding weight to char, brings char downwards 
                    self.jump = True
                
                #attack
                if key[pygame.K_q] or key[pygame.K_e] or key[pygame.K_r]:
                    self.attack(surface, target)
                    self.attacking = True

                    #determine attack type used
                    if key[pygame.K_q]:
                        self.attacktype = 3
                    if key[pygame.K_e]:
                        self.attacktype = 4
                    if key[pygame.K_r]:
                        self.attacktype = 5
            #If player is player 2
            if not self.player:
                 #movement key pressed
                if key[pygame.K_LEFT]:
                    dx = -speed # change in speed becomes negative, moves char backwards
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = speed
                    self.running = True
                #jumping
                if key[pygame.K_UP] and not self.jump:
                    self.vel_y = -30 #adding weight to char, brings char downwards 
                    self.jump = True
                
                #attack
                if key[pygame.K_b] or key[pygame.K_n] or key[pygame.K_m]:
                    self.attack(surface, target)
                    self.attacking = True

                    #determine attack type used
                    if key[pygame.K_b]:
                        self.attacktype = 3
                    if key[pygame.K_n]:
                        self.attacktype = 4
                    if key[pygame.K_m]:
                        self.attacktype = 5

        #gravity
        self.vel_y += gravity
        #update y coordinate
        dy += self.vel_y
        
        #check player on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 0:
            self.vel_y = 0
            self.jump = False
            dy = (screen_height - 0) - self.rect.bottom


        #ensure player faces each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
        
        #update player position
        self.rect.x += dx
        self.rect.y += dy
    

    #animation updates
    def update(self):
        #check action player is performing
        if self.hit:
            self.update_action(3)
        if self.attacking:
            if self.attacktype == 3:
                self.update_action(5)
            if self.attacktype == 4:
                self.update_action(6)
            if self.attacktype == 5:
                self.update_action(7)
       
        if self.jump:
            self.update_action(2)#jump
        elif self.running:
            self.update_action(1)#run
        else:
            self.update_action(0)#idle




        animation_cooldown = 90 #miliseconds of which animation frame is shown, determines how fast animations are executed 
        if self.attacktype == 3:
            self.action = 5
            self.frame_index = 0
            self.updateTime = pygame.time.get_ticks()
            animation_cooldown = 600
        if self.attacktype == 4:
            self.action = 6
            self.frame_index = 0
            self.updateTime = pygame.time.get_ticks()
            animation_cooldown = 600
            
        if self.attacktype == 5:
            self.action = 7
            self.frame_index = 0
            self.updateTime = pygame.time.get_ticks()
            animation_cooldown = 600

        if self.hit:
            self.action = 6
            self.frame_index = 0
            self.updateTime = pygame.time.get_ticks()
            self.hit = False
            self.attacking = False

        self.image = self.animationlist[self.action][self.frame_index]#gets correct frame to display
        #check if enough time has passed to move on to next frame
        if pygame.time.get_ticks() - self.updateTime > animation_cooldown:
            self.frame_index += 1 #next frame
            self.updateTime = pygame.time.get_ticks()#restart timer
        #check if animation finished
        if self.frame_index >= len(self.animationlist[self.action]):#if the animation has reached its last frame, animation stops
            if self.attacking:
                self.attacking = False

            self.frame_index = 0
            #check if attack executed
            if self.action == 6:
              self.attacking = False
            if self.action == 7:
              self.attacking = False
            if self.action == 8:
              self.attacking = False
        




    def attack(self, surface, target):
        self.attacking = True
        attackingRect = pygame.Rect(self.rect.centerx - (2*self.rect.width*self.flip), self.rect.y, 2*self.rect.width, self.rect.height)
        if attackingRect.colliderect(target.rect):
            target.health -= 6.5 #the damage players receive from attacks
            target.hit = True
        #pygame.draw.rect(surface,(0, 255, 0), attackingRect) #- shows the area which damage can occur to other player



    def update_action(self, newAction):

        #check if new action is different to previous
        if newAction != self.action:
            self.action = newAction

            #update animation settings
            self.frame_index = 0 
            self.updateTime = pygame.time.get_ticks()
