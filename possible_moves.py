import copy
class Square:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __deepcopy__(self, memodict={}):

        new = type(self)()
        new.__dict__.update(self.__dict__)
        return new

class Board:
    def __init__(self):
        self.board_list = [[' ',' ',' ',' ',' ',' ',' ',' '],
                           [' ','n',' ',' ',' ',' ',' ',' '],
                           [' ',' ',' ',' ',' ',' ',' ',' '],
                           [' ',' ',' ','p','n','b',' ',' '],
                           [' ',' ',' ',' ',' ',' ',' ',' '],
                           [' ',' ',' ',' ','P',' ',' ',' '],
                           [' ','K','R',' ',' ','Q',' ',' '],
                           [' ',' ',' ',' ',' ',' ',' ',' ']]
        self.next_move_color = 'White'
        self.is_black_in_check = False
        self.is_white_in_check = False
        self.is_black_in_mate = False
        self.is_white_in_mate = False
        self.en_passant = ''

    # def __deepcopy__(self, memodict={}):
    #     newone = type(self)()
    #     newone.__dict__.update(self.__dict__)
    #     self.board_list = copy.deepcopy(self.board_list, memodict)
    #     return newone


    def __setattr__(self, name, value):
        self.__dict__[name] = value
        print(name)

    def print(self):
        print()
        print()
        for i in range(8):
            print()
            for j in range(8):
                a = self.board_list[i][j].zfill(2)
                a = a.replace(' ', '0')
                print(a, end=' ')

    def get_squares(self, piece):
        result_squares = []
        for x in range(8):
            for y in range(8):
                if self.board_list[x][y].rstrip('.') == piece:
                    result_squares.append(Square(x, y))
        return result_squares

    def get_piece (self, square: Square):
        x = square.x
        y = square.y
        return self.board_list[x][y].lower()

    def get_piece_colored(self, square):
        x = square.x
        y = square.y
        return self.board_list[x][y]

    def is_own_king_in_check(self):
        print('eerre')
        if self.next_move_color == 'White':
            print('CAPS')
            king_square = self.get_squares('K')[0]

            board = king_possible_moves(copy.deepcopy(self), king_square, True)
            if board.get_squares('.k'): print('a');return True

            board = rook_possible_moves(copy.deepcopy(self),king_square, True)
            if board.get_squares('.r'):print('b'); return True

            board = knight_possible_moves(copy.deepcopy(self),king_square, True)
            if  board.get_squares('.n'): print('c');return True

            board = bishop_possible_moves(copy.deepcopy(self), king_square, True)
            if board.get_squares('.b'):print('d'); return True

            board = queen_possible_moves(copy.deepcopy(self),king_square, True)
            if board.get_squares('.q'): print('e');return True

            return False
        #TODO pawn
        else:
            king_square = self.get_squares('k')[0]

            board = king_possible_moves(copy.deepcopy(self), king_square, True)
            if board.get_squares('.K'): print('a');return True
            self.print()
            board = rook_possible_moves(copy.deepcopy(self),king_square, True)
            if board.get_squares('.R'): print('b');return True
            self.print()
            board = knight_possible_moves(copy.deepcopy(self),king_square, True)
            if  board.get_squares('.N'): print('c');return True
            self.print()
            board = bishop_possible_moves(copy.deepcopy(self), king_square, True)
            if  board.get_squares('.B'): print('d');return True
            self.print()
            board = queen_possible_moves(copy.deepcopy(self),king_square, True)
            if board.get_squares('.Q'): print('e');return True
            self.print()




def own_piece_capture_check(board: Board) -> Board:
    for x in range(8):
        for y in range(8):
            if board.next_move_color == 'White':
                if board.board_list[x][y].isupper():
                    board.board_list[x][y] = board.board_list[x][y].replace('.','')
            else:
                if board.board_list[x][y].islower(): board.board_list[x][y] = board.board_list[x][y].replace('.','')




