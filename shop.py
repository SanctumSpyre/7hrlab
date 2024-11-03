import pygame
#for the shop
class Button():
    def __init__(self, cooldown, cost, name):
        self.cooldown = cooldown
        self.cost = cost
        self.name = name