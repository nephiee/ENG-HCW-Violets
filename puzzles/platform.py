import pygame
import random

pygame.init()
width = 900
height = 500
screen = pygame.display.set_mode((width,height))

FONT = pygame.font.Font(None, 36)
TEXT_COLOR = (40, 40, 60) 

bg = pygame.image.load("../violets/assets/platform/castle2.jpg").convert()
bg = pygame.transform.scale(bg, (width, height))
bg_x1 = 0
bg_x2 = 800 
bg_scroll_speed = 3

oph = pygame.image.load("../violets/assets/platform/1.png").convert_alpha()
oph = pygame.transform.scale(oph, (50,90))
oph_rect = oph.get_rect(midleft=(120, 430))
oph_grav = 0
is_jump = False

guard = pygame.image.load("../violets/assets/platform/guard1.png").convert_alpha()
guard = pygame.transform.scale(guard, (70,110))
guard_rect = guard.get_rect(bottomleft=(500, 480))

enemies_loc_x = []
for x in range (1,11): 
    enemies_loc_x.append(random.randint(300,500)+ (enemies_loc_x[-1] if enemies_loc_x else random.randint(300,500)))
enemies_rect = []
for enemies in enemies_loc_x:
    enemies_rect.append(guard.get_rect(bottomleft=(enemies, 480)))
    
hamlet = pygame.image.load("../violets/assets/platform/hamlet.png").convert_alpha()
hamlet = pygame.transform.scale(hamlet, (70,110))
hamlet_rect = hamlet.get_rect(bottomleft=(enemies_rect[-1].x+1000, 480))
    
hp = 100
collision_strength = [False,0]
game_state = True



def set_states():
    global bg_x1, bg_x2
    global oph_grav, oph_rect, is_jump
    global hp, collision_strength,game_state, enemies_loc_x, enemies_rect, hamlet_rect
    
    bg_x1 = 0
    bg_x2 = 800

    oph_rect = oph.get_rect(midleft=(120, 430))
    oph_grav = 0
    is_jump = False

    hp = 100
    collision_strength = [False,0]
    game_state = True
    
    enemies_loc_x = []
    for x in range (1,11): 
        enemies_loc_x.append(random.randint(300,500)+ (enemies_loc_x[-1] if enemies_loc_x else random.randint(300,500)))
    enemies_rect = []
    for enemies in enemies_loc_x:
        enemies_rect.append(guard.get_rect(bottomleft=(enemies, 480)))
        
    hamlet_rect = guard.get_rect(bottomleft=(enemies_rect[-1].x+1000, 480))


def draw_hp_bar(hp):
    fill = (hp / 100) * 200
    outline_rect = pygame.Rect(80, 42, 200, 20)
    fill_rect = pygame.Rect(80, 42, fill, 20)

    if (hp/100>=0.5): pygame.draw.rect(screen, (0, 255, 0), fill_rect) 
    elif (hp/100>=0.25): pygame.draw.rect(screen, (255, 255, 0), fill_rect) 
    else: pygame.draw.rect(screen, (255, 0, 0), fill_rect) 
    
    hp_font = pygame.font.Font(None, 36)
    hp_text = hp_font.render("HP:", True, (40, 40, 60))
    screen.blit(hp_text, (20,40))
    pygame.draw.rect(screen, (0, 0, 0), outline_rect, 2) 


def platform(events):
    global bg_x1, bg_x2
    global oph_grav,is_jump
    global hp, collision_strength,game_state, enemies_loc_x, enemies_rect
    
    tint = pygame.Surface((width, height), pygame.SRCALPHA) 
    tint.fill((235, 220, 247, 100))
    
    if(game_state==False): set_states()

    if(game_state):
        bg_x1 -= bg_scroll_speed
        bg_x2 -= bg_scroll_speed
        hamlet_rect.x -= 5
        for enemy in enemies_rect:
            enemy.x -= 5

        # reset bg when it reaches border
        if bg_x1 <= -800: bg_x1 = 800
        if bg_x2 <= -800: bg_x2 = 800
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jump:
                    print("jumped")
                    is_jump = True
                    oph_grav = -34
                    

        if is_jump:
            oph_rect.y += oph_grav
            oph_grav += 2
        
        if(oph_grav > 34): is_jump = False 
        
        for enemies in enemies_rect:
            print(oph_rect,enemies)
            if(oph_rect.colliderect(enemies)):
                print("Collision")
                if(collision_strength[0]): collision_strength[1] += 1
                else: collision_strength = [True, 1]
            else:
                if collision_strength[0] == True:
                    hp -= collision_strength[1]*5
                    print(hp)
                    collision_strength = [False, 0]
        
        if abs(oph_rect.x - hamlet_rect.x) < 10:
            game_state = False
            return 'win'
        if(hp<0): 
            game_state = False
            return 'lose'
        
    screen.blit(bg, (bg_x1, 0))
    screen.blit(bg, (bg_x2, 0))
    screen.blit(oph, oph_rect)
    screen.blit(hamlet, hamlet_rect)
    for enemies in enemies_rect:
        screen.blit(guard, enemies)
    screen.blit(tint, (0, 0))
    
    draw_hp_bar(hp)
    
    msg = f"Press Space to avoid the guards and reach Hamlet. Press ESC to skip Stage"
    msg_render = FONT.render(msg, True, TEXT_COLOR)
    screen.blit(msg_render, (10, 10))
    
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = "win"
                return "win"
    
    return '1'