import pygame
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# GLOBAL VARIABLES 
COLOR = (255, 100, 98) 
SURFACE_COLOR = (167, 255, 100) 
WIDTH = 1920
HEIGHT = 1080
MOUSE_CLICKED = pygame.USEREVENT + 1
mouse_clicked = pygame.event.Event(MOUSE_CLICKED)

# Object class 
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
        X = 1800
        Y = 100
        # set the center of the rectangular object.
        textRect.center = (X // 2, Y // 2)
        screen.blit(text, textRect)
        
class Troops():
    def __init__(self, size, speed, health, dps, cost, team=0):
        self.team = team
        if self.team != 0:
            self.speed = -speed
        else:
            self.speed = speed
        self.health = healthtext = font.render('GeeksForGeeks', True, green, blue)
        self.dps = dps
        self.size = size
        self.cost = cost

    def kill(self):
        pass

    def draw(self):
        pass

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
        self.reload = 10 // level
        self.damage = 2 * level
        self.x0, self.y0 = (50, 1035 - castle_height)
        self.cannonballs = {}

    def draw(self):
        to_remove = {}
        for ball in self.cannonballs:
            if ball.center[0] < 0 or ball.center[0] > WIDTH or ball.center[1] < 0 or ball.center[1] > HEIGHT:
                to_remove.add(ball)
            ball.draw()
        self.cannonballs.difference(to_remove)
        pygame.draw.rect(screen, (0, 0, 0), ((0, 1050 - castle_height), (50, 30)))

    def fire(self, dst):
        x, y = dst[0], dst[1]
        vector = [(x - self.x0) // 20, (y - self.y0) // 20]
        self.cannonballs.append(Cannonball([self.x0, self.y0], vector, self.damage))


# Cannonball class
class Cannonball:
    def __init__(self, center, vector, damage):
        self.center = center
        self.vector = vector
        self.damage = damage
        self.radius = 10

    def draw(self):
        self.center[0] += self.vector[0]
        self.center[1] += self.vector[1] - 5
        pygame.draw.circle(screen, (0, 0, 0), self.center, self.radius)




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

# game loop
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
        if event.type == MOUSE_CLICKED:
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

    player_castle.draw()
    enemy_castle.draw()



    if tick_count >= 1:
        tick_count = 0

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit() 