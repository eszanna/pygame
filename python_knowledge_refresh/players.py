import pygame
import random
from pygame.locals import *

vec = pygame.math.Vector2

prof_image = pygame.image.load("prof.png").convert_alpha()
player_image = pygame.image.load("undergraduate.png").convert_alpha()
player_image_left = pygame.image.load("undergraduate_left.png").convert_alpha()
flipped_prof = pygame.transform.flip(prof_image, True, False)
dead = pygame.image.load("dead.png").convert_alpha()

HEIGHT = 1000
WIDTH = 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Prof(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = prof_image
        self.rect = self.surf.get_rect(center=(0, 0))
        self.ACC = 7
        self.pos = vec(random.randint(30, screen.get_width()-50), random.randint(30, screen.get_height()-50))
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        self.direction_timer = 0
        self.speed = 60
        self.FRIC = -0.08

    def move(self):
        self.direction_timer += 1

        if self.direction_timer >= self.speed:  # 1 second (assuming 60 FPS)
            self.direction_timer = 0
            
            random_direction = random.choice(["left", "right", "up", "down"])
            if random_direction == "left":
                self.surf = prof_image
                self.acc.x = -self.ACC              
            elif random_direction == "right":
                self.acc.x = self.ACC               
                self.surf = flipped_prof
            elif random_direction == "up":
                self.acc.y = -self.ACC
            elif random_direction == "down":
                self.acc.y = self.ACC
        else:
            self.acc.x = 0
            self.acc.y = 0
            
        self.acc.x += self.vel.x * self.FRIC
        self.acc.y += self.vel.y * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        self.pos.x = max(0, min(self.pos.x, WIDTH-50))
        self.pos.y = max(0, min(self.pos.y, HEIGHT-50))

        screen_rect = pygame.display.get_surface().get_rect()
        self.rect.midbottom = self.pos
        self.rect.clamp_ip(screen_rect)
          
        
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__() 
        self.surf = player_image
        self.rect = player_image.get_rect(center=(0,0))
        self.motivation = 100
        self.inventory = []
        self.dead = False
        self.ACC = 0.4
        self.FRIC = -0.08
        
        self.pos = vec((10, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
    def move(self):
        if self.motivation <= 0:
            self.dead = True
            self.surf = dead
            return
        
        self.acc = vec(0,0)
 
        pressed_keys = pygame.key.get_pressed()
            
        if pressed_keys[K_LEFT] or pressed_keys[pygame.K_a]:
            self.acc.x = -self.ACC
            self.surf = player_image_left
            
        if pressed_keys[K_RIGHT] or pressed_keys[pygame.K_d]:
            self.acc.x = self.ACC
            self.surf = player_image
            
        if pressed_keys[K_UP] or pressed_keys[pygame.K_w]:
            self.acc.y = -self.ACC
            
        if pressed_keys[K_DOWN] or pressed_keys[pygame.K_s]:
            self.acc.y = self.ACC
            
        self.acc.x += self.vel.x * self.FRIC
        self.acc.y += self.vel.y * self.FRIC
        
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        self.pos.x = max(0, min(self.pos.x, WIDTH-50))
        self.pos.y = max(0, min(self.pos.y, HEIGHT-50))
    
        screen_rect = screen.get_rect()
        self.rect.midbottom = self.pos
        self.rect.clamp_ip(screen_rect)
        
