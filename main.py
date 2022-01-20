import random

dict_squares_2 = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
dict_squares = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}


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

n = 10000
i = 0
L = []
while i <= n:
    board = Chessboard()
    caval = Knight(board, "a1", 0.3)
    while True:
        caval.move()
        if caval.transcript() == "a1" and caval.cpt != 0:
            print("BINGO ! \n The knight just came back home ! ... after...", caval.cpt, "moves...")
            L.append(caval.cpt)
            print("History : ", caval.history)
            print(L)
            break
    i += 1
print('-------------------')
print("Moyenne : ", sum(L)/len(L))
print('-------------------')
