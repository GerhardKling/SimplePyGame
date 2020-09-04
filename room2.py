"""Creates second room; inherits from Room superclass"""
import pygame as py
import copy
import os as os

from room import Room
from wall import Wall
from bullet import Bullet

class Room2(Room):
    """This creates all the walls in room 1"""
    def __init__(self):
        super().__init__()
        # Make walls (x, y, width, height)   
        global door, walls
        door = [305, 350, 10, 90, self.brown]         
        walls = [[20, 20, 20, 580, self.white],
                 [20, 20, 850, 20, self.white],   
                 [20, 580, 850, 20, self.white],
                 [850, 20, 20, 450, self.white],
                 [850, 450, 60, 20, self.white],
                 [850, 570, 20, 10, self.white],
                 [850, 560, 60, 20, self.white],
                 [300, 20, 20, 330, self.white],
                 [300, 440, 20, 140, self.white],
                 [300, 330, 200, 20, self.white],
                 [700, 330, 150, 20, self.white],
                ]
        block = copy.deepcopy(walls) #makes deep copy
        block.append(door) #adds door
        
        #Add list of walls to wall_list from superclass Room               
        for item in block:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
            
        #Door closed
        self.door_open = False
            
    def open_door(self, player, current_room):
        if player.rect.x - door[0] > -100: #Door opens if player comes close
            self.wall_list = None
            self.wall_list = py.sprite.Group()
            #Add list of walls (global) to wall_list from superclass Room               
            for item in walls:
                wall = Wall(item[0], item[1], item[2], item[3], item[4])
                self.wall_list.add(wall)   
                
            #Declare door open
            self.door_open = True


    def draw(self, win, player):
        if player.rect.x < 45 and player.rect.y < 50:
            chest_open = py.image.load('Pictures' + os.sep + 'Room' + os.sep + 'chestOpen_E.png')
            win.blit(chest_open, (-30, -350))
        else:
            chest = py.image.load('Pictures' + os.sep + 'Room' + os.sep + 'chestClosed_E.png')
            win.blit(chest, (-30, -350))   
            
        if player.rect.x > 680 and player.rect.y < 50:
            chest_open = py.image.load('Pictures' + os.sep + 'Room' + os.sep + 'chestOpen_E.png')
            win.blit(chest_open, (600, -350))
            player.health = 100
        else:
            chest = py.image.load('Pictures' + os.sep + 'Room' + os.sep + 'chestClosed_E.png')
            win.blit(chest, (600, -350))       
    
    
    def find_weapon(self, player):
        if player.rect.x < 45 and player.rect.y < 50:
            player.weapon = True
            
    def traps(self, player, arrows: list):
        count = 0
        
        if abs(player.rect.x - 155) < 50 and abs(player.rect.y - 365) < 50 and count < 2 and len(arrows) < 5:
            count += 1
            arrow = Bullet(x = player.rect.x - 80, \
            y = player.rect.y + 50, facing_x = 1, facing_y = 0)
            arrow.vel = 5
            arrows.append(arrow)  
            
