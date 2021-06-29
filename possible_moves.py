import copy




class Square:
    def __init__(self, x=0,y=0):
        self.x = x
        self.y = y


    def __deepcopy__(self, memodict={}):

        new = type(self)()
        new.__dict__.update(self.__dict__)
        return new

    def is_inside_board(self):
        return 0 <= self.x <= 7 and 0 <= self.y <= 7


class Board:
    def __init__(self):
        self.board_list = [['Q',' ',' ',' ',' ',' ',' ',' '],
                           [' ',' ',' ',' ',' ',' ',' ',' '],
                           [' ',' ','q',' ',' ',' ',' ',' '],
                           [' ',' ',' ','b',' ',' ',' ',' '],
                           [' ','K',' ','R','r','k',' ',' '],
                           [' ',' ',' ','B',' ',' ',' ',' '],
                           [' ',' ',' ',' ',' ',' ',' ',' '],
                           [' ',' ',' ',' ',' ',' ',' ',' ']]
        self.is_next_move_white = True
        self.is_black_in_check = False
        self.is_white_in_check = False
        self.is_black_in_mate = False
        self.is_white_in_mate = False
        self.black_long_castle = True
        self.white_long_castle = True
        self.black_short_castle = True
        self.white_short_castle = True
        self.en_passant = ''

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def print(self, message='') -> None:
        print(message)
        for i in range(8):
            for j in range(8):
                a = self.board_list[i][j].zfill(2)
                a = a.replace(' ', '0')
                print(a, end=' ')
            print()
        print()

    def get_squares(self, piece: str) -> list:
        result_squares = []
        for x in range(8):
            for y in range(8):
                if self.board_list[x][y].rstrip('.') == piece:
                    result_squares.append(Square(x, y))
        return result_squares

    def get_piece_name (self, square: Square) -> str.lower: #regardless of color
        x = square.x
        y = square.y
        return self.board_list[x][y].lower()

    def get_piece(self, square: Square) -> str:
        x = square.x
        y = square.y
        return self.board_list[x][y]

    def is_color_of_piece_white(self, square: Square) -> bool:
        return self.get_piece(square).isupper()

    def is_empty_square(self, square: Square) -> bool:
        return self.get_piece_name(square) == ' .' or self.get_piece_name(square) == '. ' or self.get_piece_name(square)==' '

    def update(self,square: Square, piece: str) -> None:
        self.board_list[square.x][square.y] = piece

    def flip(self):
        new_board_list = []
        for i in range(7,-1,-1):
            new_board_list.append(self.board_list[i].reverse())
        self.board_list = new_board_list

    def is_king_in_check(self) -> bool:
           #print(original_board.next_move_color)
        if self.is_next_move_white:
            king_square = self.get_squares('K')[0]
            q = copy.deepcopy(self)
            #q.print()
            board = king_possible_moves(q, king_square, True)
            if board.get_squares('.k'): print('a');return True

            board = rook_possible_moves(copy.deepcopy(self),king_square, True)
            if board.get_squares('.r'):print('b'); return True

            board = knight_possible_moves(copy.deepcopy(self),king_square, True)
            if board.get_squares('.n'): print('c');return True

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

            board = rook_possible_moves(copy.deepcopy(self),king_square, True)
            if board.get_squares('.R'): print('b');return True

            board = knight_possible_moves(copy.deepcopy(self),king_square, True)
            if board.get_squares('.N'): print('c');return True

            board = bishop_possible_moves(copy.deepcopy(self), king_square, True)
            if board.get_squares('.B'): print('d');return True

            board = queen_possible_moves(copy.deepcopy(self),king_square, True)
            if board.get_squares('.Q'): print('e');return True

            return False


    def own_piece_capture_check(self):
        for x in range(8):
            for y in range(8):
                if self.is_next_move_white:
                    if self.board_list[x][y].isupper():
                        self.board_list[x][y] = self.board_list[x][y].replace('.', '')
                else:
                    if self.board_list[x][y].islower():
                        self.board_list[x][y] = self.board_list[x][y].replace('.', '')


def puts_own_king_in_check(board: Board, start_square: Square, target_square: Square) -> bool:

    piece = board.get_piece(start_square)
    board.update(start_square, ' ')
    target_piece = board.get_piece(target_square)
    if  target_piece != 'K' and target_piece != 'k':
        board.update(target_square, piece)
    return is_king_in_check(board)


def is_move_legal(board: Board, square: Square, target_square: Square, king_check=False) -> bool:
    x = target_square.x
    y = target_square.y
    #print(x,y,king_check)
    if not king_check:
        if target_square.is_inside_board() and not puts_own_king_in_check(copy.deepcopy(board), square, target_square):
            board.board_list[x][y] += '.'
            return board.is_empty_square(target_square)
        else:
            return False

    else:
        if target_square.is_inside_board():
            board.board_list[x][y] = '.' + board.board_list[x][y]
            return board.is_empty_square(target_square)
        else:
            return False




def pawn_possible_moves(board: Board, square: Square, king_check = False) -> Board:
    if not board.is_next_move_white:
        board.flip()
        square.x = (8-square.x)%8
        square.y = (8-square.y)%8
    _pawn_captures_moves(board, square)
    _pawn_straight_moves(board, square)
    _pawn_promotion_moves(board, square)
    return board


def _pawn_captures_moves(board: Board, square: Square) -> Board:
    square.y -= 1
    if square.is_inside_board() and (board.is_color_of_piece_white(square) == board.is_next_move_white):
        piece = board.get_piece(square)

        board.update()


