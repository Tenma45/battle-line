import pygame
import math
import re

# Init
pygame.init()
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 960
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Battle Line v.0.1.0")

# Set up fonts and colors
BACKGROUND_COLOR = (50, 30, 20)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BUTTON_COLOR = (100, 100, 255)
TEXT_COLOR = (200, 200, 200)
FONT = pygame.font.Font(None, 96)
RESULT_FONT = pygame.font.Font(None, 300)
LABEL_FONT = pygame.font.Font(None, 24)

RED = (190, 35, 35)
ORANGE = (230, 160, 30)
YELLOW = (210, 210, 70)
GREEN = (80, 180, 80)
BLUE = (50, 150, 200)
PURPLE = (160, 100, 220)
BROWN = (120, 70, 30)
GRAY = (60, 60, 60)

CARD_WIDTH = 80
CARD_HEIGHT = 120
BORDER_WIDTH = 2
LANE_WIDTH = 80
LANE_HEIGHT = 280

TROOP_X = 1020
TROOP_Y = 380
TACTIC_X = 1120
TACTIC_Y = 380

card_color_dict = {0:RED,1:ORANGE,2:YELLOW,3:GREEN,4:BLUE,5:PURPLE}
back_card_color_dict = {1:GRAY,2:BROWN}

board_layout =   [[(100, 100),(200, 100),(300, 100),(400, 100),(500, 100),(600, 100),(700, 100),(800, 100),(900, 100)],
           [(100, 180),(200, 180),(300, 180),(400, 180),(500, 180),(600, 180),(700, 180),(800, 180),(900, 180)],
           [(100, 260),(200, 260),(300, 260),(400, 260),(500, 260),(600, 260),(700, 260),(800, 260),(900, 260)],
           [(100, 500),(200, 500),(300, 500),(400, 500),(500, 500),(600, 500),(700, 500),(800, 500),(900, 500)],
           [(100, 580),(200, 580),(300, 580),(400, 580),(500, 580),(600, 580),(700, 580),(800, 580),(900, 580)],
           [(100, 660),(200, 660),(300, 660),(400, 660),(500, 660),(600, 660),(700, 660),(800, 660),(900, 660)],
]

lane_layout =   [(100, 100),(200, 100),(300, 100),(400, 100),(500, 100),(600, 100),(700, 100),(800, 100),(900, 100),
                 (100, 500),(200, 500),(300, 500),(400, 500),(500, 500),(600, 500),(700, 500),(800, 500),(900, 500)]

hand_layout = [(200, 800),(300, 800),(400, 800),(500, 800),(600, 800),(700, 800),(800, 800)]

enemy_layout = [(200, -40),(300, -40),(400, -40),(500, -40),(600, -40),(700, -40),(800, -40)]

pin_layout = [(140, 440),(240, 440),(340, 440),(440, 440),(540, 440),(640, 440),(740, 440),(840, 440),(940, 440),]

def lobby(state):
    background = pygame.image.load("./assets/background.jpg").convert()
    background.set_alpha(50)
    # Clear the screen
    screen.blit(background, (0, 0))
    # draw rectangle and argument passed which should
    # be on screen
    input_rect = pygame.Rect(200, 200, 600, 70)
    pygame.draw.rect(screen, WHITE, input_rect)
  
    text_surface = FONT.render(state["port"], True, BLACK)
      
    # render at position stated in arguments
    screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
    
    label = "Port/server (AAAAA/B)"
    label_surface = LABEL_FONT.render(label, True, WHITE)
    label_rect = label_surface.get_rect()
    label_rect.topleft = (200,160)
    screen.blit(label_surface, label_rect)

    pattern = re.compile((".{5}\/.{1}"))
    start_button_color = GREEN if pattern.match(state["port"]) else GRAY
    start_button = pygame.Rect(200, 300, 160, 80)
    pygame.draw.rect(screen, start_button_color, start_button)
    label = "Join"
    label_surface = FONT.render(label, True, WHITE)
    label_rect = label_surface.get_rect()
    label_rect.topleft = (210,310)
    screen.blit(label_surface, label_rect)
    return None, None, None, None, start_button

