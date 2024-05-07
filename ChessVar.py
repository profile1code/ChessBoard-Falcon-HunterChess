# Author: James Osborn
# GitHub username: profile1code
# Date: 3/15/24
# Description: Class contains functionality to run a special variant of chess. Contains
#              classes including a ChessVar which runs the board and keeps track of the
#              pieces, and classes related to all of the pieces and an EmptySquare class
#              for squares that are empty.


import Board

class ChessVar:
    """Contains functions that are able to run a special variant of chess, keep track
    of the board, and decide when someone wins the game. Works with all of the piece classes,
    as well as an EmptySquare class, which are the pieces that are actually on the board."""
    def __init__(self):
        self._player_turn = 'White'
        self._board = None
        self.initialize_board()
        self._game_state = 'UNFINISHED'
        # Keeps track of whether each side has used their falcon/hunter or not
        self._white_falcon, self._white_hunter = False, False
        self._black_falcon, self._black_hunter = False, False
        self._white_pieces_lost = 0
        self._black_pieces_lost = 0

    def get_game_state(self):
        """Returns whether if the game is over, and if so, who won the game."""
        return self._game_state

    def make_move(self, moved_from, moved_to):
        """Takes a square the piece will move from and the target square,
        and executes the move if it is deemed legal, returning True in the process
        while updating the player turn. If not, then returns False"""
        moved_from, moved_to = moved_from.upper(), moved_to.upper()
        if moved_from == moved_to or self.get_game_state() != 'UNFINISHED':
            return False
        to_row, to_col = get_board_indexes(moved_to)
        from_row, from_col = get_board_indexes(moved_from)
        # Checks to see if the inputted board squares are valid
        if not (is_on_board(to_row, to_col) and is_on_board(from_row, from_col)):
            return False

        moved_object = self.search_square(moved_from)
        removed_object = self.search_square(moved_to)
        if moved_object.get_color() is not self._player_turn:  # Player must move pieces of their own color
            return False
        if not moved_object.is_legal_move(self, moved_to):  # Looks for legal moves for each piece
            return False
        moved_object.set_position(moved_to)
        self._board[to_row][to_col] = moved_object
        self._board[from_row][from_col] = self.make_new_piece('E', moved_from)
        # Adds to the taken pieces for each color for tracking
        if removed_object.get_code() != " []" and removed_object.get_code().upper() != " P ":
            if self._player_turn == "White":
                self._black_pieces_lost += 1
            else:
                self._white_pieces_lost += 1
            # Updates whether either player won the game
            if removed_object.get_code() == ' K ':
                self._game_state = 'BLACK_WON'
            elif removed_object.get_code() == ' k ':
                self._game_state = 'WHITE_WON'

        self.update_player_turn()

        return True
    
    def set_game_state(self, state):
        self._game_state = state

    def search_square(self, square):
        """Takes a square and returns the object type that is currently there."""
        row, column = get_board_indexes(square)
        return self._board[row][column]

    def enter_fairy_piece(self, piece_type, square_entered):
        """Takes a type of fairy piece (black/white hunter/falcon) and executes a
        move onto the board by that piece if it is deemed legal. Otherwise returns false."""
        if self.get_game_state() != 'UNFINISHED':
            return False
        row, col = get_board_indexes(square_entered)
        color = get_color(piece_type)
        square = self.search_square(square_entered)
        if square.get_code() == ' []':  # Square must be empty
            if color == "White":
                if self._white_pieces_lost > 0 and self._player_turn == 'White':
                    if 0 <= row <= 1:
                        # White hunter
                        if piece_type == 'H' and self._white_hunter is False:
                            piece = self.make_new_piece('H', square_entered)
                            self._board[row][col] = piece
                            self._white_pieces_lost -= 1  # Means current on board pieces must have been taken
                            self.update_player_turn()
                            self._white_hunter = True
                            return True
                        # White falcon
                        elif piece_type == 'F' and self._white_falcon is False:
                            piece = self.make_new_piece('F', square_entered)
                            self._board[row][col] = piece
                            self._white_pieces_lost -= 1
                            self.update_player_turn()
                            self._white_falcon = True
                            return True
            else:
                if self._black_pieces_lost > 0 and self._player_turn == 'Black':
                    if 6 <= row <= 7:
                        # Black hunter
                        if piece_type == 'h' and self._black_hunter is False:
                            piece = self.make_new_piece('h', square_entered)
                            self._board[row][col] = piece
                            self._black_pieces_lost -= 1
                            self.update_player_turn()
                            self._black_hunter = True
                            return True
                        # Black falcon
                        elif piece_type == 'f' and self._black_falcon is False:
                            piece = self.make_new_piece('f', square_entered)
                            self._board[row][col] = piece
                            self._black_pieces_lost -= 1
                            self.update_player_turn()
                            self._black_falcon = True
                            return True
        return False

    def print_board(self):
        """Prints the board out for testing purposes, with the bottom left square being A1"""
        for row in range(7, -1, -1):
            row_string = ''
            for column in range(8):
                row_string += self._board[row][column].get_code() + ' '
            print(row_string + '\n')

    def update_player_turn(self):
        """Changes the player turn to the other player."""
        if self._player_turn == "White":
            self._player_turn = "Black"
        else:
            self._player_turn = "White"

    def initialize_board(self):
        """Sets up the board in the initial position for the game"""
        empty_array = [[n for n in range(8)] for m in range(8)]
        # This is a string containing the initial object that needs to be in each square
        set_string = "RNBQKBNR" + "P" * 8 + "e" * 32 + "p" * 8 + "rnbqkbnr"
        for row in range(8):
            for column in range(8):
                board_index = (row * 8) + column
                letter = set_string[board_index]
                empty_array[row][column] = self.make_new_piece(letter, get_board_notation(row, column))
        self._board = empty_array

    def make_new_piece(self, given_letter, position):
        """Takes a coded letter and position of a piece, and returns a piece object
        with the color and position."""
        color = ''
        if given_letter.isupper():
            color = "White"
        else:
            color = "Black"
        piece_maker = {  # Contains functionality to make each type of piece depending on the
                         # passed in key
            'K': King(position, color),
            'Q': Queen(position, color),
            'B': Bishop(position, color),
            'N': Knight(position, color),
            'R': Rook(position, color),
            'P': Pawn(position, color),
            'F': Falcon(position, color),
            'H': Hunter(position, color),
            'E': EmptySquare(position)
        }
        return piece_maker[given_letter.upper()]


