import pygame, random

class Fighter():
    def __init__(self,x,y, flip, data, sprite_sheet, animationsteps, Player1,CPU):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animationlist = self.load_images(sprite_sheet, animationsteps)
        self.rect = pygame.Rect((x,y,80,150))
        self.vel_y = 0 
        self.vel_x = 0
        self.knockFriction = 0
        self.running = False
        self.action = 0 #0=idle, 1=run, 2=jump, 3=attack1, 4=attack2, 5=attack3, 6=hit, 7=dead 
        self.frame_index = 0
        self.image = self.animationlist[self.action][self.frame_index]
        self.currentFrame = 0
        self.updateTime = pygame.time.get_ticks()
        self.attack_cooldown = 0
        self.cooldown_timer = 500
        self.jump = False
        self.attacking = False
        self.attacktype = 0
        self.hit = False
        self.health = 100
        self.dead = False
        self.player = Player1 #boolean, player 1 uses WASD, player 2 uses arrow keys
        self.CPU = CPU

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
        knock_x = 0
        randAttack = random.randint(0,1)
        randJump = random.randint(0,5)
        attackingRect = pygame.Rect(self.rect.centerx - (2*self.rect.width*self.flip), self.rect.y, 2*self.rect.width, self.rect.height)

        
        

        #get key pressed on keyboard
        key = pygame.key.get_pressed()
        if not self.dead:
        #check if attacking to postpone other actions
            if self.CPU:

                if not target.dead:

                    if not self.attacking:
                        
                        if self.player or not self.player:
                            
                            #if CPU can attack player
                            if abs(target.rect.centerx - self.rect.centerx) < 35:
                                self.attack(surface,target)
                                self.attacking = True
                                if random.randint(0,1) == 0:
                                    self.attack_type = 4
                                else:
                                    self.attack_type = 5
                            
                            #if player is in the air, CPU jumps
                            if random.randint(0,45)==7:
                                if self.rect.bottom + dy > screen_height - 0 and not self.dead:
                                    self.vel_y = 0
                                    self.jump = False
                                    dy = (screen_height - 0) - self.rect.bottom
                                else:
                                    self.vel_y = -30
                                    self.jump = True
                            #CPU chases player
                            if target.rect.centerx > self.rect.centerx:
                                dx = speed-5
                                self.running = True
                            elif target.rect.centerx < self.rect.centerx:
                                dx = -speed + 5
                                self.running = True

            else:
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
                            self.vel_y = -30 #makes player jump up 
                            self.jump = True
                        
                        #attack
                        if key[pygame.K_e] or key[pygame.K_r]:
                            self.attack(surface, target)
                            self.attacking = True

                            #determine attack type used
                            # if key[pygame.K_q]:
                            #     self.attacktype = 3
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
                            self.vel_y = -30 #makes player jump up
                            self.jump = True
                        
                        #attack
                        if key[pygame.K_n] or key[pygame.K_m]:
                            self.attack(surface, target)
                            self.attacking = True

                            #determine attack type used
                            # if key[pygame.K_b]:
                            #     self.attacktype = 3
                            if key[pygame.K_n]:
                                self.attacktype = 4
                            if key[pygame.K_m]:
                                self.attacktype = 5

        #gravity
        self.vel_y += gravity
        #update y coordinate
        dy += self.vel_y

        if self.hit:
            if not self.flip:
                self.vel_x = -self.knockFriction
                    
                if target.attacktype == 5:
                    self.vel_x += self.vel_x-20
                dx += self.vel_x
                self.knockFriction -= 1


            else:
                
                self.vel_x = self.knockFriction
                if target.attacktype == 5:
                    self.vel_x += self.vel_x+20
                dx += self.vel_x
                self.knockFriction -= 1

        if self.knockFriction <= 0.25:
                self.knockFriction = 0
                self.vel_x = 0
                
        
        #check player on screen
        if self.rect.left + dx < 0 and not self.dead:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width and not self.dead:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 0 and not self.dead:
            self.vel_y = 0
            self.jump = False
            dy = (screen_height - 0) - self.rect.bottom


        #ensure player faces each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
        
        #update player position when not dead
        if not self.dead:
            self.rect.x += dx
            self.rect.y += dy
        #knock out animation, inspired by Super Smash Bros
        elif self.dead:
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



    
        

    def restoreHealth(self):
        self.dead = False
        self.health = 100

#animation updates
    def update(self):
        if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
        if self.health<= 0:
            self.dead = True
            self.health = 0.1 
        if self.hit:
            self.knockFriction = 10
            self.update_action(7)
            
        elif self.attacking:
                if self.attacktype == 3:
                    self.update_action(3)
                elif self.attacktype == 4:
                    self.update_action(4)
                elif self.attacktype == 5:
                    self.update_action(5)
                self.attack_cooldown += self.cooldown_timer // (1000/60)
        elif self.jump:
            self.update_action(2)
        elif self.running:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 60
        if self.attacking:
            animation_cooldown = 125

        if pygame.time.get_ticks() - self.updateTime > animation_cooldown:
            self.frame_index += 1
            self.updateTime = pygame.time.get_ticks()
        if self.frame_index >= len(self.animationlist[self.action])-1:
            self.frame_index = 0
            if self.attacking:
                self.attacking = False
                self.attack_type = 0
            if self.hit:
                self.hit = False
                self.attacking = False
                
        self.image = self.animationlist[self.action][self.frame_index]
        




    def attack(self, surface, target):
        self.attacking = True
        attackingRect = pygame.Rect(self.rect.centerx - (2*self.rect.width*self.flip), self.rect.y, 2*self.rect.width, self.rect.height)
        if attackingRect.colliderect(target.rect):
            target.health -= 6.5 #the damage players receive from attacks
            target.hit = True
            if target.flip:
                target.vel_y -= 20
                # target.vel_x = 1 * 10
                # target.rect.x += target.vel_x
            else:
                target.vel_y -= 20
                # target.vel_x = -1 * 10
                # target.rect.x += target.vel_x

        #pygame.draw.rect(surface,(0, 255, 0), attackingRect) #- shows the area which damage can occur to other player



    def update_action(self, newAction):

        #check if new action is different to previous
        if newAction != self.action:
            self.action = newAction

            #update animation settings
            self.frame_index = 0 
            self.updateTime = pygame.time.get_ticks()
