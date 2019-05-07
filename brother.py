#Import library
import pygame
from pygame.locals import *
import random
class Opponent(pygame.sprite.Sprite):
    def __init__(self):
        super(Opponent, self).__init__()
        self.image = pygame.image.load('bird.gif').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(
        center=(random.randint(820, 900), random.randint(0, 600))
    )
        self.speed = random.randint(1, 2)
 
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill() 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('jet.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect()
        self.surf = pygame.Surface((75, 75))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
  
    def move(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)
        #Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600 
#Initialize pygame modules
pygame.init()
   
#Create your screen
screen = pygame.display.set_mode((800, 600))
  
#Instantiate our player; right now he's just a rectangle
player = Player()
opponent = Opponent()
#Set background color
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))

#Group the Sprites together
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(opponent)

opponents = pygame.sprite.Group()
opponents.add(opponent)
 
#Create ADDOPPONENT Event
ADDOPPONENT = pygame.USEREVENT + 1

#Set a timer for the ADDOPPONENT Event to occur every 250 milliseconds
pygame.time.set_timer(ADDOPPONENT, 250)
#create game clock, create variable for frames per second (FPS), and get starting time
clock = pygame.time.Clock()
fps = 100 
running = True
while running:
    #set game FPS
    clock.tick(fps)      
    #For loop through the event queue
    for event in pygame.event.get():
        #Check for KEYDOWN event
        #KEYDOWN is a constant defined in pygame.locals, imported earlier
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
            print("Escape")
        #Check for QUIT event; if QUIT, set running to false
        elif event.type == QUIT:
            running = False
            print("QUIT")        
        #Check for the ADDOPPONENT Event; if required, create and add an Opponent Instance
        elif event.type == ADDOPPONENT:
            new_opponent = Opponent()
            opponents.add(new_opponent)
            all_sprites.add(new_opponent)

    #Draw background
    screen.blit(background, (0, 0))
  
    #Get pressed keys
    pressed_keys = pygame.key.get_pressed()
  
    #Update player position
    player.move(pressed_keys)

   #Update the Opponent Instance
    opponents.update()

#Draw all Sprites on the screen
    for entity in all_sprites:
       screen.blit(entity.image, entity.rect)

#Kill the Player Instance if it and an opponent collide
    if pygame.sprite.spritecollideany(player, opponents):
        player.kill()
    pygame.display.flip()
  
#Exit the Game
pygame.quit()