def render(state):

    board = state["board"]
    hand = state["you"]
    enemy = state["enemy"]
    troop = state["troop"]
    tactic = state["tactic"]
    pins = state["pins"]
    result = state["result"]
    player = state["player"]
    status = state["status"]
    select_card = state["select_card"]
    
    background = pygame.image.load("./assets/background.jpg").convert()
    background.set_alpha(50)
    # Clear the screen
    screen.blit(background, (0, 0))
    
    # create a surface object, image is drawn on it.
    imp = pygame.image.load("./assets/rule.png").convert()
    
    # Using blit to copy content from one surface to other
    screen.blit(imp, (1020, 520))

    lanes = []
    for index, lane in enumerate(lane_layout):
        pygame.draw.rect(screen, BLACK, (lane[0] - BORDER_WIDTH, lane[1] - BORDER_WIDTH, LANE_WIDTH + 2 * BORDER_WIDTH, LANE_HEIGHT + 2 * BORDER_WIDTH))
        lane_rect = pygame.Rect((lane[0], lane[1], LANE_WIDTH, LANE_HEIGHT))
        lanes.append((lane_rect,index))
        pygame.draw.rect(screen, BACKGROUND_COLOR, lane_rect)

    for row, row_layout in zip(board,board_layout):
        for card, position in zip(row, row_layout):
            if card != 0:
                first_digit = math.floor((card-1)/10)
                rect_color = card_color_dict[first_digit]
                pygame.draw.rect(screen, BLACK, (position[0] - BORDER_WIDTH, position[1] - BORDER_WIDTH, CARD_WIDTH + 2 * BORDER_WIDTH, CARD_HEIGHT + 2 * BORDER_WIDTH))
                pygame.draw.rect(screen, rect_color, (position[0], position[1], CARD_WIDTH, CARD_HEIGHT))
                label = str(card%10) if card%10 != 0 else str(10)
                label_surface = FONT.render(label, True, WHITE)
                label_rect = label_surface.get_rect()
                label_rect.topleft = (position[0]+20, position[1]+30) if label != "10" else (position[0]+1, position[1]+30)

                # Blit (draw) the label surface onto the screen
                screen.blit(label_surface, label_rect)

    hands = []
    for card, position in zip(hand, hand_layout):
        if card != 0:
            if card <= 60:
                first_digit = math.floor((card-1)/10)
                rect_color = card_color_dict[first_digit]
                border = pygame.Rect(position[0] - BORDER_WIDTH, position[1] - BORDER_WIDTH, CARD_WIDTH + 2 * BORDER_WIDTH, CARD_HEIGHT + 2 * BORDER_WIDTH)
                border_color = WHITE if select_card == card else BLACK
                pygame.draw.rect(screen, border_color, border)
                card_rect = pygame.Rect(position[0], position[1], CARD_WIDTH, CARD_HEIGHT)
                hands.append((card_rect,card))
                pygame.draw.rect(screen, rect_color, card_rect)
                label = str(card%10) if card%10 != 0 else str(10)
                label_surface = FONT.render(label, True, WHITE)
                label_rect = label_surface.get_rect()
                label_rect.topleft = (position[0]+20, position[1]+30) if label != "10" else (position[0]+1, position[1]+30)
            else:
                imp = pygame.image.load("./assets/card61.png").convert()
                image = pygame.transform.scale(imp, (CARD_WIDTH,CARD_HEIGHT))
                border = pygame.Rect(position[0] - BORDER_WIDTH, position[1] - BORDER_WIDTH, CARD_WIDTH + 2 * BORDER_WIDTH, CARD_HEIGHT + 2 * BORDER_WIDTH)
                border_color = WHITE if select_card == card else BLACK
                pygame.draw.rect(screen, border_color, border)
                screen.blit(image, (position[0], position[1]))

            # Blit (draw) the label surface onto the screen
            screen.blit(label_surface, label_rect)

    for card, position in zip(enemy, enemy_layout):
        if card != 0:
            rect_color = back_card_color_dict[card]
            pygame.draw.rect(screen, BLACK, (position[0] - BORDER_WIDTH, position[1] - BORDER_WIDTH, CARD_WIDTH + 2 * BORDER_WIDTH, CARD_HEIGHT + 2 * BORDER_WIDTH))
            pygame.draw.rect(screen, rect_color, (position[0], position[1], CARD_WIDTH, CARD_HEIGHT))

    rect_color = back_card_color_dict[1]
    troop_rect = pygame.Rect(TROOP_X - BORDER_WIDTH, TROOP_Y - BORDER_WIDTH, CARD_WIDTH + 2 * BORDER_WIDTH, CARD_HEIGHT + 2 * BORDER_WIDTH)
    pygame.draw.rect(screen, BLACK, troop_rect)
    pygame.draw.rect(screen, rect_color, (TROOP_X, TROOP_Y, CARD_WIDTH, CARD_HEIGHT))
    label = str(troop)
    label_surface = FONT.render(label, True, WHITE)
    label_rect = label_surface.get_rect()
    label_rect.topleft = (TROOP_X+1, TROOP_Y+30) if troop >= 10 else (TROOP_X+20, TROOP_Y+30)
    screen.blit(label_surface, label_rect)

    rect_color = back_card_color_dict[2]
    tactic_rect = pygame.Rect(TACTIC_X - BORDER_WIDTH, TACTIC_Y - BORDER_WIDTH, CARD_WIDTH + 2 * BORDER_WIDTH, CARD_HEIGHT + 2 * BORDER_WIDTH)
    pygame.draw.rect(screen, BLACK, tactic_rect)
    pygame.draw.rect(screen, rect_color, (TACTIC_X, TACTIC_Y, CARD_WIDTH, CARD_HEIGHT))
    label = str(tactic)
    label_surface = FONT.render(label, True, WHITE)
    label_rect = label_surface.get_rect()
    label_rect.topleft = (TACTIC_X+1, TACTIC_Y+30) if tactic >= 10 else (TACTIC_X+20, TACTIC_Y+30)
    screen.blit(label_surface, label_rect)

    # pygame.draw.rect(screen, BLACK, (100,440,900,2))
    
    for pin, position in zip(pins,pin_layout):
        shift_y = 0 if pin == 0 else 30 if pin == player else -30
        pin_border = BACKGROUND_COLOR if pin == 0 else WHITE if pin == player else BLACK
        pin_border_size = 15
        pygame.draw.circle(screen, pin_border, (position[0],position[1]+shift_y),pin_border_size)
        pygame.draw.circle(screen, RED, (position[0],position[1]+shift_y),13)

    if result == "win" or result == "lose":
        label = "You "+result
        label_surface = RESULT_FONT.render(label, True, WHITE)
        label_rect = label_surface.get_rect()
        label_rect.topleft = (200, 350)
        screen.blit(label_surface, label_rect)

    label = "status: "+status
    label_surface = LABEL_FONT.render(label, True, WHITE)
    label_rect = label_surface.get_rect()
    label_rect.topleft = (1015, 860)
    screen.blit(label_surface, label_rect)

    start_button_color = GREEN if status == "Ready to start" else GRAY
    start_button = pygame.Rect(1015, 880, 80, 40)
    pygame.draw.rect(screen, start_button_color, start_button)
    label = "Start"
    label_surface = LABEL_FONT.render(label, True, WHITE)
    label_rect = label_surface.get_rect()
    label_rect.topleft = (1025,890)
    screen.blit(label_surface, label_rect)

    return hands, lanes, troop_rect,tactic_rect, start_button