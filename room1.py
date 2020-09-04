"""Creates first room; inherits from Room superclass"""
import pygame as py
import copy
import os as os

from room import Room
from wall import Wall

class Room1(Room):
    """This creates all the walls in room 1"""
    def __init__(self):
        super().__init__()
        # Make walls (x, y, width, height)   
        global door, walls, secret
        door = [205, 350, 10, 90, self.brown]   
        secret = [740, 350, 110, 20, self.white]  
        walls = [[20, 20, 20, 580, self.white],
                 [20, 20, 510, 20, self.white],   
                 [620, 20, 250, 20, self.white], 
                 [20, 580, 850, 20, self.white],
                 [850, 20, 20, 580, self.white],
                 [200, 20, 20, 330, self.white],
                 [200, 440, 20, 140, self.white],
                 [490, 20, 20, 330, self.white],
                 [490, 350, 250, 20, self.white]
                ]
        block = copy.deepcopy(walls) #makes deep copy
        block.append(door) #adds door
        block.append(secret) #adds secret door
        
        #Add list of walls to wall_list from superclass Room               
        for item in block:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
            
        #Door closed
        self.door_open = False
        #Secret door closed
        self.secret_open = False
            
    def open_door(self, player, current_room):
        if player.rect.x - door[0] > -100: #Door opens if player comes close
            self.wall_list = None
            self.wall_list = py.sprite.Group()
            block = copy.deepcopy(walls) #makes deep copy
            block.append(secret) #adds secret door
            #Add list of walls to wall_list from superclass Room               
            for item in block:
                wall = Wall(item[0], item[1], item[2], item[3], item[4])
                self.wall_list.add(wall)   
                
            #Declare door open
            self.door_open = True
            
        if len(current_room.enemies) <= 1: #Secret door opens after two orc killed
            self.wall_list = None
            self.wall_list = py.sprite.Group()
            block = copy.deepcopy(walls) #makes deep copy
            #Add list of walls to wall_list from superclass Room               
            for item in block:
                wall = Wall(item[0], item[1], item[2], item[3], item[4])
                self.wall_list.add(wall)   
                
            #Declare door open
            self.secret_open = True         
             

    def draw(self, win, player):
        """Drawing objects in room"""
        table = py.image.load('Pictures' + os.sep + 'Room' + os.sep + 'tableRound_E.png')
        win.blit(table, (250, 30))  
        
        barrel = py.image.load('Pictures' + os.sep + 'Room' + os.sep + 'barrelsStacked_E.png')
        win.blit(barrel, (200, -280))
        
        if player.rect.x > 730 and player.rect.y < 100:
            chest_open = py.image.load('Pictures' + os.sep + 'Room' + os.sep + 'chestOpen_E.png')
            win.blit(chest_open, (660, -290))
            player.health = 100
        else:
            chest = py.image.load('Pictures' + os.sep + 'Room' + os.sep + 'chestClosed_E.png')
            win.blit(chest, (660, -290))   
       
       
    def find_weapon(self, player):
        pass
    
    def traps(self, player, arrows: list):
        pass
       



            

