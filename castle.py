import pygame

# 1920 x 1080
castle_health = 1000
width = 200
height = 600

class castle:
    def __init__(self, cannon, team):
        self.health = castle_health
        self.cannon = cannon

        if team:
            self.x = 1920 - width/2
        else:
            self.x = width/2
        self.y = 1080 - height

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y))