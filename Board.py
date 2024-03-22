# https://www.pngfind.com/mpng/TiximRR_chess-pieces-sprite-chess-pieces-sprite-sheet-hd/
# https://stackoverflow.com/questions/66467383/how-to-draw-a-chessboard-with-pygame-and-move-the-pieces-on-the-board#:~:text=You%20have%20to%20create%20a%20pygame.sprite.Sprite%20object%20for,class%20ChessSprite%28pygame.sprite.Sprite%29%3A%20def%20__init__%28self%2C%20i%2C%20j%2C%20image%29%3A%20super%28%29.__init__%28%29

# James Osborn
# This class incorporates the ChessVar class into an interactable board to play on


# Import the necessary libraries
import pygame
import ChessVar


class DragOperator:
    def __init__(self, sprite):
        self.sprite = sprite
        self.dragging = False
        self.rel_pos = (0, 0)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.dragging = self.sprite.rect.collidepoint(event.pos)
                self.rel_pos = event.pos[0] - self.sprite.rect.x, event.pos[1] - self.sprite.rect.y
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            if event.type == pygame.MOUSEMOTION and self.dragging:
                self.sprite.rect.topleft = event.pos[0] - self.rel_pos[0], event.pos[1] - self.rel_pos[1]


class ChessSprite(pygame.sprite.Sprite):
    def __init__(self, board_rect, i, j, image):
        super().__init__()
        self.board = board_rect
        self.image = image
        self.set_pos(i, j)
        self.drag = DragOperator(self)

    def set_pos(self, i, j):
        x = self.board.left + self.board.width // 8 * i + self.board.width // 16
        y = self.board.left + self.board.height // 8 * (7 - j) + self.board.height // 16
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, event_list):
        self.drag.update(event_list)
        if not self.drag.dragging:
            i = max(0, min(7, (self.rect.centerx - self.board.left) // (self.board.width // 8)))
            j = 7 - max(0, min(7, (self.rect.centery - self.board.top) // (self.board.height // 8)))
            self.set_pos(i, j)


def main():
    pygame.display.init()

    size = 60
    white, black, red = (255, 220, 220), (70, 80, 255), (50, 50, 50)

    # Set up the display window
    screen = pygame.display.set_mode((900, 600))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Falcon-Hunter Chess Variant")
    board = pygame.Surface(screen.get_size())
    board.fill(white)



    boardLength = 8
    screen.fill(red)

    IMAGES = {}
    pieces = ['wp', 'wr', 'wn', 'wb', 'wk', 'wq', 'bp', 'br', 'bn', 'bb', 'bk', 'bq']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(
                            pygame.image.load("ChessPieces/" + piece + ".png"),
                                              (size, size))
    white_pieces = {}
    for i, f in enumerate(['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']):
        white_pieces[f] = ChessSprite(i, 0, IMAGES[f])
    for i in range(8):
        pawn_name = 'wp' + str(i+1)
        white_pieces[pawn_name] = ChessSprite(i, 1, IMAGES['wp'])

    black_pieces = {}
    for i, f in enumerate(['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br']):
        black_pieces[f] = ChessSprite(i, 7, IMAGES[f])
    for i in range(8):
        pawn_name = 'bp' + str(i+1)
        black_pieces[pawn_name] = ChessSprite(i, 6, IMAGES['bp'])

    group = pygame.sprite.Group()
    group.add(white_pieces.values())
    group.add(black_pieces.values())


    count = 0
    for row in range(1, boardLength+1):
        for col in range(1, boardLength+1):
            if count % 2 == 0:
                pygame.draw.rect(screen, white, [size * col, size * row, size, size])
            else:
                pygame.draw.rect(screen, black, [size * col, size * row, size, size])
            count += 1
        count -= 1

    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update display
        pygame.display.flip()

    # Clean up
    pygame.quit()

if __name__ == '__main__':
    main()


