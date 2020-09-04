"""Builds Enemy superclass"""
import pygame as py
import os as os
import random
import numpy as np

class Enemy(py.sprite.Sprite):
    def __init__(self, x, y):
        #Position, dimension and velocity of character
        self.width = 40
        self.height = 40
        self.vel = 2
        #Direction of walk
        self.left = False
        self.right = False
        self.down = False
        self.up = False
        self.walk = 0
        self.standing = True
        self.health = 100
        self.alive = True   
        self.damage = 10
        # Make our top-left corner the passed-in location; for wall collision
        self.image = py.Surface([55, 75])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y  
        #Visability
        self.visible = False
        
        # Call constructor from superclass
        super().__init__()
        
        
    def draw(self, win):
        """Animation for moving"""
        if not self.standing:
            if self.left:
                win.blit(self.load_left_pic[self.walk % 8], (self.rect.x, self.rect.y))
                self.walk += 1                
            elif self.right:
                win.blit(self.load_right_pic[self.walk % 8], (self.rect.x, self.rect.y))
                self.walk += 1                
            elif self.down:
                win.blit(self.load_down_pic[self.walk % 8], (self.rect.x, self.rect.y))
                self.walk += 1
            elif self.up:
                win.blit(self.load_up_pic[self.walk % 8], (self.rect.x, self.rect.y))
                self.walk += 1   
                
        else:
            if self.left:
                win.blit(self.load_left_pic[0], (self.rect.x, self.rect.y))
            elif self.right:    
                win.blit(self.load_right_pic[0], (self.rect.x, self.rect.y))
            elif self.down:    
                win.blit(self.load_down_pic[0], (self.rect.x, self.rect.y))              
            elif self.up:    
                win.blit(self.load_up_pic[0], (self.rect.x, self.rect.y))
            else:
                win.blit(self.load_standing_pic, (self.rect.x, self.rect.y))    
                
        #Health bar: red bar
        py.draw.rect(win, (255, 0, 0), \
        (self.rect.x + self.width // 2, self.rect.y - 0.2 * self.height, self.width, 5))
            
        #green bar decreaes with damage
        py.draw.rect(win, (0, 255, 0), \
        (self.rect.x + self.width // 2, self.rect.y - 0.2 * self.height, \
          self.health/100 * self.width, 5))                
           

    def move(self, player, xdim, ydim, current_room):
        """Orc follows player; needs player and xdim"""
        #Movement starts once door opens
        if current_room.door_open:
            self.visible = True
            #Should orc move in x or y direction?
            #Checks best move
            x_dist = abs(player.rect.x - self.rect.x)
            y_dist = abs(player.rect.y - self.rect.y)
            if x_dist > y_dist:             
                #Move left
                if self.rect.x > player.rect.x:
                    self.rect.x -= self.vel #move by velocity to left
                    self.left = True
                    self.right = False
                    self.up = False
                    self.down = False
                    self.standing = False
                #Move right    
                else:   
                    self.rect.x += self.vel  
                    self.left = False
                    self.right = True
                    self.up = False
                    self.down = False
                    self.standing = False  
            else:
                #Move up
                if self.rect.y > player.rect.y:
                    self.rect.y -= self.vel    
                    self.left = False
                    self.right = False
                    self.up = True
                    self.down = False
                    self.standing = False  
                #Move down
                else:
                    self.rect.y += self.vel   
                    self.left = False
                    self.right = False
                    self.up = False
                    self.down = True
                    self.standing = False 

        #Blocked by walls
        block_hit_list = py.sprite.spritecollide(self, current_room.wall_list, False)
        for block in block_hit_list:
            #Reset position based on the left/right of the object
            if self.right:
                self.rect.right = block.rect.left 
            if self.left:
                self.rect.left = block.rect.right
            #Reset position based on the top/bottom of the object
            if self.down:
                self.rect.bottom = block.rect.top 
            if self.up:
                self.rect.top = block.rect.bottom
    
            
    def hit(self, bullets:list, player):
        """Determines hits and health"""
        epsilon = 50 #Radius of impact
        for bullet in bullets:
            distance = np.sqrt((self.rect.x - bullet.rect.x)**2+(self.rect.y - bullet.rect.y)**2)
            if distance < epsilon and self.alive:
                self.health -= random.randint(0, player.damage) #random damage
                bullets.pop(bullets.index(bullet)) #removes bullets after hit
                player.score += 1 #score for player
                self.shot_hit.play()
                if self.health <= 0:
                    self.alive = False   
                    
    def shoot(self, arrows: list): 
        pass
                
    @property
    def shot_hit(self):
        shot_hit = py.mixer.Sound('Sounds' + os.sep + 'shot_hit.wav')
        shot_hit.set_volume(0.1) #reduces volume
        return shot_hit