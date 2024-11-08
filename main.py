import pygame
import numpy as np
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
SOLDIER_CLICKED = pygame.USEREVENT + 2
soldier_clicked = pygame.event.Event(SOLDIER_CLICKED)
CANNON_UPGRADE_CLICKED = pygame.USEREVENT + 3
cannon_upgrade_clicked = pygame.event.Event(CANNON_UPGRADE_CLICKED)


# Object class 
class Button():
    def __init__(self, position, cd, cost, ID):
        self.position = position
        self.cd = cd
        self.cost = cost
        self.clicked = False
        self.rect = pygame.Rect(self.position,(100,100))
        self.ID = ID

    def draw(self):
        # click handling
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
            if self.ID == 'soldier':
                pygame.event.post(soldier_clicked)
            elif self.ID == 'cannon_upgrade':
                pygame.event.post(cannon_upgrade_clicked)
            self.clicked = False
        

            
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        if self.ID == 'soldier':
            text = my_font.render('Soldier', True,'yellow', 'black')
            text2 = my_font.render('10', True,'yellow', 'black')
            textRect = text.get_rect()
            textRect2 = text2.get_rect()
            X = 50
            Y = 50
            Y2 = 100
            textRect.center = (X, Y // 2)
            textRect2.center = (X, Y2 // 2)
            screen.blit(text, textRect)
            screen.blit(text2, textRect2)
        elif self.ID == 'cannon_upgrade':
            text = my_font.render('Cannon', True,'yellow', 'black')
            text2 = my_font.render('Upgrade', True,'yellow', 'black')
            text3 = my_font.render('30', True,'yellow', 'black')
            textRect = text.get_rect()
            textRect2 = text2.get_rect()
            textRect3 = text3.get_rect()
            X = 200
            Y = 50
            Y2 = 100
            Y3 = 150
            textRect.center = (X, Y // 2)
            textRect2.center = (X, Y2 // 2)
            textRect3.center = (X, Y3 // 2)
            screen.blit(text, textRect)
            screen.blit(text2, textRect2)
            screen.blit(text3, textRect3)

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
    def __init__(self, size, speed, health, dps, team=0):
        self.team = team
        if self.team != 0:
            self.speed = -speed
        else:
            self.speed = speed
        self.health = health
        self.dps = dps
        self.size = size
        if team == 0:
            self.x = 250
        else:
            self.x = 1920 - castle_width + 8
        self.y = 980

        self.damage = 10

        self.rect = pygame.Rect((self.x, self.y), self.size)

    def update(self):
        self.x += self.speed
        self.rect = pygame.Rect((self.x, self.y), self.size)

    def kill(self):
        pass
    

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), ((self.x,self.y), self.size))


castle_health = 500
castle_width = 200
castle_height = 600
class Castle:
    def __init__(self, cannon, team):
        self.health = castle_health
        self.cannon = cannon
        self.team = team

        if team:
            self.x = 1920 - castle_width
        else:
            self.x = 0
        self.y = 1080 - castle_height
        
        self.rect = pygame.Rect((self.x, self.y), (castle_width, castle_height))
        self.rect1 = pygame.Rect((self.x, self.y - 50), (50, 50))
        self.rect2 = pygame.Rect((self.x + 75, self.y - 50), (50, 50))
        self.rect3 = pygame.Rect((self.x + 150, self.y - 50), (50, 50))

    def draw(self):
        if self.cannon:
            self.cannon.draw()
        if self.team == 0:
            pygame.draw.rect(screen, (0, 0, 0), ((0, 200), (self.health, 10)))
        else:
            pygame.draw.rect(screen, (0, 0, 0), ((WIDTH - self.health, 200), (self.health, 10)))
            
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect1)
        pygame.draw.rect(screen, (0, 0, 0), self.rect2)
        pygame.draw.rect(screen, (0, 0, 0), self.rect3)

# Cannon class
class Cannon:
    def __init__(self):
        self.level = 1
        self.speed = 10 + self.level
        self.reload = 120 // (self.level*0.5 + 0.5)
        self.damage = 2 * self.level
        self.x0, self.y0 = (50 + castle_width, 1100 - castle_height)
        self.cannonballs = set()
        self.ready = False
        self.cycles = 0
        self.x, self.y = 0, 1050 - castle_height
        self.rect = pygame.Rect((self.x, self.y), (50, 30))

    def draw(self):
        if not self.ready:
            p = self.cycles / self.reload 
            pygame.draw.rect(screen, (0, 0, 0), ((castle_width, 1070 - castle_height), (50*p, 5)))
            self.cycles += 1
        else:
            pygame.draw.rect(screen, (0, 0, 0), ((castle_width, 1070 - castle_height), (50, 5)))

        if self.cycles >= self.reload:
            self.ready = True
            self.cycles = 0
        to_remove = set()
        for ball in self.cannonballs:
            if ball.center[0] < 0 or ball.center[0] > WIDTH or ball.center[1] < 0 or ball.center[1] > HEIGHT:
                to_remove.add(ball)
            ball.draw()
        self.cannonballs = self.cannonballs.difference(to_remove)
        pygame.draw.rect(screen, (0, 0, 0), ((0, self.y0 - 25), (castle_width + 50, 40)))

    def fire(self, dst):
        if self.ready:
            pygame.mixer.music.load('cannon.mp3')
            pygame.mixer.music.play()
            x, y = dst[0], dst[1]
            vector = np.array([x - self.x0, y - self.y0])
            magnitude = np.linalg.norm(vector)
            unit_vector = vector / magnitude
            vector = unit_vector * self.speed
            self.cannonballs.add(Cannonball([self.x0, self.y0], vector, self.damage))
        self.ready = False
    
    def upgrade(self):
        self.level += 1
        self.speed = 10 + (self.level*5)
        self.reload = 120 // (self.level*0.5 + 0.5)
        self.damage = 2 * self.level



# Cannonball class
class Cannonball:
    def __init__(self, center, vector, damage):
        self.center = center
        self.vector = vector
        self.damage = damage
        self.radius = 10
        self.rect = pygame.Rect(center[0]-self.radius, center[1]-self.radius, self.radius*2, self.radius*2)

    def draw(self):
        self.vector[1] += 0.3
        self.center[0] += self.vector[0]
        self.center[1] += self.vector[1]
        pygame.draw.circle(screen, (0, 0, 0), self.center, self.radius)
        self.rect = pygame.Rect(self.center[0]-self.radius, self.center[1]-self.radius, self.radius*2, self.radius*2)


# Enemy class
class Enemy:
    def __init__(self):
        self.level = 1
        self.troops = set()
        self.soldier_reset = 360
        self.cycles = 0
    
    def draw(self):
        self.cycles += 1
        if self.cycles % self.soldier_reset == 0:
            self.troops.add(Troop((16,16),1.5,1,1,1))
        if self.cycles % 1200 == 0:
            if self.soldier_reset > 30:to_delete_enemies.add(enemy)

        for troop in self.troops:
            troop.update()
            troop.draw()




# game loop
troops = set()
soldier_button = Button((0,0),1,1,'soldier')
cannon_upgrade_button = Button((150,0),1,1,'cannon_upgrade')
tick_count = 0
player0 = Player(0)
cannon = Cannon()
player_castle = Castle(cannon, 0)
enemy_castle = Castle(None, 1)
enemy_ai = Enemy()
clicked = False
while running:
    # poll for events
    for ball in cannon.cannonballs:
        for enemy in enemy_ai.troops:
            to_delete = set()
            if ball.rect.colliderect(enemy.rect):
                pygame.mixer.music.load('hit.mp3')
                pygame.mixer.music.play()
                to_delete.add(enemy)
            player0.gain_money(2*len(to_delete))
            
            enemy_ai.troops = enemy_ai.troops.difference(to_delete)

    to_delete_enemies = set()
    to_delete_troops = set()
    for enemy in enemy_ai.troops:
        if enemy.x <= castle_width:
            to_delete_enemies.add(enemy)
            player_castle.health -= enemy.damage*20
            pygame.mixer.music.load('explode.mp3')
            pygame.mixer.music.play()
            if player_castle.health <= 0:
                print('DEFEAT!')
                running = False
        for troop in troops:
            if enemy.rect.colliderect(troop):
                to_delete_troops.add(troop)
                to_delete_enemies.add(enemy)
    troops = troops.difference(to_delete_troops)
    enemy_ai.troops = enemy_ai.troops.difference(to_delete_enemies)

    to_delete_troops = set()
    for troop in troops:
        if troop.x > WIDTH - castle_width:
            to_delete_troops.add(troop)
            pygame.mixer.music.load('explode.mp3')
            pygame.mixer.music.play()
            enemy_castle.health -= troop.damage*20
            if enemy_castle.health <= 0:
                print('VICTORY!')
                running = False

    troops = troops.difference(to_delete_troops)



    # pygame.QUIT event means the user clicked X to close your window
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SOLDIER_CLICKED:
            if player0.money >= 10:
                troops.add(Troop((16,16),1.5,1,1,0))
                player0.lose_money(10)
        elif event.type == CANNON_UPGRADE_CLICKED:
            if player0.money >= 30:
                cannon.upgrade()
                player0.lose_money(30)


        elif event.type == MOUSE_CLICKED:
            if pygame.mouse.get_pos()[1] >= 100:
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
        tick_count = 0

        
    player0.display_money()
    soldier_button.draw()
    cannon_upgrade_button.draw()
    player_castle.draw()
    
    enemy_castle.draw()
    enemy_ai.draw()

    for troop in troops:
        troop.update()
    for troop in troops:
        troop.draw()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit() 