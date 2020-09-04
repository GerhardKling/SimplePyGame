"""Builds Room superclass"""
import pygame as py

class Room():
    """Superclass for all rooms"""
    #Colors as class attributes
    white = (255, 255, 255)
    black = (  0,   0,   0)
    red   = (255,   0,   0)
    light_gray = ((200,200,200))
    dark_gray = ((50,50,50))
    brown = ((100,40,0))
 
    # Each room has a list of walls and enemies.
    wall_list = None
    enemies = None
 
    def __init__(self):
        """Constructor, create lists"""
        self.wall_list = py.sprite.Group()
        self.enemies = py.sprite.Group()


