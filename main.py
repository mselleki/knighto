import numpy as np

dict_squares_2 = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
dict_squares = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}


class Chessboard:

    def __init__(self):
        self.squares = np.zeros((8, 8))

    def get_squares(self):
        return self.squares

    def set_piece(self, piece, square, dict_squares):
        self.squares[dict_squares[square[0]]][square[1]-1] = piece
        return square


class Knight:
    def __init__(self, position, cpt, drunk_pour):
        self.position = Chessboard.set_piece(self, position, dict_squares)  # current position of the knight
        self.cpt = cpt  # number of moves
        self.drunk_pour = drunk_pour  # probability of going left or right given a square

    def move(self):
        return self
