"""Main file for execution"""
#https://www.mapeditor.org/

import pygame as py
import os as os

from player import Player
from redraw import redraw_game_window
from orc import Orc
from zombie import Zombie
from evil import Evil
from room1 import Room1
from room2 import Room2
from room3 import Room3

#Initialise PyGame
py.init()

#Initialize fonts
py.font.init()

#Create window of certain dimension
xdim = 900
ydim = 600
win = py.display.set_mode((xdim, ydim))

#Title of game
py.display.set_caption("Quest")

#Background
background = py.image.load('Pictures' + os.sep + 'Room' + os.sep + 'StoneTexture.jpg')
background = py.transform.scale(background,(xdim, ydim)) #rescale

#Clock; pics per minute
clock = py.time.Clock()

#Main loop
#List of bullets
bullets = []

#List of arrows
arrows = []

#Room setup
rooms = [
    Room1(),
    Room2(),
    Room3()
    ]
  
#Adding enemies to the room
rooms[0].enemies.add(Orc(x = 400, y = 300))
rooms[0].enemies.add(Orc(x = 400, y = 100))
rooms[0].enemies.add(Zombie(x = 600, y = 70))
rooms[1].enemies.add(Orc(x = 600, y = 500))
rooms[1].enemies.add(Orc(x = 600, y = 400))
rooms[1].enemies.add(Orc(x = 600, y = 350))
rooms[1].enemies.add(Zombie(x = 600, y = 50))
rooms[1].enemies.add(Zombie(x = 600, y = 100))
rooms[2].enemies.add(Orc(x = 200, y = 290))
rooms[2].enemies.add(Orc(x = 450, y = 100))
rooms[2].enemies.add(Orc(x = 200, y = 350))
rooms[2].enemies.add(Orc(x = 350, y = 350))
rooms[2].enemies.add(Zombie(x = 220, y = 330))
rooms[2].enemies.add(Evil(x = 520, y = 100))

current_room_no = 0
current_room = rooms[current_room_no]  

#Initialize player
if current_room_no == 0:
    player = Player(x = 50, y = 300)
if current_room_no == 1:
    player = Player(x = 125, y = 490)    
if current_room_no == 2:
    player = Player(x = 50, y = 475)    

run = True

while run: 
    #py.time.delay(100) slows down movement in ms
    clock.tick(20)    
  
    for event in py.event.get(): #loop over events
        if event.type == py.QUIT: #hit the exit button in corner of window
            run = False #stops the while loop
           
       
    #pressed keys induce movement
    keys = py.key.get_pressed()
    #Start message
    if current_room_no == 0 and player.rect.x == 50 and player.rect.y == 300:
        start_time = py.time.get_ticks() #Time in ms
        
        #Font size and style
        font = py.font.SysFont('Arial', 30, True)
                              
        while py.time.get_ticks() - start_time < 300:
            text = font.render('Hi Player! Space triggers your magic eyes!', True, (255,0,0)) #rendering text
            win.blit(text, (xdim//2 - 300, ydim//2)) #positioning text      
            py.display.update() #needed to show actors
    
    #Movement of player
    player.move(xdim, ydim, current_room.wall_list)    
     
    #Open door
    current_room.open_door(player, current_room)       
     
    #Player heals
    player.magic_heal(win, xdim, ydim)
    
    #Fire magic
    player.magic_fire(win, xdim, ydim, current_room)
    
    #Movement of enemies
    for enemy in current_room.enemies:
        enemy.move(player, xdim, ydim, current_room)               

    #Player hit by enemies
    player.hit(current_room)        
              
    #Bullets shooting by player
    player.shoot(xdim, bullets)    
      
    #Bullets fly      
    for bullet in bullets:
        bullet.fly(xdim, bullets, current_room.wall_list) 

    #Hits against enemies
    for enemy in current_room.enemies:
        enemy.hit(bullets, player)     
        
    #Check how many enemies are alive and remove from list
    for enemy in current_room.enemies:
        if not enemy.alive:
            current_room.enemies.remove(enemy)
        
    #Find weapons in room
    current_room.find_weapon(player)    
    
    #Execue traps in room
    current_room.traps(player, arrows) 
    
    #Evil shoots
    for enemy in current_room.enemies:
        enemy.shoot(arrows)
    
    #Arrows fly      
    for arrow in arrows:
        arrow.fly(xdim, arrows, current_room.wall_list) 
    
    #Player affected by traps
    player.hit_arrow(arrows)     
    
    #Moving between rooms
    if current_room_no == 0 and player.rect.y < 20:
        current_room_no = 1
        current_room = rooms[current_room_no]
        player.rect.x = 125
        player.rect.y = 490
        
    if current_room_no == 1 and player.rect.x >= 840:
        current_room_no = 2
        current_room = rooms[current_room_no]
        player.rect.x = 50
        player.rect.y = 475
        
        
        
    #Winning message
    if len(current_room.enemies) == 0 and current_room_no == 2:
        start_time = py.time.get_ticks() #Time in ms
        
        #Font size and style
        font = py.font.SysFont('Arial', 50, True)        
                             
        while py.time.get_ticks() - start_time < 800:
            text = font.render('VICTORY TO PLAYER', True, (255,0,0)) #rendering text
            win.blit(text, (xdim//2 - 300, ydim//2)) #positioning text      
            py.display.update() #needed to show actors     
        
    #Drawing the game        
    redraw_game_window(player, bullets, win, current_room, background, arrows)
    
        
py.quit() #quits application






