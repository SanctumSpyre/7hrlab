import pygame

class Troops():
    def __init__(self, size, speed, health, dps, team=0):
        self.team = team
        if self.team != 0:
            self.speed = -speed
        else:
            self.speed = speed
        self.health = health
        self.dps = dps
        self.size = size

    def kill(self):
        if self.health <= 0:
            

    def draw(self):


    

