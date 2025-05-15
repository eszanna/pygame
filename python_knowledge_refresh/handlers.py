
import pygame

def handle_professor_collisions(game):
    if game.prof_collision_timer % 5 == 0:
        for prof in game.professors:
            if pygame.sprite.collide_rect(game.P1, prof):
                game.P1.motivation -= 2.5
                game.prof_collision_timer = 0
        if game.P1.motivation < 0:
            game.P1.motivation = 0

def calculate_motivation(game):
    # calculating the motivation
    for mark in game.P1.inventory:  
        if(mark.value == 1 and not mark.used):
            game.P1.motivation -= 15
            mark.used = True
        elif(mark.value == 2 and not mark.used):
            game.P1.motivation -= 10
            mark.used = True
        elif(mark.value == 4 and not mark.used):
           game.P1.motivation += 5
           mark.used = True
        elif(mark.value == 5 and not mark.used):
            game.P1.motivation += 15
            mark.used = True 
        if game.P1.motivation < 0:
            game.P1.motivation = 0
        if game.P1.motivation > 100:
            game.P1.motivation = 100

def picking_up_marks(game):
    for Mark in game.marks:
        pressed_keys = pygame.key.get_pressed()
           
        if pygame.sprite.collide_rect(game.P1, Mark) and pressed_keys[pygame.K_g]:
                
            # only draw it once, which means it is not yet drawn and is not in the list 
            if Mark not in game.picked_up_items and len(game.P1.inventory) < 5:
                game.P1.inventory.append(Mark)
                game.picked_up_items.append(Mark)
                game.all_sprites.remove(Mark) 
                pygame.display.update()
