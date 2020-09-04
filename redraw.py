"""Defines the redraw function"""
import pygame as py

def redraw_game_window(player, bullets: list, win, current_room, background, arrows: list):     
    #Background image 
    win.blit(background,(0,0)) #Blit background onto the screen first
         
    #Draw player
    if player.alive:
        player.draw(win)
        
    #Draw enemies
    for enemy in current_room.enemies:
        if enemy.alive and enemy.visible:
            enemy.draw(win)
        
   
    #Draw bullets
    for bullet in bullets:
        bullet.draw(win)
        
    #Draw arrows
    for arrow in arrows:
        arrow.draw(win)    
        
    #Draw walls of current room
    current_room.wall_list.draw(win)    

    #Draw objects in current room
    current_room.draw(win, player)       
       
    #Font size and style
    font = py.font.SysFont('Arial', 12, True)
    
    #Score display
    text = font.render(f'Score: {player.score}', True, (255,0,0)) #rendering text
    win.blit(text, (750, 40)) #positioning text
    
    #Health display
    text = font.render('Health', True, (255,0,0)) #rendering text
    win.blit(text, (750, 55)) #positioning text
    
    py.display.update() #needed to show actors 