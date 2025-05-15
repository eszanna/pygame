import pygame

titlepic = pygame.image.load("title.png").convert_alpha()
diploma = pygame.image.load("diploma.png").convert_alpha()
flipped_diploma = pygame.transform.flip(diploma, True, False)

def draw_start_menu(screen, HEIGHT, WIDTH):

    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('Corbel', 40)
    start_button_text = font.render('Click to start', True, (0, 255, 0))
    
    #play button triangle
    pygame.draw.polygon(screen, (255, 255, 255), ((HEIGHT/2-30,WIDTH/2),(HEIGHT/2-30,WIDTH/2 + 80),(HEIGHT/2 + 20, WIDTH/2 + 40)))
    
    title_x = WIDTH / 2 - titlepic.get_width() / 2
    title_y = HEIGHT / 2 - titlepic.get_height() / 2

    # Blit the title image
    screen.blit(titlepic, (title_x, title_y - 200))
    screen.blit(diploma, ((title_x - 225, title_y)))
    screen.blit(flipped_diploma, ((title_x + 435, title_y)))

    screen.blit(start_button_text, (WIDTH / 2 - 100, HEIGHT / 2 + 100))
    pygame.display.update()


def draw_motivation_bar(game, screen, HEIGHT, WIDTH):
    font = pygame.font.SysFont("Arial", 20)
    text_surface = font.render(f"Motivation: {game.P1.motivation}%", True, (255, 255, 255))
    text_rect = text_surface.get_rect(midleft=(WIDTH - 200, 15))
    screen.blit(text_surface, text_rect)
    
    if(game.P1.motivation >= 90):
            pygame.draw.rect(screen,(0,255,0) ,[WIDTH-250,30,250,30]) 
            
    elif(game.P1.motivation < 90 and game.P1.motivation >= 80):
            pygame.draw.rect(screen,(60,255,0) ,[WIDTH-225,30,225,30]) 
            
    elif(game.P1.motivation < 80 and game.P1.motivation >= 70):
            pygame.draw.rect(screen,(120,255,0) ,[WIDTH-200,30,200,30])
            
    elif(game.P1.motivation < 70 and game.P1.motivation >= 60):
            pygame.draw.rect(screen,(255,255,0) ,[WIDTH-175,30,175,30]) 
            
    elif(game.P1.motivation < 60 and game.P1.motivation >= 50):
            pygame.draw.rect(screen,(255,255,0) ,[WIDTH-150,30,150,30]) 
            
    elif(game.P1.motivation < 50 and game.P1.motivation >= 40):
            pygame.draw.rect(screen,(255,200,0) ,[WIDTH-125,30,125,30]) 

    elif(game.P1.motivation < 40 and game.P1.motivation >= 30):
            pygame.draw.rect(screen,(255,165,0) ,[WIDTH-100,30,100,30]) 
            
    elif(game.P1.motivation < 30 and game.P1.motivation >= 20):
            pygame.draw.rect(screen,(255,0,0) ,[WIDTH-75,30,75,30]) 
            
    elif(game.P1.motivation < 20):
            pygame.draw.rect(screen,(255,0,0) ,[WIDTH-50,30,50,30]) 


