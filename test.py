import copy
import random
BLACK = 1
WHITE = -1
from Othello import Othello
#
# class R:
#     def __init__(self):
#         self.board = [[0 for _ in range(8)] for _ in range(8)]
#         self.index = 100
#         self.d = {1:'xxx', 2:['YYY','ppp'], 3:'zzz'}
#         self.s = {10, 11, 12}
# a  = [77,88,99]
# re = R()
# def mm(re, depth):
#     if depth == 0:
#         return
#     re.s.add(a[depth])
#     #print(re.s,depth)
#     re_temp = copy.deepcopy(re)
#     for i in list(re.s):
#         if depth == 2:
#             print(i,re.s)
#         if depth == 1:
#             print(i, re.s)
#         #print(re.s,i,depth)
#         mm(re,depth-1)
#     #print(re.s,depth)
#         re = copy.deepcopy(re_temp)
#
#
#     return re
# mm(re,2)
board = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, -1, 0, 0, 0], [0, 0, 1, 1, -1, 0, 0, 0], [0, 0, 0, 0, -1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
def evaluate(board, maximizing_color):
    black_score = 0
    white_score = 0
    print(board)
    for x in range(0, 7):
        for y in range(0, 7):
            if (x, y) in ((0, 0), (0, 7), (7, 0), (7, 7)):
                if board[x][y] == BLACK:
                    black_score += 50
                else:
                    print("white", (x, y), white_score)
                    white_score += 50
            elif (x, y) in ((1, 0), (0, 1), (0, 6), (1, 7), (6, 0), (7, 1), (7, 6), (6, 7)):
                if board[x][y] == BLACK:
                    black_score -= 15
                else:
                    print("white", (x, y), white_score)
                    white_score += -15
            elif (x, y) in ((1, 1), (6, 6), (1, 6), (6, 1)):
                if board[x][y] == BLACK:
                    black_score -= 30
                else:
                    print("white", (x, y), white_score)
                    white_score += -30
            elif x == 7 or x == 0 or y == 7 or y == 0:
                if board[x][y] == BLACK:
                    black_score += 10
                else:
                    print("white", (x, y), white_score)
                    white_score += 10
            else:
                if board[x][y] == BLACK:
                    print("black", (x, y), black_score)
                    black_score += 3
                else:
                    print("white", (x, y), white_score)
                    white_score += 3
    print(black_score, white_score)
    if maximizing_color == BLACK:
        return black_score - white_score
    else:
        return white_score - black_score
evaluate(board, WHITE)