class Helper:

    def __init__(self, position, color):
        self._position = position
        self._color = color

    def get_position(self):
        """Returns the position of the square."""
        return self._position

    def get_color(self):
        """Returns the color of the square."""
        return self._color

    def set_position(self, position):
        """Sets the position of the square to the given position."""
        self._position = position

    def set_color(self, color):
        """Sets the color of the square to the given color."""
        self._color = color


class King(Helper):
    """Contains functionality for the King piece on the board. Works with the ChessVar class
    as this is the blueprint for the King that goes on the ChessVar board."""

    def get_code(self):
        """Returns a printable version of the piece for display on the board."""
        return get_colored_key(" K ", self._color)

    def is_legal_move(self, board, target):
        """Takes the board and a target square and returns whether or not the piece can move to
        the given target"""
        current_row, current_column = get_board_indexes(self._position)
        # All possible moves for the King relative to the starting position (all 1 square moves)
        relative_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        possible_squares = []
        for row_mod, col_mod in relative_moves:
            new_row = current_row + row_mod
            new_col = current_column + col_mod
            if is_on_board(new_row, new_col):
                target_square = board.search_square(get_board_notation(new_row, new_col))
                if get_color(target_square.get_code()) != self._color:
                    possible_squares.append(get_board_notation(new_row, new_col))

        return target.upper() in possible_squares


class Queen(Helper):
    """Contains functionality for the Queen piece on the board. Works with the ChessVar class
        as this is the blueprint for the Queen that goes on the ChessVar board."""

    def get_code(self):
        """Returns a printable version of the piece for display on the board."""
        return get_colored_key(" Q ", self._color)

    def is_legal_move(self, board, target):
        """Takes the board and a target square and returns whether or not the piece can move to
        the given target"""
        bishop = bishop_functionality(self, board, target)
        rook = rook_functionality(self, board, target)
        return bishop or rook


