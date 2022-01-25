import random
import time
from cairosvg import svg2png
import chess.svg
import chess
import png2gif

dict_squares_2 = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
dict_squares = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
start_time = time.time()
chess.COLORS = [True, True]
chess.COLOR_NAMES = ['white', 'white']


class Chessboard:

    def __init__(self):
        self.squares = [[None for i in range(8)] for j in range(8)]

    def get_squares(self):
        return self.squares

    def get_position(self):
        for column in range(8):
            for raw in range(8):
                if self.squares[column][raw] is not None:
                    return [column, raw]
        return [-1, -1]

    def set_piece(self, piece, square):
        if piece.cpt != 0:
            self.squares[piece.position[0]][piece.position[1]] = None
        self.squares[dict_squares[square[0]]][int(square[1]) - 1] = piece
        return self.get_position()


class Knight:
    def __init__(self, board, position, drunk_prob):
        self.cpt = 0  # number of moves
        self.position = board.set_piece(piece=self, square=position)  # current knight's pos
        self.history = []
        self.drunk_prob = drunk_prob  # probability of going left or right given a square

    def transcript(self):
        col = dict_squares_2[self.position[0] + 1]
        raw = str(self.position[1] + 1)
        case = col + raw
        return case

    def move(self):
        dict_moves = {
            'left': [[-2, -1, self.drunk_prob / 4], [-2, 1, self.drunk_prob / 4], [-1, 2, self.drunk_prob / 4],
                     [-1, -2, self.drunk_prob / 4]],
            'right': [[1, 2, (1 - self.drunk_prob) / 4], [1, -2, (1 - self.drunk_prob) / 4],
                      [2, 1, (1 - self.drunk_prob) / 4], [2, -1, (1 - self.drunk_prob) / 4]]}  # last elt is probability
        for key, moves in dict_moves.items():
            moves = [move for move in moves if
                     (0 <= self.position[0] + move[0] <= 7 and 0 <= self.position[1] + move[1] <= 7)]
            if len(moves) != 0:
                for move in moves:
                    if key == 'left':
                        move[2] = round(move[2] + (self.drunk_prob / 4) * (4 - len(moves)) / len(moves), 3)
                    else:
                        move[2] = round(move[2] + ((1 - self.drunk_prob) / 4) * (4 - len(moves)) / len(moves), 3)

            dict_moves[key] = moves

        if len(dict_moves['left']) == 0:
            for move in dict_moves['right']:
                move[2] = round(move[2] * 1 / (1 - self.drunk_prob), 3)
        if len(dict_moves['right']) == 0:
            for move in dict_moves['left']:
                move[2] = round(move[2] * 1 / self.drunk_prob, 3)

        list_moves = [*list(dict_moves.values())[0], *list(dict_moves.values())[1]]
        move_chosen = random.choices(list_moves, weights=[move[2] for move in list_moves])
        # print('Move chosen : ', move_chosen[0])
        self.position[0] += move_chosen[0][0]
        self.position[1] += move_chosen[0][1]
        self.history.append(self.transcript())
        self.cpt += 1
        return self

    def info_piece(self):
        print("Position : ", caval.position)
        print("History : ", caval.history)
        print("cpt : ", caval.cpt)
        print("drunk_prob : ", caval.drunk_prob)
        print("-----------------------")
        return self


n = 100
i = 0
img_num = 0
L = []
board_ = chess.Board('8/8/8/8/8/8/8/8 w - - 0 1')
board_.set_piece_at(square=chess.SQUARE_NAMES.index('a1'), piece=chess.Piece.from_symbol('N'))
board_svg = chess.svg.board(board_)
svg2png(bytestring=board_svg,
        write_to='/home/icrin_3/PycharmProjects/Knighto/board_png/move' + str(img_num) + '.png')
board_.remove_piece_at(square=chess.SQUARE_NAMES.index('a1'))
img_num += 1
while i <= n:
    board = Chessboard()
    starting_square = "a1"
    caval = Knight(board, starting_square, 0.3)

    while True:
        caval.move()
        if i == 0:
            board_.set_piece_at(square=chess.SQUARE_NAMES.index(caval.history[-1]), piece=chess.Piece.from_symbol('N'))
            board_svg = chess.svg.board(board_)
            svg2png(bytestring=board_svg,
                    write_to='/home/icrin_3/PycharmProjects/Knighto/board_png/move' + str(img_num) + '.png')
            board_.remove_piece_at(square=chess.SQUARE_NAMES.index(caval.history[-1]))
            img_num += 1

        if caval.transcript() == "a1" and caval.cpt != 0:
            L.append(caval.cpt)
            # print("History : ", caval.history) random walk of the knighto
            # print(caval.cpt)
            break
    i += 1

png2gif.pngtogif()  # Create the GIF of the knighto walk
print(' \-----------------------------------------------\ ')
print(f" \ Expected first return time (n={n}): {int(sum(L) / len(L))} moves \ ")
print(" \-------------- %s seconds ------------------\ " % round((time.time() - start_time), 3))

# RESULTS PART
# ---------------------------------------
# n = 100 E[T] = 888 ~ 2 seconds
# n = 10.000 E[T] = 876 ~120 seconds
# n = 1.000.000 E[T] = 893 ~ 11 600 seconds
