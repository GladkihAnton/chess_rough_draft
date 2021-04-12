import possible_moves
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


def make_a_move(board: Board) -> Board:
    return board


def click_on_dot(board: Board, square: tuple) -> bool:
    return '.' in board.get_piece(square)



def main():
    board = Board()
    #front -> back: click_on_square
    start_square = Square()
    start_square.x = 6
    start_square.y = 2
    print(board.get_piece(start_square),' - piece')
    for i in range(8):
        print()
        for j in range(8):
            a = board.board_list[i][j].zfill(2)
            a = a.replace(' ', '0')
            print(a,end=' ')

    possible_moves_board = Board()
    print(type(possible_moves_board))
    possible_moves_board = possible_moves.generate_possible_moves(board, start_square)
    possible_moves_board.print()
    #back -> front: possible_moves_board - board with dots for possible moves
    #front -> back: target_square
    target_square = (0,0)
    print(type(possible_moves_board))
    # if click_on_dot(possible_moves_board, target_square):
    #     move = Move(board, start_square,target_square)
    #     board = make_a_move(board, move)
    # else:
    #     pass #board without dots goes to frontend

if __name__ == "__main__":
    main()