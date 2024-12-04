import pygame
import random
import time
import sys
import math
import copy

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
CARD_WIDTH, CARD_HEIGHT = 100, 100
BOARD_SIZE = 3
FONT_SIZE = 24
INFO_PANEL_HEIGHT = 100
PLAYER_CARDS_AREA_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# pygame 초기화
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Triple Triad")
font = pygame.font.Font(None, FONT_SIZE)

title_background = pygame.image.load("image/title.png")
title_start_game = pygame.image.load("image/start_game.png")
card_player = pygame.image.load("image/card_player.png")
card_ai = pygame.image.load("image/card_ai.png")
board_background = pygame.image.load("image/board_background2.png")

class Button:  
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action=None):
        mouse = pygame.mouse.get_pos()  
        click = pygame.mouse.get_pressed()  
        if x + width > mouse[0] > x and y + height > mouse[1] > y:  
            screen.blit(img_act, (x_act, y_act))  
            if click[0] and action is not None:  
                time.sleep(0.2)
                action()
        else:
            screen.blit(img_in, (x, y))


# Card class
class Card:
    def __init__(self, top, right, bottom, left, owner):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
        self.owner = owner  # 'player' or 'AI'

    def draw(self, x, y):
        if self.owner == 'player':
            screen.blit(card_player,(x,y))
        else :
            screen.blit(card_ai,(x,y))
        values = [self.top, self.right, self.bottom, self.left]
        positions = [(x + (CARD_WIDTH-20) // 2, y+10),
                     (x + CARD_WIDTH - 30, y + (CARD_HEIGHT-20) // 2),
                     (x + (CARD_WIDTH-20) // 2, y + CARD_HEIGHT - 30),
                     (x + 10, y + (CARD_HEIGHT-20) // 2)]

        for value, pos in zip(values, positions):
            text = font.render(str(value), True, WHITE)
            screen.blit(text, text.get_rect(center=pos))

# Board class
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def draw(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x, y = col * CARD_WIDTH + 150, row * CARD_HEIGHT + INFO_PANEL_HEIGHT + 30
                pygame.draw.rect(screen, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 1,border_radius=10)
                if self.grid[row][col]:
                    self.grid[row][col].draw(x+10, y+10)
         
        pygame.draw.rect(screen, BLACK, (150, 130, CARD_WIDTH*3, CARD_HEIGHT*3), 4,border_radius=10)
        
    def place_card(self, card, row, col):
        if self.grid[row][col] is None:
            self.grid[row][col] = card
            return True
        return False

    def check_control(self, row, col):
        card = self.grid[row][col]
        if not card:
            return

        directions = [(0, -1, "top", "bottom"), (1, 0, "right", "left"),
                      (0, 1, "bottom", "top"), (-1, 0, "left", "right")]

        for dx, dy, my_side, their_side in directions:
            nr, nc = row + dy, col + dx
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                neighbor = self.grid[nr][nc]
                if neighbor and neighbor.owner != card.owner:
                    my_value = getattr(card, my_side)
                    their_value = getattr(neighbor, their_side)

                    if my_value > their_value:
                        neighbor.owner = card.owner
                    elif my_value == their_value:
                        my_sum = card.top + card.right + card.bottom + card.left
                        their_sum = neighbor.top + neighbor.right + neighbor.bottom + neighbor.left
                        if my_sum > their_sum:
                            neighbor.owner = card.owner

    def evaluate(self):
        player_score = sum(1 for row in self.grid for card in row if card and card.owner == 'player')
        ai_score = sum(1 for row in self.grid for card in row if card and card.owner == 'AI')
        return ai_score - player_score


# AI class
class AI:
    def __init__(self, cards, player_cards):
        self.cards = cards
        self.player_cards= player_cards
    def choose_move(self, board):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board.grid[row][col] is None:
                    return random.choice(self.cards), row, col
    
    def choose_move2(self, board):
        best_score = -math.inf
        best_move = None
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board.grid[row][col] is None:
                   for card in (self.cards):
                    backup=copy.deepcopy(board.grid) # 이전 상태의 board 저장
                    board.grid[row][col]=copy.deepcopy(card) # card의 복사본 전달 원본은 건드리면 안됨
                    board.check_control(row,col)
                    score = self.alpha_beta(2, -math.inf, math.inf, False, board)
                    board.grid=copy.deepcopy(backup)

                    if score > best_score:
                            best_score = score
                            best_move = (card, row, col)

        if best_move:
            return best_move
        

    def alpha_beta(self, depth, alpha, beta, maximizing_player, board):
        if depth == 0 or all(cell is not None for row in board.grid for cell in row):
            return board.evaluate()
        if maximizing_player:
            max_eval = -math.inf
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    if board.grid[row][col] is None:
                        for card in (self.cards):
                            backup=copy.deepcopy(board.grid)
                            board.grid[row][col] = copy.deepcopy(card)
                            board.check_control(row,col)
                            eval = self.alpha_beta(depth-1, alpha, beta, False, board)
                            board.grid=copy.deepcopy(backup)
                            max_eval = max(max_eval, eval)
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break
            return max_eval
        else:
            min_eval = math.inf
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    if board.grid[row][col] is None:
                        for card in self.player_cards:
                            backup=copy.deepcopy(board.grid)
                            board.grid[row][col] = copy.deepcopy(card)
                            board.check_control(row,col)
                            eval = self.alpha_beta(depth-1, alpha, beta, True, board)
                            board.grid=copy.deepcopy(backup)
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                break
            return min_eval
        


# Utility function for drawing the info panel
def draw_info_panel(player_cards, ai_cards, player_score, ai_score):
    screen.blit(resize(board_background,0.67),(0,0))
    score_text = font.render(f"Player {player_score} : {ai_score} AI", True, BLACK)
    score_width, score_height= score_text.get_size()
    screen.blit(score_text, (SCREEN_WIDTH/2-score_width/2, INFO_PANEL_HEIGHT-score_height/2))

# Utility function for drawing player's cards
def draw_player_cards(player_cards, selected_card_index):
    start_x = 40
    y = SCREEN_HEIGHT - PLAYER_CARDS_AREA_HEIGHT + 10

    for i, card in enumerate(player_cards):
        x = start_x + i * (CARD_WIDTH + 10)
        if i == selected_card_index:
            pygame.draw.rect(screen, WHITE, (x - 5, y-25, CARD_WIDTH - 10, CARD_HEIGHT - 10), 3)
        card.draw(x, y-20)

# Function to select starting turn
def select_starting_turn():
    selecting = True
    while selecting:
        screen.fill(BLACK)
        text = font.render("Press 1 for First Turn, 2 for Second Turn", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return True
                if event.key == pygame.K_2:
                    return False

def retry():
    selecting = True
    while selecting:
        screen.fill(BLACK)
        text = font.render("Press 1 for Retry, 2 for Exit", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return True
                if event.key == pygame.K_2:
                    return False
                
def difficulty():
    selecting = True
    while selecting:
        screen.fill(BLACK)
        text = font.render("Press 1 for Easy, 2 for Normal, 3 for Hard", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 70
                if event.key == pygame.K_2:
                    return 50
                if event.key == pygame.K_3:
                    return 30

def resize(image, ratio):
    image_width, image_height = image.get_size()
    new_height=ratio * image_height
    new_width=ratio*image_width
    return pygame.transform.scale(image, (new_width, new_height))

# Function to check game result and display it on the board
def display_game_result(player_turn, player_score):
    if player_turn:  # Player went first
        if player_score >= 6:
            result_text = "You win!"
        elif player_score == 5:
            result_text = "Draw!"
        else:
            result_text = "You lose!"
    else:  # Player went second
        if player_score >= 5:
            result_text = "You win!"
        elif player_score == 4:
            result_text = "Draw!"
        else:
            result_text = "You lose!"
    
    # Display the result on the board
    screen.fill(BLACK)  # Clear the screen
    text_surface = font.render(result_text, True, WHITE)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

def title():
    clock = pygame.time.Clock()
    menu = True
    resized_start_game=resize(title_start_game,1.1)
    resized_background= resize(title_background,0.59)
    
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(resized_background,(0,0)) 
        Button(title_start_game, 250, 425, 100, 100, resized_start_game, 245, 420, play)
        pygame.display.update()
        clock.tick(15)

def play():
    diff=difficulty()
    player_turn = select_starting_turn()
    who_is_first = player_turn
    player_cards = [Card(random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), 'player') for _ in range(5 if player_turn else 4)]
    ai_cards = [Card(random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), random.randint(1, 10), 'AI') for _ in range(5 if not player_turn else 4)]
    board = Board()
    ai = AI(ai_cards,player_cards)

    player_score, ai_score = 0, 0
    selected_card_index = 0

    running = True
    while running:
        screen.fill(BLACK)
        draw_info_panel(player_cards, ai_cards, player_score, ai_score)
        board.draw()
        draw_player_cards(player_cards, selected_card_index)
        if player_score + ai_score == 9:
            text = font.render("Click the screen to see the result", True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT - PLAYER_CARDS_AREA_HEIGHT - 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN and player_turn:
                if event.key == pygame.K_LEFT:
                    selected_card_index = max(0, selected_card_index - 1)
                if event.key == pygame.K_RIGHT:
                    selected_card_index = min(len(player_cards) - 1, selected_card_index + 1)
            
            if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                mx, my = pygame.mouse.get_pos()
                row, col = (my - INFO_PANEL_HEIGHT - 30) // CARD_HEIGHT, (mx-150) // CARD_WIDTH

                if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and player_cards:
                    if board.place_card(player_cards[selected_card_index], row, col):
                        player_cards.pop(selected_card_index)
                        selected_card_index = min(selected_card_index, len(player_cards) - 1)
                        board.check_control(row, col)
                        player_turn = False
            
            if player_score + ai_score == 9 and event.type == pygame.MOUSEBUTTONDOWN:
                display_game_result(who_is_first, player_score)
                time.sleep(1.5)
                if(retry()):
                    return
                else:
                    running = False

        if not player_turn and ai_cards:
            time.sleep(1)
            if random.randint(1,100)<=diff: 
                card, row, col = ai.choose_move(board)
            else: 
                card, row, col = ai.choose_move2(board)
        
            if board.place_card(card, row, col):
                ai_cards.remove(card)
                board.check_control(row, col)
                player_turn = True
        
        # Calculate scores
        player_score = sum(1 for row in board.grid for card in row if card and card.owner == 'player')
        ai_score = sum(1 for row in board.grid for card in row if card and card.owner == 'AI')

        pygame.display.flip()
        time.sleep(0.1)
    
    pygame.quit()
    sys.exit()

# Game loop
title()
