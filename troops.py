import pygame

class Troops():
    def __init__(self, size, speed, health, dps, cost, team=0):
        self.team = team
        if self.team != 0:
            self.speed = -speed
        else:
            self.speed = speed
        self.health = health
        self.dps = dps
        self.size = size
        self.cost = cost

    def kill(self):
            

    def draw(self):


    