def _pawn_straight_moves(board: Board, square: Square) -> Board:
    pass


def _pawn_promotion_moves(board: Board, square: Square) -> Board:
    pass




def rook_possible_moves(board: Board, square: Square, king_check=False) -> Board:

    new_square = Square()
    if square.x < 8:
        new_square.y = square.y
        for rank in range(square.x+1,8):
            new_square.x = rank
            if not is_move_legal(board,square, new_square,king_check): break
    if square.x > 0:
        for rank in range(square.x-1, -1, -1):
            new_square.x = rank
            if not is_move_legal(board,square, new_square,king_check): break
    if square.y < 8:
        new_square.x = square.x
        for file in range(square.y+1, 8):
            new_square.y = file
            if not is_move_legal(board, square,new_square,king_check): break
    if square.y > 0:
        for file in range(square.y-1, -1, -1):
            new_square.y = file
            if not is_move_legal(board, square, new_square,king_check): break
    return board


def knight_possible_moves(board: Board, square: Square, king_check = False) -> Board:
    new_square = Square()
    all_directions = [(1,2), (2,1)]
    for direction in all_directions:
        for x_direction in [-1,1]:
            for y_direction in [-1, 1]:
                new_square.x = square.x + direction[0] * x_direction
                new_square.y = square.y + direction[1] * y_direction
                is_move_legal(board, square, new_square, king_check)

    return board


def bishop_possible_moves(board: Board, square: Square, king_check=False) -> Board:
    new_square = Square()
    all_directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    for move_length in range(1,8):
        all_directions_cache = all_directions.copy()
        for direction in all_directions_cache:
            new_square.x = square.x + direction[0] * move_length
            new_square.y = square.y + direction[1] * move_length
            if not is_move_legal(board, square, new_square, king_check):
                all_directions.remove(direction)
    return board


def queen_possible_moves(board: Board, square: Square, king_check=False) -> Board:
    board = bishop_possible_moves(board,square, king_check)
    board = rook_possible_moves(board,square, king_check)
    return board


def king_possible_moves(board: Board, square: Square, king_check = False) -> Board:
    new_square = Square()
    for x_direction in [-1,0,1]:
        for y_direction in [-1,0,1]:
            if x_direction or y_direction:
                new_square.x = x_direction + square.x
                new_square.y = y_direction + square.y
                is_move_legal(board,square, new_square, king_check)
    if not king_check:
        castles(board)
        if board.is_next_move_white:
            board.white_long_castle = False
            board.white_short_castle = False
        else:
            board.black_short_castle = False
            board.black_long_castle = False
    return board

def castles(board: Board) -> Board:
    if board.is_next_move_white:
        king_square = board.get_squares('K')[0]
        x = king_square.x
        y = king_square.y
        if board.white_long_castle and not board.is_white_in_check:
            cache_board = copy.deepcopy(board)
            for i in range(1,3):
                cache_board.board_list[x][y - i] = 'K'
                cache_board.board_list[x][y - i + 1] = ' '
                if is_king_in_check(cache_board): break
            else:
                print('+', board.board_list[7][0],'+',len(board.board_list[7][0]))
                board.board_list[7][0] += '.'
                print('+', board.board_list[7][0], '+', len(board.board_list[7][0]))

        if board.white_short_castle and not board.is_white_in_check:
            cache_board = copy.deepcopy(board)
            for i in range(1,3):
                cache_board.board_list[x][y + i] = 'K'
                cache_board.board_list[x][y + i - 1] = ' '
                if is_king_in_check(cache_board): break
            else:
                print('+',board.board_list[7][7],'+',len(board.board_list[7][7]))
                board.board_list[7][7] += '.'
                print('+', board.board_list[7][7], '+', len(board.board_list[7][7]))

    else:
        king_square = board.get_squares('k')[0]
        x = king_square.x
        y = king_square.y
        if board.black_long_castle and not board.is_black_in_check:
            cache_board = copy.deepcopy(board)
            for i in range(1,3):
                cache_board.board_list[x][y - i] = 'k'
                cache_board.board_list[x][y - i + 1] = ' '
                if is_king_in_check(cache_board): break
            else:
                board.board_list[0][0] += '.'
        if board.white_short_castle and not board.is_white_in_check:
            cache_board = copy.deepcopy(board)
            for i in range(1,3):
                cache_board.board_list[x][y + i] = 'k'
                cache_board.board_list[x][y + i - 1] = ' '
                if is_king_in_check(cache_board): break
            else:
                board.board_list[0][7] += '.'

    board.print()



def generate_possible_moves(board: Board, square: Square) -> Board:
    piece = board.get_piece(square)
    print(piece)
    if (board.is_next_move_white and piece.isupper()) or (not board.is_next_move_white and piece.islower()):
        piece = piece.lower()
        if piece == 'p':
            board = pawn_possible_moves(board, square)
        if piece == 'r':
            board = rook_possible_moves(board, square)
        if piece == 'n':
            board = knight_possible_moves(board, square)
        if piece == 'b':
            board = bishop_possible_moves(board, square)
        if piece == 'q':
            board = queen_possible_moves(board, square)
        if piece == 'k':
            board = king_possible_moves(board, square)
        own_piece_capture_check(board)
        if board.get_squares('k.'):
            board.is_black_in_check = True
        if board.get_squares('K.'):
            board.is_black_in_check = True
    return board