# James Osborn
# This class incorporates the ChessVar class into an interactable board to play on
# Sounds from https://pixabay.com/


# Import the necessary libraries
import pygame
import ChessVar
import os
import time


# Constants / Setup
screen_width = 1800
screen_height = int(screen_width * 9 / 16)

fps = 120
clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Falcon-Hunter Chess')

black_square_color = (73, 97, 209)
white_square_color = (240, 240, 200)
falcon_hunter_rectangle_color = (150, 200, 255)

ratio = screen_width / 16


def main():
    
    # Creates the game object
    pygame.init()
    pygame.font.init()
    run = True

    chess_game = ChessVar.ChessVar()
    draw_board(chess_game)

    selected_piece = None
    initial_square = None

    click_sound = get_sound('click')
    unable_sound = get_sound('unable')
    ding_sound = get_sound('ding')

    time_of_last_frame = 0

    white_timer = 300
    black_timer = 300

    while run:
        # Takes a list of events
        for event in pygame.event.get():
            # Checks whether the X in the top right is clicked
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = find_square_from_mouse()   
                if len(mouse_position) == 2:    
                    initial_square = find_square_from_mouse()
                    row, column = ChessVar.get_board_indexes(initial_square)
                    piece = chess_game._board[row][column]
                    if '[]' not in piece.get_code():
                        selected_piece = piece
                        piece_square = initial_square
                elif len(mouse_position) == 1:
                    selected_piece = mouse_position


            if event.type == pygame.MOUSEBUTTONUP and selected_piece is not None:
                final_square = find_square_from_mouse()
                print(final_square)
                if final_square == 'Off Board' or len(final_square) != 2:
                    pygame.mixer.Sound.play(unable_sound)
                elif type(selected_piece) is str:
                    move = chess_game.enter_fairy_piece(selected_piece, final_square)
                    if move:
                        pygame.mixer.Sound.play(ding_sound)
                else:
                    move = chess_game.make_move(initial_square, final_square)
                    if move:
                        pygame.mixer.Sound.play(click_sound)
                selected_piece = None
                initial_square = None

        if chess_game.get_game_state() is not 'UNFINISHED':
            player_wins(chess_game)
        else:
            draw_board(chess_game, selected_piece)

        time_of_last_frame, white_timer, black_timer = manage_timers(chess_game._player_turn, time_of_last_frame, white_timer, black_timer)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    

def draw_board(chess_game, selected_piece=None):
    screen.fill((0, 0, 0))

    board = chess_game._board

    # Draws the board
    for row in range(8):
        for column in range(8):
            color = ''
            if (row + column) % 2 == 0:
                color = black_square_color
            else:
                color = white_square_color
            square = pygame.Rect((ratio * (column + 1), screen_height - (ratio * (row + 1.5)), ratio, ratio))
            pygame.draw.rect(screen, color, square)
    # Draws the background rectangle for the fairy pieces
    rectangle = pygame.Rect((ratio * (8 + 1), screen_height - (ratio * (7 + 1.5)), ratio * 1.5, ratio * 8))
    pygame.draw.rect(screen, falcon_hunter_rectangle_color, rectangle)

    # Draws the board pieces
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            color = 'w'
            if piece.get_color() == 'Black':
                color = 'b'
            code = piece.get_code().lower()
            if '[]' not in code:
                img = make_image(color, code)
                # Checks if a piece is currently being dragged from its position
                if selected_piece == piece and selected_piece is not None and len(find_square_from_mouse()) == 2:
                    x, y = pygame.mouse.get_pos()
                    x -= ratio / 2
                    y -= ratio / 2
                else:
                    x, y = get_square_location(row, col)
                screen.blit(img, (x, y))

    # Draws the Falcons/Hunters
    # Messy and repetitive
    x, y
    if chess_game._white_hunter == False:
        if selected_piece == 'H':
            x, y = pygame.mouse.get_pos()
            x, y = x - ratio / 2, y - ratio / 2
        else:
            x, y = ratio * 9.25, screen_height - (ratio * 1.5)
        img = make_image('w', 'h')
        screen.blit(img, (x, y))
    if chess_game._white_falcon == False:
        if selected_piece == 'F':
            x, y = pygame.mouse.get_pos()
            x, y = x - ratio / 2, y - ratio / 2
        else:
            x, y = ratio * 9.25, screen_height - (ratio * 2.5)
        img = make_image('w', 'f')
        screen.blit(img, (x, y))
    if chess_game._black_hunter == False:
        if selected_piece == 'h':
            x, y = pygame.mouse.get_pos()
            x, y = x - ratio / 2, y - ratio / 2
        else:
            x, y = ratio * 9.25, screen_height - (ratio * 8.5)
        img = make_image('b', 'h')
        screen.blit(img, (x, y))
    if chess_game._black_falcon == False:
        if selected_piece == 'f':
            x, y = pygame.mouse.get_pos()
            x, y = x - ratio / 2, y - ratio / 2
        else:
            x, y = ratio * 9.25, screen_height - (ratio * 7.5)
        img = make_image('b', 'f')
        screen.blit(img, (x, y))
        

def find_square_from_mouse():
    """Returns what square the mouse is on, or if it's somewhere else"""
    x, y = pygame.mouse.get_pos()
    column = int(x / ratio) - 1
    row = int((screen_height - y) / ratio - 0.5)
    if ChessVar.is_on_board(row, column):
        return ChessVar.get_board_notation(row, column)
    elif 7 <= column <= 10.5:
        if row == 0:
            return 'H'
        elif row == 1:
            return 'F'
        elif row == 6:
            return 'f'
        elif row ==7:
            return 'h'
    return 'Off Board'
    
def get_square_location(row, column):
    """Returns the pixel location of a square on the board"""
    x = ratio * (column + 1)
    y = screen_height - (ratio * (row + 1.5))
    return (x, y)

def player_wins(game):
    screen.fill((0, 0, 0))

def make_image(color, code):
    """Initializes image of pieces with the given color and piece code"""
    code = code.lower()
    dir = os.path.dirname(os.path.realpath(__file__))
    location = dir.strip() + "\\ChessPieces\\".strip() + color.strip() + code.strip() + '.png'.strip()
    img = pygame.image.load(location).convert_alpha()
    img = pygame.transform.scale(img, (ratio, ratio))
    return img

def get_sound(name):
    """Initializes sounds with given name"""
    dir = os.path.dirname(os.path.realpath(__file__))
    location = dir.strip() + "\\Sounds\\".strip() + name.strip() + '.mp3'.strip()
    sound = pygame.mixer.Sound(location)
    return sound

def manage_timers(player_turn, time_of_last_frame, white_timer, black_timer):
    # Finds the time elapsed since previous frame
    time_since_last_frame = pygame.time.get_ticks() - time_of_last_frame
    font = pygame.font.SysFont('Noto Sans', int(ratio * 1.5))

    white_timer_text = font.render(str(int(white_timer)), False, (255, 255, 255))
    screen.blit(white_timer_text, (ratio * 12, screen_height - (ratio * 3)))

    black_timer_text = font.render(str(int(black_timer)), False, (255, 255, 255))
    screen.blit(black_timer_text, (ratio * 12, screen_height - (ratio * 7)))

    # Checks which player's turn is currently ongoing
    if player_turn == 'White':
        white_timer -= time_since_last_frame / 1000
    else:
        black_timer -= time_since_last_frame / 1000

    return pygame.time.get_ticks(), white_timer, black_timer

if __name__ == '__main__':
    main()


