"""Builds Zombie class"""
import pygame as py
import os as os

from enemy import Enemy

class Zombie(Enemy):
    def __init__(self, x, y):
        self.vel = 1
        self.health = 200
        self.damage = 20
       
        # Call constructor from superclass
        super().__init__(x, y)       
        
             
                
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
            location = 'Pictures' + os.sep + 'Zombie' + os.sep + pic
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
            location = 'Pictures' + os.sep + 'Zombie' + os.sep + pic
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
            location = 'Pictures' + os.sep + 'Zombie' + os.sep + pic
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
            location = 'Pictures' + os.sep + 'Zombie' + os.sep + pic
            down_walk.append(py.image.load(location))
        return down_walk      
    
    @property
    def load_standing_pic(self):
        #Character standing
        char = py.image.load('Pictures' + os.sep + 'Zombie' + os.sep + 'Front.png')
        return char



