"""Creates third room; inherits from Room superclass"""
import pygame as py
import copy

from room import Room
from wall import Wall
from bullet import Bullet

class Room3(Room):
    """This creates all the walls in room 1"""
    def __init__(self):
        super().__init__()
        # Make walls (x, y, width, height)   
        global door, walls
        door = [[200, 455, 190, 10, self.brown],
                [390, 450, 250, 20, self.white],
                ]
        walls = [[20, 200, 20, 250, self.white],
                 [20, 200, 500, 20, self.white],
                 [0, 450, 200, 20, self.white],               
                 [0, 580, 850, 20, self.white],
                 [850, 20, 20, 600, self.white],
                 [350, 20, 20, 250, self.white],
                 [350, 20, 500, 20, self.white]
                ]
        block = copy.deepcopy(walls) #makes deep copy
        block.extend(door) #adds door
        
        #Add list of walls to wall_list from superclass Room               
        for item in block:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
            
        #Door closed
        self.door_open = False
            
    def open_door(self, player, current_room):
        if player.rect.x > 350: #Door opens if player comes close
            self.wall_list = None
            self.wall_list = py.sprite.Group()
            #Add list of walls (global) to wall_list from superclass Room               
            for item in walls:
                wall = Wall(item[0], item[1], item[2], item[3], item[4])
                self.wall_list.add(wall)   
                
            #Declare door open
            self.door_open = True


    def draw(self, win, player):
        pass
    
    def find_weapon(self, player):
        if player.rect.x < 45 and player.rect.y < 45:
            player.weapon = True
            
    def traps(self, player, arrows: list):
        count = 0
        
        if abs(player.rect.x - 155) < 50 and abs(player.rect.y - 365) < 50 and count < 2 and len(arrows) < 5:
            count += 1
            arrow = Bullet(x = player.rect.x - 80, \
            y = player.rect.y + 50, facing_x = 1, facing_y = 0)
            arrow.vel = 5
            arrows.append(arrow)  
            


