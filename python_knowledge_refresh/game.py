import pygame
import random
import sys
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Anna's pygame")

vec = pygame.math.Vector2
HEIGHT = 1000
WIDTH = 1000
FPS = 60

smallfont = pygame.font.SysFont('Corbel',35) 
text = smallfont.render('X' , True , (255,255,255) ) 

FramePerSec = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#these need to be imported after initializing the pygame.display
import players
import display
import handlers

drink = pygame.image.load("drink.png").convert_alpha()
burger = pygame.image.load("burger.png").convert_alpha()
exitpng = pygame.image.load("exit.png").convert_alpha()

one_image = pygame.image.load("1.png").convert_alpha()
two_image = pygame.image.load("2.png").convert_alpha()
three_image = pygame.image.load("3.png").convert_alpha()
four_image = pygame.image.load("4.png").convert_alpha()
five_image = pygame.image.load("5.png").convert_alpha()

    #Generating the marks on the board
# 15% - 1
# 50% - 2 
# 20% - 3 
# 10% - 4 
# 5% - 5

def put_marks(number_of_marks, all_sprites, marks):
    for i in range(number_of_marks):
        which = random.randint(0,100)
        if 0 < which <= 60:
            two = Mark(pngname = two_image, value = 2)
            all_sprites.add(two)
            marks.add(two)
     
        if 60 < which <= 70:
            three = Mark(pngname = three_image, value = 3)
            all_sprites.add(three)
            marks.add(three)
       
        if 70 < which <= 85:
            one = Mark(pngname = one_image, value = 1)
            all_sprites.add(one)
            marks.add(one)
        
        if 85 < which <= 95:
            four = Mark(pngname = four_image, value = 4)
            all_sprites.add(four)
            marks.add(four)
        
        if 95 < which:
            five = Mark(pngname = five_image, value = 5)
            all_sprites.add(five)
            marks.add(five)

class Mark(pygame.sprite.Sprite):
    def __init__(self, pngname, value):
        super().__init__() 
        self.surf = pngname
        self.value = value
        self.pos = vec(random.randint(30,screen.get_width()-50), random.randint(30,screen.get_height()-50))
        self.rect = pngname.get_rect(center=(self.pos.x,self.pos.y))
        self.used = False
    
class Booster(pygame.sprite.Sprite):
    def __init__(self, pngname):
        super().__init__() 
        self.surf = pngname
        self.pos = vec(random.randint(30,screen.get_width()-50), random.randint(30,screen.get_height()-50))
        self.rect = pngname.get_rect(center=(self.pos.x,self.pos.y))
        self.used = False

