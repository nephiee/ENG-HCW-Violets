import pygame
import random

# --- Setup ---
pygame.init()
width = 900
height = 500
screen = pygame.display.set_mode((width,height))
# --- Colors ---
BG_COLOR = (230, 220, 250)
TEXT_COLOR = (50, 30, 80)
INPUT_COLOR = (255, 255, 255)
RESULT_COLOR = (60, 60, 60)

# --- Fonts ---
font_large = pygame.font.Font(None, 80)
font_med = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 36)
FONT = pygame.font.Font(None, 36)

# --- Word List ---
WORDS = ["FENNEL", "COLUMBINES", "VIOLETS"]
def shuffle_word(word_index):
    global WORDS
    
    word = WORDS[word_index]
    scrambled = list(word)
    while True:
        random.shuffle(scrambled)
        if "".join(scrambled) != word:
            break
    return word, "".join(scrambled)

word_index = 0
random.shuffle(WORDS)
original, scrambled = shuffle_word(word_index)
user_text = ""
message = ""

def anagram(events):
    global BG_COLOR, TEXT_COLOR, INPUT_COLOR, RESULT_COLOR,screen,font_large,font_med,font_small,width,height
    global original, scrambled, user_text, message, word_index
    screen.fill(BG_COLOR)

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_text.upper() == original:
                    message = "✅ Correct!"
                    pygame.time.wait(500)
                    word_index += 1
                    if(word_index >= 3):
                        return 'win'
                    original, scrambled = shuffle_word(word_index)
                    user_text = ""
                else:
                    message = "❌ Try again!"
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.unicode.isalpha():
                user_text += event.unicode.upper()

    # --- Draw UI ---
    # Scrambled word
    scrambled_text = font_large.render(scrambled, True, TEXT_COLOR)
    screen.blit(scrambled_text, scrambled_text.get_rect(center=(width//2, height//3)))

    # Input box
    input_rect = pygame.Rect(width//2 - 150, height//2, 300, 60)
    pygame.draw.rect(screen, INPUT_COLOR, input_rect, border_radius=10)
    pygame.draw.rect(screen, (180, 160, 210), input_rect, 3, border_radius=10)

    # Player text
    text_surface = font_med.render(user_text, True, (TEXT_COLOR))
    screen.blit(text_surface, text_surface.get_rect(center=input_rect.center))

    # Message
    msg_surface = font_small.render(message, True, RESULT_COLOR)
    screen.blit(msg_surface, msg_surface.get_rect(center=(width//2, height - 100)))

    # Hint or instructions
    hint = font_small.render("Type your guess and press Enter", True, (100, 80, 140))
    screen.blit(hint, (width//2 - 180, height - 50))
    
    context = font_small.render("Hint: Think of the flowers Ophelia gives away.", True, (100, 80, 140))
    screen.blit(context, (width//2 - 260, 50))
    
    msg = f"Unscramble the words. Press ESC to skip Stage"
    msg_render = FONT.render(msg, True, TEXT_COLOR)
    screen.blit(msg_render, (10, 10))
    
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "win"
    
    return '4'  