def is_pinned(board: Board, start_square: Square, target_square: Square) -> bool:
    piece = board.get_piece_colored(start_square)
    board.board_list[start_square.x][start_square.y] = ' '
    if board.board_list[target_square.x][target_square.y] != 'K':
        board.board_list[target_square.x][target_square.y] = piece #TODO has to be changed
    return board.is_own_king_in_check()



def is_marked_square_empty(board: Board, square: Square, s: Square, king_check = False) -> bool:
    x = s.x
    y = s.y

    if 0 <= x <= 7 and 0 <= y <= 7 and not king_check:
        if is_pinned(copy.deepcopy(board),square,s):
            return board
        board.board_list[x][y] += '.'

        return board.board_list[x][y] == ' .' #TODO maybe need to use "in" here
    elif 0 <= x <= 7 and 0 <= y <= 7:
        board.board_list[x][y] = '.' + board.board_list[x][y]
        return board.board_list[x][y] == '. '
    else:
        return False


def pawn_possible_moves(board: Board, square: Square, king_check = False) -> Board:
    return board


def rook_possible_moves(board: Board, square: Square, king_check = False) -> Board:

    new_square = Square()
    if square.x < 8:
        new_square.y = square.y
        for rank in range(square.x+1,8):
            new_square.x = rank
            if not is_marked_square_empty(board,square, new_square,king_check): break
    if square.x > 0:
        for rank in range(square.x-1, -1, -1):
            new_square.x = rank
            if not is_marked_square_empty(board,square, new_square,king_check): break
    if square.y < 8:
        new_square.x = square.x
        for file in range(square.y+1,8):
            new_square.y = file
            if not is_marked_square_empty(board, square,new_square,king_check): break
    if square.y > 0:
        for file in range(square.y-1, -1, -1):
            new_square.y = file
            if not is_marked_square_empty(board,square, new_square,king_check): break
    return board


def knight_possible_moves(board: Board, square: Square, king_check = False) -> Board:
    new_square = Square()
    all_directions = [(1,2),(2,1)]
    for direction in all_directions:
        for x_direction in [-1,1]:
            for y_direction in [-1,1]:
                new_square.x = square.x + direction[0] * x_direction
                new_square.y = square.y + direction[1] * y_direction
                is_marked_square_empty(board,square, new_square, king_check)

    return board


def bishop_possible_moves(board: Board, square: Square, king_check = False) -> Board:
    x = square.x
    y = square.y
    new_square = Square()
    all_directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    for move_length in range(1,8):
        all_directions_cache = all_directions.copy()
        for direction in all_directions_cache:
            new_square.x = square.x + direction[0] * move_length
            new_square.y = square.y + direction[1] * move_length
            if not is_marked_square_empty(board,square, new_square, king_check):
                all_directions.remove(direction)
    return board


def queen_possible_moves(board: Board, square: Square, king_check = False) -> Board:
    board = bishop_possible_moves(board,square, king_check)
    board = rook_possible_moves(board,square, king_check)
    return board


def king_possible_moves(board: Board, square: Square, king_check = False) -> Board:
    new_square = Square()
    x=square.x
    y=square.y
    for x_direction in [-1,0,1]:
        for y_direction in [-1,0,1]:
            if x_direction or y_direction:
                new_square.x = x_direction + square.x
                new_square.y = y_direction + square.y
                xx = new_square.x
                yy = new_square.y
                is_marked_square_empty(board,square, new_square, king_check)
    return board


def generate_possible_moves(board: Board, square: Square) -> Board:


    piece = board.get_piece(square)
    if piece.lower() == 'p':
        board = pawn_possible_moves(board, square)
    if piece.lower() == 'r':
        board = rook_possible_moves(board, square)
    if piece.lower() == 'n':
        board = knight_possible_moves(board, square)
    if piece.lower() == 'b':
        board = bishop_possible_moves(board, square)
    if piece.lower() == 'q':
        board = queen_possible_moves(board, square)
    if piece.lower() == 'k':
        board = king_possible_moves(board, square)
    own_piece_capture_check(board)
    return board