import pygame
import numpy as np
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 40)

# GLOBAL VARIABLES 
COLOR = (255, 100, 98) 
SURFACE_COLOR = (167, 255, 100) 
WIDTH = 1920
HEIGHT = 1080
MOUSE_CLICKED = pygame.USEREVENT + 1
mouse_clicked = pygame.event.Event(MOUSE_CLICKED)
SOLDIER_CLICKED = pygame.USEREVENT + 2
soldier_clicked = pygame.event.Event(SOLDIER_CLICKED)
# Object class 
class Button():
    def __init__(self, position, cd, cost):
        self.position = position
        self.cd = cd
        self.cost = cost
        self.clicked = False
        self.rect = pygame.Rect(self.position,(50,50)) 

    def draw(self):
        # click handling
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
            pygame.event.post(soldier_clicked)
            self.clicked = False

            
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
    
class Player():
    def __init__(self, money):
        self.money = money

    def gain_money(self, income):
        self.money += income

    def lose_money(self, spendings):
        self.money -= spendings

    def display_money(self):
        text = my_font.render(f"{self.money}", True,'yellow', 'black')
        textRect = text.get_rect()
        X = 1900
        Y = 50
        # set the center of the rectangular object.
        textRect.center = (X, Y // 2)
        screen.blit(text, textRect)
        
class Troop():
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
        if team == 0:
            self.x == 0
        else:
            self.x == 1920

    def update(self):
        self.x += self.speed

    def kill(self):
        pass
    

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), ((self.x,self.y), self.size))

# Castle class
# 1920 x 1080
castle_health = 1000
castle_width = 200
castle_height = 600

class Castle:
    def __init__(self, cannon, team):
        self.health = castle_health
        self.cannon = cannon

        if team:
            self.x = 1920 - castle_width/2
        else:
            self.x = -castle_width/2
        self.y = 1080 - castle_height
        
        self.rect = pygame.Rect((self.x, self.y), (castle_width, castle_height))

    def draw(self):
        if self.cannon:
            self.cannon.draw()
        pygame.draw.rect(screen, (0, 0, 0), self.rect)

# Cannon class
class Cannon:
    def __init__(self, level=1):
        self.speed = 10 * level
        self.reload = 240 // (level*0.5 + 0.5)
        self.damage = 2 * level
        self.x0, self.y0 = (50, 1035 - castle_height)
        self.cannonballs = set()
        self.ready = True
        self.cycles = 0

    def draw(self):
        if not self.ready:
            self.cycles += 1

        if self.cycles >= self.reload:
            self.ready = True
            self.cycles = 0

        to_remove = set()
        for ball in self.cannonballs:
            if ball.center[0] < 0 or ball.center[0] > WIDTH or ball.center[1] < 0 or ball.center[1] > HEIGHT:
                to_remove.add(ball)
            ball.draw()
        self.cannonballs = self.cannonballs.difference(to_remove)
        pygame.draw.rect(screen, (0, 0, 0), ((0, 1050 - castle_height), (50, 30)))

    def fire(self, dst):
        if self.ready:
            x, y = dst[0], dst[1]
            vector = np.array([x - self.x0, y - self.y0])
            magnitude = np.linalg.norm(vector)
            unit_vector = vector / magnitude
            vector = unit_vector * self.speed
            self.cannonballs.add(Cannonball([self.x0, self.y0], vector, self.damage))
        self.ready = False



# Cannonball class
class Cannonball:
    def __init__(self, center, vector, damage):
        self.center = center
        self.vector = vector
        self.damage = damage
        self.radius = 10

    def draw(self):
        self.vector[1] += 0.3
        self.center[0] += self.vector[0]
        self.center[1] += self.vector[1]
        pygame.draw.circle(screen, (0, 0, 0), self.center, self.radius)





# game loop
troops = []
soldier_button = Button((0,0),1,1)
tick_count = 0
player0 = Player(0)
cannon = Cannon()
player_castle = Castle(cannon, 0)
enemy_castle = Castle(None, 1)
clicked = False
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SOLDIER_CLICKED:
            troops.append(Troop((16,16),1/60,1,1,10,0))
        elif event.type == MOUSE_CLICKED:
            cannon.fire(pygame.mouse.get_pos())


    # looking for mouse click
    if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
        clicked = True
    if pygame.mouse.get_pressed()[0] == 0 and clicked == True:
        pygame.event.post(mouse_clicked)
        clicked = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")
    
    # RENDER YOUR GAME HERE
    tick_count += 1/60.0
    if tick_count >= 1:
        player0.gain_money(1)
    player0.display_money()
    soldier_button.draw()
    player_castle.draw()
    enemy_castle.draw()
    for troop in troops:
        troop.update()
    for troop in troops:
        troop.draw()


    if tick_count >= 1:
        tick_count = 0

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit() 