import pygame
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

# GLOBAL VARIABLES 
COLOR = (255, 100, 98) 
SURFACE_COLOR = (167, 255, 100) 
WIDTH = 500
HEIGHT = 500

# Object class 
class Player():
    def __init__(self, money):
        self.money = money

    def gain_money(self, income):
        self.money += income

    def lose_money(self, spendings):
        self.money -= spendings

    def display_money(self):
        
        
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
        


# Castle class
# 1920 x 1080
castle_health = 1000
castle_width = 200
castle_height = 600

class castle:
    def __init__(self, cannon, team):
        self.health = castle_health
        self.cannon = cannon

        if team:
            self.x = 1920 - castle_width/2
        else:
            self.x = castle_width/2
        self.y = 1080 - castle_height

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y))







class Sprite(pygame.sprite.Sprite): 
    def __init__(self, color, height, width): 
        super().__init__() 
  
        self.image = pygame.Surface([width, height]) 
        self.image.fill(SURFACE_COLOR) 
        self.image.set_colorkey(COLOR) 
  
        pygame.draw.rect(self.image, 
                         color, 
                         pygame.Rect(0, 0, width, height)) 
  
        self.rect = self.image.get_rect()  

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit() 