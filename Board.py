# James Osborn
# This class incorporates the ChessVar class into an interactable board to play on


# Import the necessary libraries
import pygame
import ChessVar
import os
import time


# Constants / Setup
screen_width = 1200
screen_height = int(screen_width * 9 / 16)

fps = 60
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
    run = True

    chess_game = ChessVar.ChessVar()
    draw_board(chess_game._board)

    selected_piece = None
    initial_square = None
    
    while run:
        find_square_from_mouse()
        # Takes a list of events
        for event in pygame.event.get():
            # Checks whether the X in the top right is clicked
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and find_square_from_mouse() != 'Off Board':
                initial_square = find_square_from_mouse()
                row, column = ChessVar.get_board_indexes(initial_square)
                piece = chess_game._board[row][column]
                if '[]' not in piece.get_code():
                    selected_piece = piece
                    piece_square = initial_square
            if event.type == pygame.MOUSEBUTTONUP and selected_piece is not None:
                final_square = find_square_from_mouse()
                if final_square == 'Off Board':
                    final_square = initial_square
                move = chess_game.make_move(initial_square, final_square)
                selected_piece = None
                initial_square = None

        if chess_game.get_game_state() is not 'UNFINISHED':
            player_wins(chess_game)

        draw_board(chess_game._board, selected_piece)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    

def draw_board(board, selected_piece=None):
    screen.fill((0, 0, 0))

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

    rectangle = pygame.Rect((ratio * (8 + 1), screen_height - (ratio * (7 + 1.5)), ratio * 1.5, ratio * 8))
    pygame.draw.rect(screen, falcon_hunter_rectangle_color, rectangle)

    # Draws the pieces
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            color = 'w'
            if piece.get_color() == 'Black':
                color = 'b'
            code = piece.get_code().lower()
            if '[]' not in code:
                dir = os.path.dirname(os.path.realpath(__file__))
                location = dir.strip() + "\\ChessPieces\\".strip() + color.strip() + code.strip() + '.png'.strip()
                img = pygame.image.load(location).convert_alpha()
                img = pygame.transform.scale(img, (ratio, ratio))
                # Checks if a piece is currently being dragged from its position
                if selected_piece == piece and selected_piece is not None and len(find_square_from_mouse()) == 2:
                    x, y = pygame.mouse.get_pos()
                    x -= ratio / 2
                    y -= ratio / 2 
                    print('Selected')
                else:
                    x, y = get_square_location(row, col)
                screen.blit(img, (x, y))


def find_square_from_mouse():
    """Returns what square the mouse is on, or if it's somewhere else"""
    x, y = pygame.mouse.get_pos()
    column = int(x / ratio) - 1
    row = int((screen_height - y) / ratio - 0.5)
    if ChessVar.is_on_board(row, column):
        return ChessVar.get_board_notation(row, column)
    elif 0 <= row <= 7 and 7 <= column <= 10.5:
        print(row, column)
        return 'Falcon/Hunter'
    else:
        return 'Off Board'
    
def get_square_location(row, column):
    """Returns the pixel location of a square on the board"""
    x = ratio * (column + 1)
    y = screen_height - (ratio * (row + 1.5))
    return (x, y)

def player_wins(game):
    screen.fill((0, 0, 0))


if __name__ == '__main__':
    main()


