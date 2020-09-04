"""Creates Bullet class"""
import pygame as py

class Bullet():
    def __init__(self, x, y, facing_x, facing_y):
        # self.x = x
        # self.y = y
        self.facing_x = facing_x
        self.facing_y = facing_y
        self.vel = 10 
        # Make our top-left corner the passed-in location; for wall collision
        self.image = py.Surface([4, 4])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y  
        
    def draw(self, win):
        #Color (0,0,255); last is thickness / radius
        #red = (255,   0,   0)
        py.draw.circle(win, (0,0,255), (round(self.rect.x), round(self.rect.y)), 3, 1)        
       
    def fly(self, xdim, bullets: list, walls: list):
        """How bullets fly; needs xdim and a list of bullets"""
        #Blocked by walls
        block_hit_list = py.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            bullets.pop(bullets.index(self)) #removes bullets at boundaries            
       
        if self.facing_y == 0: #Player moves left or right
            self.rect.x += self.vel * self.facing_x
        if self.facing_x == 0: #Player moves down or up
            self.rect.y += self.vel * self.facing_y