class Bishop(Helper):
    """Contains functionality for the Bishop piece on the board. Works with the ChessVar class
        as this is the blueprint for the Bishop that goes on the ChessVar board."""

    def get_code(self):
        """Returns a printable version of the piece for display on the board."""
        return get_colored_key(" B ", self._color)

    def is_legal_move(self, board, target):
        """Takes the board and a target square and returns whether or not the piece can move to
        the given target"""
        return bishop_functionality(self, board, target)


class Knight(Helper):
    """Contains functionality for the Knight piece on the board. Works with the ChessVar class
        as this is the blueprint for the Knight that goes on the ChessVar board."""

    def get_code(self):
        """Returns a printable version of the piece for display on the board."""
        return get_colored_key(" N ", self._color)

    def is_legal_move(self, board, target):
        """Takes the board and a target square and returns whether or not the piece can move to
        the given target"""
        current_row, current_column = get_board_indexes(self._position)
        relative_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        possible_squares = []
        for row_mod, col_mod in relative_moves:
            new_row = current_row + row_mod
            new_col = current_column + col_mod
            if is_on_board(new_row, new_col):
                target_square = board.search_square(get_board_notation(new_row, new_col))
                if get_color(target_square.get_code()) != self._color:
                    possible_squares.append(get_board_notation(new_row, new_col))

        if target.upper() not in possible_squares:
            return False
        return True


class Rook(Helper):
    """Contains functionality for the Rook piece on the board. Works with the ChessVar class
        as this is the blueprint for the Rook that goes on the ChessVar board."""

    def get_code(self):
        """Returns a printable version of the piece for display on the board."""
        return get_colored_key(" R ", self._color)

    def is_legal_move(self, board, target):
        """Takes the board and a target square and returns whether or not the piece can move to
        the given target"""
        return rook_functionality(self, board, target)


class Pawn(Helper):
    """Contains functionality for the Pawn piece on the board. Works with the ChessVar class
        as this is the blueprint for the Pawn that goes on the ChessVar board."""
    def __init__(self, position, color):
        super().__init__(position, color)
        self._is_first_move = True

    def get_code(self):
        """Returns a printable version of the piece for display on the board."""
        return get_colored_key(" P ", self._color)

    def is_legal_move(self, board, target):
        """Takes the board and a target square and returns whether or not the piece can move to
        the given target"""
        current_row, current_col = get_board_indexes(self._position)
        target_row, target_col = get_board_indexes(target)
        color_multiplier = 1
        if self._color == 'Black':
            color_multiplier = -1
        if target_col == current_col and is_on_board(current_row + color_multiplier, current_col):  # If pawn is moving straight
            first_square = get_board_notation(current_row + color_multiplier, current_col)
            # Searched square in front of pawn for empty

            if board.search_square(first_square).get_code() != " []":
                return False
            if current_row + color_multiplier == target_row:
                self._is_first_move = False
                return True
            # 2 move rule functionality
            if self._is_first_move:
                second_square = get_board_notation(current_row + (color_multiplier * 2), current_col)
                if board.search_square(second_square).get_code() != " []":
                    return False
                if current_row + (color_multiplier * 2) == target_row:
                    self._is_first_move = False
                    return True
            return False

        if target_col + 1 == current_col or target_col - 1 == current_col:  # If pawn is taking diagonally
            if current_row + color_multiplier == target_row:
                piece = board.search_square(target)
                if piece.get_code() != " []":
                    if get_color(piece.get_code()) != self._color:
                        return True
        return False


class Falcon(Helper):
    """Contains functionality for the Falcon piece on the board. Works with the ChessVar class
        as this is the blueprint for the Falcon that goes on the ChessVar board."""

    def get_code(self):
        """Returns a printable version of the piece for display on the board."""
        return get_colored_key(" F ", self._color)

    def is_legal_move(self, board, target):
        """Takes the board and a target square and returns whether or not the piece can move to
        the given target"""
        target_row, target_col = get_board_indexes(target)
        current_row, current_col = get_board_indexes(self._position)
        color_multiplier = 1
        if self._color == 'Black':
            color_multiplier = -1
        if (current_row - target_row) * color_multiplier > 0:  # Checks if piece will move backward for rook
            return rook_functionality(self, board, target)
        elif (current_row - target_row) * color_multiplier < 0:  # Check if piece will move forward for bishop
            return bishop_functionality(self, board, target)
        return False


