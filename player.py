"""Builds player class"""
import pygame as py
import os as os
import random
import numpy as np

from bullet import Bullet

class Player(py.sprite.Sprite):
    def __init__(self, x, y):       
        #Position, dimension and velocity of character
        self.width = 40
        self.height = 40
        self.vel = 5
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
        #Score of player
        self.score = 0
        #Make our top-left corner the passed-in location; for wall collision
        self.image = py.Surface([70, 75])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y   
        #Does player have weapon?
        self.weapon = False
                  
    def draw(self, win):
        """Animation for moving"""
        #Player without weapon
        if not self.weapon:
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
                 
        #Player with weapon
        if self.weapon:
            if not self.standing:
                if self.left:
                    win.blit(self.load_left_pic1[self.walk % 8], (self.rect.x, self.rect.y))
                    self.walk += 1                
                elif self.right:
                    win.blit(self.load_right_pic1[self.walk % 8], (self.rect.x, self.rect.y))
                    self.walk += 1                
                elif self.down:
                    win.blit(self.load_down_pic1[self.walk % 8], (self.rect.x, self.rect.y))
                    self.walk += 1
                elif self.up:
                    win.blit(self.load_up_pic1[self.walk % 8], (self.rect.x, self.rect.y))
                    self.walk += 1   
                    
            else:
                if self.left:
                    win.blit(self.load_left_pic1[0], (self.rect.x, self.rect.y))
                elif self.right:    
                    win.blit(self.load_right_pic1[0], (self.rect.x, self.rect.y))
                elif self.down:    
                    win.blit(self.load_down_pic1[0], (self.rect.x, self.rect.y))              
                elif self.up:    
                    win.blit(self.load_up_pic1[0], (self.rect.x, self.rect.y))
                else:
                    win.blit(self.load_standing_pic1, (self.rect.x, self.rect.y))      
        
        #Health bar: red bar
        py.draw.rect(win, (255, 0, 0), \
        (750, 70, self.width, 5))
            
        #green bar decreaes with damage
        py.draw.rect(win, (0, 255, 0), \
        (750, 70, self.health/100 * self.width, 5))                
      
          
    def move(self, xdim, ydim, walls: list):
        """Moving with keys; needs dimension of window xdim; list of walls"""
        #pressed keys induce movement
        keys = py.key.get_pressed()
        
        #different directions; note (0,0) is top left corner
        #boundary effects; note coordinates in top left corner of obejct
        if keys[py.K_LEFT] and self.rect.x >= self.vel:
            self.rect.x -= self.vel #move by velocity to left
            self.left = True
            self.right = False
            self.up = False
            self.down = False
            self.standing = False
        elif keys[py.K_RIGHT] and self.rect.x <= xdim - self.width - self.vel:   
            self.rect.x += self.vel  
            self.left = False
            self.right = True
            self.up = False
            self.down = False
            self.standing = False
        elif keys[py.K_UP] and self.rect.y >= self.vel:
            self.rect.y -= self.vel
            self.left = False
            self.right = False
            self.up = True
            self.down = False
            self.standing = False
        elif keys[py.K_DOWN] and self.rect.y <= ydim - 2 * self.height - self.vel:
            self.rect.y += self.vel
            self.left = False
            self.right = False
            self.up = False
            self.down = True
            self.standing = False
        else:
            self.standing = True
            self.walk = 0  
  
        #Blocked by walls
        block_hit_list = py.sprite.spritecollide(self, walls, False)
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
  
                
    def hit(self, current_room):
        """Determines hits and health"""
        epsilon = 7 #Radius of impact
        for e in current_room.enemies:             
            distance = np.sqrt((self.rect.x - e.rect.x)**2+(self.rect.y - e.rect.y)**2)
            if distance < epsilon and e.alive:
                self.health -= random.randint(0, e.damage)
                self.melee_hit.play()
                if self.weapon and e.alive: #player hits back with weapon
                    e.health -= random.randint(0, self.damage * 2)                    
                    if e.health <= 0:
                        e.alive = False
                        self.score += 50
                if self.health <= 0:
                    self.alive = False                    

    def hit_arrow(self, arrows:list):
        """Determines hits and health"""
        epsilon = 60 #Radius of impact
        for arrow in arrows:
            distance = np.sqrt((self.rect.x - arrow.rect.x)**2+(self.rect.y - arrow.rect.y)**2)
            if distance < epsilon and self.alive:
                self.health -= random.randint(0, 2) #random damage
                arrows.pop(arrows.index(arrow)) #removes bullets after hit
                self.shot_hit.play()
                if self.health <= 0:
                    self.alive = False                
               
    def shoot(self, xdim, bullets: list):  
        """Shooting bullets; xdim needed"""
        #pressed keys induce movement
        keys = py.key.get_pressed()
        
        #not more than 3 live bullets
        if keys[py.K_SPACE]: 
            if bullets ==[]:
                first_shot = True
            else:
                first_shot = False
            
            next_shot = False
            #Minimum distance between next shots
            if not first_shot:
                distance = np.sqrt((bullets[-1].rect.x - self.rect.x)**2 \
                            + (bullets[-1].rect.y - self.rect.y)**2)
                next_shot = len(bullets) < 3 and distance > 100
                        
            if first_shot or next_shot: 
                if self.left:
                    bullet = Bullet(x = self.rect.x + self.width, \
                    y = self.rect.y + self.height, facing_x = -1, facing_y = 0)
                    bullets.append(bullet)       
                if self.right:
                    bullet = Bullet(x = self.rect.x + self.width, \
                    y = self.rect.y + self.height, facing_x = 1, facing_y = 0)
                    bullets.append(bullet)       
                if self.down:
                    bullet = Bullet(x = self.rect.x + self.width, \
                    y = self.rect.y + self.height, facing_x = 0, facing_y = 1)
                    bullets.append(bullet)       
                if self.up:
                    bullet = Bullet(x = self.rect.x + self.width, \
                    y = self.rect.y + self.height, facing_x = 0, facing_y = -1)        
                    bullets.append(bullet)    
                self.shot_sound.play()     

    #Magic
    def magic_heal(self, win, xdim, ydim):
        #pressed keys induce movement
        keys = py.key.get_pressed()
        
        #Font size and style
        font = py.font.SysFont('Arial', 50, True)
                       
        if keys[py.K_h]:
            gap = 100 - self.health
            if self.score >= gap:
                self.health = 100
                self.score -= gap
            else:
                change = self.score
                self.health += change
                self.score -= change            
                    
            start_time = py.time.get_ticks() #Time in ms
                              
            while py.time.get_ticks() - start_time < 800:
                 text = font.render('MAGIC TO HEAL', True, (255,0,0)) #rendering text
                 win.blit(text, (xdim//2 - 150, ydim//2)) #positioning text      
                 py.display.update() #needed to show actors 
    
    #Magic
    def magic_fire(self, win, xdim, ydim, current_room):
        #pressed keys induce movement
        keys = py.key.get_pressed()
        
        #Font size and style
        font = py.font.SysFont('Arial', 50, True)
        
        if keys[py.K_f] and self.score > 50:
            start_time = py.time.get_ticks() #Time in ms
            self.score -= 50
            for enemy in current_room.enemies:
                enemy.health -= random.randint(10, 100)
                win.blit(self.load_fire_pic[0], (enemy.rect.x, enemy.rect.y))
                # time = 0
                # while time <= 13:
                #     win.blit(self.load_fire_pic[time], (enemy.rect.x, enemy.rect.y))
                #     time += 1
                
                if enemy.health <= 0:
                    enemy.alive = False
                    self.score += 10
            
            while py.time.get_ticks() - start_time < 1200:
                 text = font.render('MAGIC TO BURN', True, (255,0,0)) #rendering text
                 win.blit(text, (xdim//2 - 150, ydim//2)) #positioning text      
                 py.display.update() #needed to show actors
                 for enemy in current_room.enemies:
                     start_time = py.time.get_ticks()
                     while py.time.get_ticks() - start_time <= 600:
                         win.blit(self.load_fire_pic[7], (enemy.rect.x, enemy.rect.y))
                         py.display.update() #needed to show actors
                     while py.time.get_ticks() - start_time <= 900:
                         win.blit(self.load_fire_pic[10], (enemy.rect.x, enemy.rect.y))
                         py.display.update() #needed to show actors
                     while py.time.get_ticks() - start_time <= 1200:
                         win.blit(self.load_fire_pic[12], (enemy.rect.x, enemy.rect.y))
                         py.display.update() #needed to show actors
                 
                   
    #Properties defined by pictures; sprite sheet using RPG Character Builder
    #Splitting sprite sheet using online image splitter: https://ezgif.com/sprite-cutter
    @property        
    def load_left_pic(self):
        left_walk = []

        left_pic = (
            'L1.png',
            'L2.png',
            'L3.png',
            'L4.png',
            'L5.png',
            'L6.png',
            'L7.png',
            'L8.png'       
            )
        for pic in left_pic:
            location = 'Pictures' + os.sep + 'Player_empty' + os.sep + pic
            left_walk.append(py.image.load(location))
        
        return left_walk    
    
    @property
    def load_right_pic(self):
        right_walk = []

        right_pic = (
            'R1.png',
            'R2.png',
            'R3.png',
            'R4.png',
            'R5.png',
            'R6.png',
            'R7.png',
            'R8.png'       
            )
        for pic in right_pic:
            location = 'Pictures' + os.sep + 'Player_empty' + os.sep + pic
            right_walk.append(py.image.load(location))
        return right_walk    
    
    @property
    def load_up_pic(self):
        up_walk = []

        up_pic = (
            'U1.png',
            'U2.png',
            'U3.png',
            'U4.png',
            'U5.png',
            'U6.png',
            'U7.png',
            'U8.png'       
            )
        for pic in up_pic:
            location = 'Pictures' + os.sep + 'Player_empty' + os.sep + pic
            up_walk.append(py.image.load(location))
        return up_walk    

    @property
    def load_down_pic(self):
        down_walk = []

        down_pic = (
            'D1.png',
            'D2.png',
            'D3.png',
            'D4.png',
            'D5.png',
            'D6.png',
            'D7.png',
            'D8.png'       
            )
        for pic in down_pic:
            location = 'Pictures' + os.sep + 'Player_empty' + os.sep + pic
            down_walk.append(py.image.load(location))
        return down_walk      
    
    @property
    def load_standing_pic(self):
        #Character standing
        char = py.image.load('Pictures' + os.sep + 'Player_empty' + os.sep + 'Front.png')
        return char
    
    #Pictures for player with weapon
    @property        
    def load_left_pic1(self):
        left_walk = []

        left_pic = (
            'L1.png',
            'L2.png',
            'L3.png',
            'L4.png',
            'L5.png',
            'L6.png',
            'L7.png',
            'L8.png'       
            )
        for pic in left_pic:
            location = 'Pictures' + os.sep + 'Player' + os.sep + pic
            left_walk.append(py.image.load(location))
        
        return left_walk    
    
    @property
    def load_right_pic1(self):
        right_walk = []

        right_pic = (
            'R1.png',
            'R2.png',
            'R3.png',
            'R4.png',
            'R5.png',
            'R6.png',
            'R7.png',
            'R8.png'       
            )
        for pic in right_pic:
            location = 'Pictures' + os.sep + 'Player' + os.sep + pic
            right_walk.append(py.image.load(location))
        return right_walk    
    
    @property
    def load_up_pic1(self):
        up_walk = []

        up_pic = (
            'U1.png',
            'U2.png',
            'U3.png',
            'U4.png',
            'U5.png',
            'U6.png',
            'U7.png',
            'U8.png'       
            )
        for pic in up_pic:
            location = 'Pictures' + os.sep + 'Player' + os.sep + pic
            up_walk.append(py.image.load(location))
        return up_walk    

    @property
    def load_down_pic1(self):
        down_walk = []

        down_pic = (
            'D1.png',
            'D2.png',
            'D3.png',
            'D4.png',
            'D5.png',
            'D6.png',
            'D7.png',
            'D8.png'       
            )
        for pic in down_pic:
            location = 'Pictures' + os.sep + 'Player' + os.sep + pic
            down_walk.append(py.image.load(location))
        return down_walk      
    
    @property
    def load_fire_pic(self):
        fire_walk = []

        fire_pic = (
            'F1.png',
            'F2.png',
            'F3.png',
            'F4.png',
            'F5.png',
            'F6.png',
            'F7.png',
            'F8.png',  
            'F9.png', 
            'F10.png', 
            'F11.png', 
            'F12.png', 
            'F13.png'
            )
        for pic in fire_pic:
            location = 'Pictures' + os.sep + 'Magic' + os.sep + pic
            fire_walk.append(py.image.load(location))
        return fire_walk      
    
    @property
    def load_standing_pic1(self):
        #Character standing
        char = py.image.load('Pictures' + os.sep + 'Player' + os.sep + 'Front.png')
        return char    
    
    
    #Properties for sound
    @property
    def shot_sound(self):
        #See https://freesound.org
        return py.mixer.Sound('Sounds' + os.sep + 'shot.wav')
    
    @property
    def melee_hit(self):
        return py.mixer.Sound('Sounds' + os.sep + 'melee_hit.wav')
    
    @property
    def shot_hit(self):
        shot_hit = py.mixer.Sound('Sounds' + os.sep + 'shot_hit.wav')
        shot_hit.set_volume(0.1) #reduces volume
        return shot_hit