class Burger(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = burger
        self.pos = vec(random.randint(30,screen.get_width()-50), random.randint(30,screen.get_height()-50))
        self.rect = burger.get_rect(center=(self.pos.x,self.pos.y))
        self.used = False
        
class Exit(pygame.sprite.Sprite):
    def __init__(self):
         super().__init__()
         self.surf = exitpng
         self.pos = vec(100, screen.get_height()-40)
         self.rect = exitpng.get_rect(center=(self.pos.x,self.pos.y))
         
class Game():
    def __init__(self):  
         self.level = 1
         self.game_state = "start_menu"
         self.prof_collision_timer = 0 
         
         self.P1 = players.Player()
         self.ex = Exit()
         self.all_sprites = pygame.sprite.Group()
         
         self.all_sprites.add(self.P1)
         self.all_sprites.add(self.ex)
         
         self.marks = pygame.sprite.Group()
         self.boosters = pygame.sprite.Group([Booster(drink) for _ in range(random.randint(0,2))])
         self.burgers = pygame.sprite.Group([Burger() for _ in range(random.randint(2,4))])
         
         self.professors = pygame.sprite.Group([players.Prof() for _ in range(4)])
         
         self.picked_up_items = [] #to only draw them once
         put_marks(random.randint(7,12), self.all_sprites, self.marks)
         
         for i in self.professors:
            self.all_sprites.add(i) 

         for b in self.boosters:
            self.all_sprites.add(b)
           
         for c in self.burgers:
             self.all_sprites.add(c)

levels = []
for i in range(7):                
    game = Game()
    levels.append(game)
averages = []
    
game = levels[0]

burger_effect_duration = 4000
burger_effect_active = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if game.game_state == "start_menu":
            display.draw_start_menu(screen, HEIGHT, WIDTH)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                if WIDTH/2 - 140 <= mouse[0] <= WIDTH/2 + 140 and HEIGHT/2 - 140 <= mouse[1] <= HEIGHT/2 + 140:
                    game.game_state = "running"  # change the game state when the "Start" button is clicked
 
    if game.game_state == "running": 
        
        mouse = pygame.mouse.get_pos()
       
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if HEIGHT-30 <= mouse[0] <= HEIGHT and 0 <= mouse[1] <= 30: 
                pygame.quit() 
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN: 
            if HEIGHT-60 <= mouse[0] <= HEIGHT and 0 <= mouse[1] <= 30 : 
                game.game_state = "paused"
                
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_p]:
             game.game_state = "paused"
      
        handlers.handle_professor_collisions(game)
                    
        game.prof_collision_timer += pygame.time.get_ticks()
    
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if pygame.sprite.collide_rect(game.P1, game.ex) and mouse[0] < 120 and mouse[1] > HEIGHT-120:
                 if len(game.P1.inventory) < 3:
                     game.game_state = "message"
                     
                 else:
                     game.game_state = "semester_x"
                     
    # picking up marks
        handlers.picking_up_marks(game)
                    
      #BOOSTERS             
    # so far it only can be enrgy drink, which increases the speed
        for Booster in game.boosters:
            pressed_keys = pygame.key.get_pressed()
           
            if pygame.sprite.collide_rect(game.P1, Booster) and pressed_keys[pygame.K_g]:
                game.P1.ACC+=0.05
                game.all_sprites.remove(Booster)
                
        if burger_effect_active:
            burger_effect_duration -= 1
            if burger_effect_duration <= 0:
                # Reset professor's speed after the effect duration
                for prof in game.professors:
                    prof.speed = 60
                burger_effect_active = False  # Disable the effect
                burger_effect_duration = 4000
            
        for Burger in game.burgers:
            #pressed_keys = pygame.key.get_pressed()
           for prof in game.professors:
                if pygame.sprite.collide_rect(prof, Burger):
                    burger_effect_active = True               
                    prof.speed = 145
                    game.all_sprites.remove(Burger)
                
        handlers.calculate_motivation(game)
        
        screen.fill((0,0,0))
                
        for entity in game.all_sprites:
            screen.blit(entity.surf, entity.rect)

        display.draw_motivation_bar(game, screen, HEIGHT, WIDTH)
        
        # changing from dark red to lighter red if hovering over the button
        if HEIGHT-30 <= mouse[0] <= HEIGHT and 0 <= mouse[1] <= 30: 
            pygame.draw.rect(screen,(255,0,0) ,[HEIGHT-30,0,30,30]) 
          
        else: 
            pygame.draw.rect(screen,(200,0,0) ,[HEIGHT-30,0,30,30]) 
    
        # the X written on the exit button
        screen.blit(text , (HEIGHT-25,0))  
        
        #drawing the pause button
        if HEIGHT-60 <= mouse[0] <= HEIGHT and 0 <= mouse[1] <= 30: 
            pygame.draw.rect(screen,(50,50,255) ,[HEIGHT-60,0,30,30]) 
          
        else: 
            pygame.draw.rect(screen,(100,100,255) ,[HEIGHT-60,0,30,30]) 
            
        #the II on the pause button
        font = pygame.font.SysFont("Arial", 24)
        text_surface = font.render("l l", True, (255, 255, 255))
        text_rect = text_surface.get_rect(midleft=(HEIGHT-53,14))
        screen.blit(text_surface, text_rect)
        
        # drawing the inventory and the items inside (50 = slot height, width, 10 = spacing)
        inventory_x = (WIDTH - (5 * (50 + 10))) / 2  # Center the inventory horizontally
        inventory_y = HEIGHT - 50 - 10  # Position the inventory at the bottom
    
        for i in range(5):
            slot_rect = pygame.Rect(inventory_x + i * (50 + 10), inventory_y, 50, 50)
            pygame.draw.rect(screen, (150, 150, 150), slot_rect)  # Draw an empty inventory slot
            
        for i, item in enumerate(game.P1.inventory):
                screen.blit(item.surf, (inventory_x + i * (50 + 10), inventory_y))
                
        game.P1.move()

        for prof in game.professors:
                prof.move()
            
        pygame.display.update()
        FramePerSec.tick(FPS)
        
    elif game.game_state == "paused":

        mouse = pygame.mouse.get_pos()
        
        if HEIGHT/2 - 75 <= mouse[0] <= WIDTH/2 + 75 and HEIGHT/2 - 75 <= mouse[1] <= HEIGHT/2 + 75:
            pygame.draw.rect(screen,(100,255,100) ,[HEIGHT/2 - 30, WIDTH/2,75,75]) 
        else:
            pygame.draw.rect(screen,(10,255,10) ,[HEIGHT/2 - 30, WIDTH/2,75,75]) 
        
        if event.type == pygame.MOUSEBUTTONDOWN:
                if HEIGHT/2 - 75 <= mouse[0] <= WIDTH/2 + 75 and HEIGHT/2 - 75 <= mouse[1] <= HEIGHT/2 + 75:
                    game.game_state = "running"

        pygame.display.update()
    	
    elif game.game_state == "message":
         font = pygame.font.Font(None, 48) 
         text_surface = font.render("You must collect at least 3 marks to go to the next semester", True, (255, 0, 0))
         text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

         screen.blit(text_surface, text_rect)
         pygame.display.flip()
         mouse = pygame.mouse.get_pos()
        
         if HEIGHT/2 - 75 <= mouse[0] <= WIDTH/2 + 75 and HEIGHT/2 - 75 <= mouse[1] <= HEIGHT/2 + 75:
            pygame.draw.rect(screen,(100,255,100) ,[HEIGHT/2 - 30, WIDTH/2,75,75]) 
         else:
            pygame.draw.rect(screen,(10,255,10) ,[HEIGHT/2 - 30, WIDTH/2,75,75]) 
        
         if event.type == pygame.MOUSEBUTTONDOWN:
                if HEIGHT/2 - 75 <= mouse[0] <= WIDTH/2 + 75 and HEIGHT/2 - 75 <= mouse[1] <= HEIGHT/2 + 75:
                    game.game_state = "running"

         pygame.display.update()
         
    elif game.game_state == "semester_x":
         
         x = 8 - len(levels)
         if x < 7:  
             font = pygame.font.Font(None, 72) 
             font_smaller = pygame.font.Font(None, 48) 
        
             text_surface = font.render(f"You finished the {x}. semester", True, (255, 255, 0))
             text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 75))

             summ = 0
             for mark in game.P1.inventory:
                 summ += mark.value
         
             avg = round(summ / len(game.P1.inventory), 2)
             averages.append(avg)
         
             text_surface_av = font_smaller.render(f"Your average was: {avg}", True, (255, 255, 0))
             text_rect_av = text_surface_av.get_rect(center=(WIDTH // 2 , HEIGHT // 2 + 120))
         
             screen.blit(text_surface, text_rect)
             screen.blit(text_surface_av, text_rect_av)

             pygame.display.flip()
             mouse = pygame.mouse.get_pos()
        
             if HEIGHT/2 - 75 <= mouse[0] <= WIDTH/2 + 75 and HEIGHT/2 - 75 <= mouse[1] <= HEIGHT/2 + 75:
                pygame.draw.polygon(screen, (255, 255, 255), ((HEIGHT/2-30,WIDTH/2),(HEIGHT/2-30,WIDTH/2 + 80),(HEIGHT/2 + 20, WIDTH/2 + 40)))
             else:
                pygame.draw.polygon(screen, (0, 255, 0), ((HEIGHT/2-30,WIDTH/2),(HEIGHT/2-30,WIDTH/2 + 80),(HEIGHT/2 + 20, WIDTH/2 + 40)))
        
             if event.type == pygame.MOUSEBUTTONDOWN:
                    if HEIGHT/2 - 75 <= mouse[0] <= WIDTH/2 + 75 and HEIGHT/2 - 75 <= mouse[1] <= HEIGHT/2 + 75:
                        game = levels.pop()
                        game.game_state = "running"

             pygame.display.update()
             
         else:
             summa = 0
             
             for av in averages:
                 summa += av
         
             avg = round(summa / len(averages), 2)
             
             font = pygame.font.Font(None, 72) 
             font_smaller = pygame.font.Font(None, 48) 
        
             text_con = font.render(f"CONGRATULATIONS", True, (0, 255, 0))
             text_you = font_smaller.render(f"You got your diploma with the average of {avg}", True, (0, 255, 0))
             screen.blit(display.diploma, ((WIDTH // 2 - 115, 100)))
             
             text_rec= text_con.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 75))
             text_rect = text_you.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
             
             screen.blit(text_con, text_rec)
             screen.blit(text_you, text_rect)
             
             pygame.display.update()