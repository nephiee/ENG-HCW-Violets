import pygame
from puzzles.platform import platform
from puzzles.matching import matching
from puzzles.anagram import anagram
from puzzles.maze import maze
from puzzles.jigsaw import jigsaw

# pygame setup 
pygame.init()
width = 900
height = 500
screen = pygame.display.set_mode((width,height))
font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 40)
pygame.display.set_caption("Violets")

clock = pygame.time.Clock()
running = True
#game_states -> [win, lose, playing]
game_state = '1'
current = 1

def menu(type):
    global font, small_font, screen, width, height, clock, running, game_state,current
    next_rect = pygame.Rect(350, height//2 - 40, 200, 50)
    restart_rect = pygame.Rect(350, height//2 + 40, 200, 50)
    quit_rect = pygame.Rect(350, height//2 + 120, 200, 50)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    
    if(type=='win'):
        screen.blit(font.render("You Win!", True, (255, 255, 255)), (330, 130))

        color = (200, 200, 200) if next_rect.collidepoint(mouse) else (255, 255, 255)
        pygame.draw.rect(screen, color, next_rect, border_radius=8)
        text = small_font.render("Next", True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=next_rect.center))
        if next_rect.collidepoint(mouse) and click:
            current+=1
            game_state=str(current)
            return
            
    if(type=='lose'):
        screen.blit(font.render("Game Over", True, (255, 255, 255)), (300, 130))

    for rect, label in [(restart_rect, "Restart"), (quit_rect, "Quit")]:
        color = (200, 200, 200) if rect.collidepoint(mouse) else (255, 255, 255)
        pygame.draw.rect(screen, color, rect, border_radius=8)
        text = small_font.render(label, True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=rect.center))

        if rect.collidepoint(mouse) and click:
            if(label=="Restart"): game_state=str(current)
            elif(label=="Quit"): running=False
    

while running:
    screen.fill((218, 213, 222))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    if(game_state.isnumeric()): 
        if(game_state=='1'):
            game_state=platform(events)
        elif(game_state=='2'):
            game_state=matching(events)
        elif(game_state=='3'):
            game_state=maze(events)
        elif(game_state=='4'):
            game_state=anagram(events)
        elif(game_state=='5'):
            game_state=jigsaw(events)
    elif(game_state=='lose'): 
        menu('lose')
    elif game_state == 'win':
        menu('win')
        
    pygame.display.flip()
    
    #set fps at 60
    clock.tick(60)
