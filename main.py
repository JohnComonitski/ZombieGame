from zombies import Game
import pygame

width, height = 1000, 700
win = pygame.display.set_mode((width, height))
game = Game(win, width, height)

clock = pygame.time.Clock()
pygame.display.set_caption('Zombie Game')

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect()

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            intro=False
                
        win.fill((0,0,0))
        #Title
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Zombie Game", largeText)
        TextRect.center = ((width/2),(height/2))
        win.blit(TextSurf, TextRect)
        #How To Start
        largeText = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = text_objects("(Press SPACE to Start!)", largeText)
        TextRect.center = ((width/2),(height/2)+85)
        win.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(15)

def game_loop():
    run = True 
    while run:
        clock.tick(24)
        game_info = game.next_turn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        if(game_info["alive"]):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                game.change_direction(1)
            elif keys[pygame.K_s]:
                game.change_direction(2)
            elif keys[pygame.K_a]:
                game.change_direction(3)
            elif keys[pygame.K_d]:
                game.change_direction(4)

            game.draw(draw_score=True, draw_textures=True)
            pygame.display.update()
        else:
            run = False

game_intro()
game_loop()
pygame.quit()
quit()