class Hunter(Helper):
    """Contains functionality for the Hunter piece on the board. Works with the ChessVar class
        as this is the blueprint for the Hunter that goes on the ChessVar board."""

    def get_code(self):
        """Returns a printable version of the piece for display on the board."""
        return get_colored_key(" H ", self._color)

    def is_legal_move(self, board, target):
        """Takes the board and a target square and returns whether or not the piece can move to
        the given target"""
        target_row, target_col = get_board_indexes(target)
        current_row, current_col = get_board_indexes(self._position)
        color_multiplier = 1
        if self._color == 'Black':
            color_multiplier = -1
        if (current_row - target_row) * color_multiplier < 0:  # Checks if the piece will move forward for rook
            return rook_functionality(self, board, target)
        elif (current_row - target_row) * color_multiplier > 0:  # Checks if piece will move backward for bishop
            return bishop_functionality(self, board, target)
        return False


class EmptySquare(Helper):
    """Contains functions for EmptySquares on the ChessVar board. Is essentially a placeholder
    for other pieces, so will get used as an object on the board."""

    def __init__(self, position):
        super().__init__(position, None)

    def get_code(self):
        """Returns a printable version of the square for display on the board."""
        return " []"


def get_colored_key(key, color):
    """Takes a piece 'key' and returns it uppercase or lowercase depending on which color it
    is, with uppercase meaning a white piece and lowercase meaning a black piece."""
    if color == 'Black':
        key = key.lower()
    else:
        key = key.upper()
    return key


def get_board_indexes(square):
    """Takes a square in traditional board notation (ie. E5) and converts
    it to the indexes for the array, returning the ."""
    letter = str(square[0]).upper()
    letter = ord(letter) - 65
    number = int(square[1]) - 1
    return number, letter


def get_board_notation(row, column):
    """Returns a board notation (ie: E4) of the given row and column"""
    row = str(row + 1)
    letter = chr(column + 65)
    return letter + row


def is_on_board(row, column):
    """Returns whether or not the given index for a square is on the board."""
    return 0 <= row < 8 and 0 <= column < 8


def get_color(key):
    """Returns the color of the given key piece, or None if it is an empty square."""
    if key == " []":
        return None
    if key.isupper():
        return "White"
    else:
        return "Black"


def rook_functionality(self, board, target):
    """Returns whether or not a rook-style move is legal. Can be used for pieces other than
    rook (like Queen)."""
    target_row, target_col = get_board_indexes(target)
    current_row, current_col = get_board_indexes(self.get_position())
    if target_col == current_col:
        ratio = (target_row - current_row) / abs(target_row - current_row)
        for square_index in range(int(current_row + ratio), int(target_row), int(ratio)):
            square_code = get_board_notation(square_index, target_col)
            square = board.search_square(square_code)
            if square.get_code() != ' []':
                return False
        target_square = board.search_square(target)
        if get_color(target_square.get_code()) != self.get_color():
            return True
    if target_row == current_row:
        ratio = (target_col - current_col) / abs(target_col - current_col)
        for square_index in range(int(current_row + ratio), int(target_row), int(ratio)):
            square_code = get_board_notation(target_row, square_index)
            square = board.search_square(square_code)
            if square.get_code() != ' []':
                return False
        target_square = board.search_square(target)
        if get_color(target_square.get_code()) != self.get_color():
            return True
    return False


def bishop_functionality(self, board, target):
    """Returns whether or not a bishop-style move is legal. Can be used for pieces other than
        rook (like Queen)."""
    target_row, target_col = get_board_indexes(target)
    current_row, current_col = get_board_indexes(self.get_position())
    row_dif = abs(target_row - current_row)
    col_dif = abs(target_col - current_col)
    if row_dif == col_dif:
        ratio_row = (target_row - current_row) / row_dif
        ratio_col = (target_col - current_col) / col_dif
        for square_index in range(1, int(row_dif)):
            row_index = current_row + (square_index * ratio_row)
            column_index = current_col + (square_index * ratio_col)
            square_code = get_board_notation(int(row_index), int(column_index))
            square = board.search_square(square_code)
            if square.get_code() != ' []':
                return False
        target_square = board.search_square(target)
        if get_color(target_square.get_code()) != self.get_color():
            return True
    return False
