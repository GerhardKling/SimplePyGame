"""Builds Wall class"""
import pygame as py

class Wall(py.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        """Construction of wall"""
 
        # Call constructor from superclass
        super().__init__()
 
        # Make a BLUE wall, of the size specified in the parameters
        self.image = py.Surface([width, height])
        self.image.fill(color)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
               

