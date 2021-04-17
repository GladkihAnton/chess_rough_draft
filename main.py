import possible_moves
import  copy
from possible_moves import Board
from possible_moves import Square

class Square:
    def __init__(self):
        pass


class Move:

    def __init__(self, board: Board, start_square: tuple, target_square: tuple):
        self.board = board
        self.start_square = start_square
        self.start_square = target_square
        self.piece = board.get_piece(start_square)
        if target_square:
            self.is_captures = True
        else:
            self.is_captures = False


def make_a_move(board: Board,start_square: Square, target_square: Square) -> Board:
    print('e')
    x = start_square.x
    y = start_square.y
    piece = board.get_piece(start_square)
    board.board_list[x][y] = ' '
    x = target_square.x
    y = target_square.y
    board.board_list[x][y] = piece
    if board.next_move_color == 'White':
        board.next_move_color = 'Black'
    else:
        board.next_move_color = 'White'
    return board


def click_on_dot(board: Board, square: tuple) -> bool:
    return '.' in board.get_piece(square)



def main():
    board = Board()
    #front -> back: click_on_square
    start_square = Square()
    target_square = Square()
    board.print()
    x = ''
    while x != 'exit':
        x = input()
        start_square.x,start_square.y = map(int,x.split())
        possible_moves_board = possible_moves.generate_possible_moves(copy.deepcopy(board), start_square)
        possible_moves_board.print()
        x = input()
        target_square.x,target_square.y = map(int,x.split())
        if '.' in possible_moves_board.get_piece_name(target_square):
            make_a_move(board,start_square,target_square)
            board.print()
        else:
            possible_moves_board = board
            possible_moves_board.print()
            board.print()



if __name__ == "__main__":
    main()