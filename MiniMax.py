from math import inf
import copy
from Reversi_game import MAX_DEPTH

BLACK = 1
WHITE = -1


def evaluate(game, maximizing_color):
    black_score = 0
    white_score = 0
    for x in range(0, 8):
        for y in range(0, 8):
            if (x, y) in ((0, 0), (0, 7), (7, 0), (7, 7)):
                if game.board[x][y] == BLACK:
                    black_score += 50
                elif game.board[x][y] == WHITE:
                    white_score += 50
            elif (x, y) in ((1, 0), (0, 1), (0, 6), (1, 7), (6, 0), (7, 1), (7, 6), (6, 7)):
                if game.board[x][y] == BLACK:
                    black_score -= 15
                elif game.board[x][y] == WHITE:
                    white_score += -15
            elif (x, y) in ((1, 1), (6, 6), (1, 6), (6, 1)):
                if game.board[x][y] == BLACK:
                    black_score -= 30
                elif game.board[x][y] == WHITE:
                    white_score += -30
            elif x == 7 or x == 0 or y == 7 or y == 0:
                if game.board[x][y] == BLACK:
                    black_score += 10
                elif game.board[x][y] == WHITE:
                    white_score += 10
            else:
                if game.board[x][y] == BLACK:
                    black_score += 3
                elif game.board[x][y] == WHITE:
                    white_score += 3

    if maximizing_color == BLACK:
        return black_score - white_score
    else:
        return white_score - black_score
"""
def minimax(game, depth, maximizing_player, maximizing_color):
    if depth == 0 or game.is_end():
        e=evaluate(game, maximizing_color)
        return None, e

    if depth != MAX_DEPTH and not game.get_valid_moves():
        if maximizing_player:
            max_eval = -inf
            current_eval = minimax(game, depth - 1, False, maximizing_color)[1]
            if current_eval > max_eval:
                max_eval = current_eval
            return None, max_eval
        else:
            min_eval = inf
            current_eval = minimax(game, depth - 1, True, maximizing_color)[1]
            if current_eval < min_eval:
                min_eval = current_eval
            return None, min_eval

    best_move = None
    if maximizing_player:
        max_eval = -inf
        temp_game_move = copy.deepcopy(game)
        for move in list(game.valid_move):
            game.move(move)
            temp_game_reversi = copy.deepcopy(game)
            for choice in list(game.reversi_choice):
                game.reversi(list(game.reversi_choice[choice])[0])
                current_eval = minimax(game, depth - 1, False, maximizing_color)[1]
                game = copy.deepcopy(temp_game_reversi)
                if current_eval > max_eval:
                    max_eval = current_eval
                    best_move = move
                # print( 'level',depth,current_eval,move,choice,max_eval)
            game = copy.deepcopy(temp_game_move)

        return best_move, max_eval
    else:
        min_eval = inf
        temp_game_move = copy.deepcopy(game)
        for move in list(game.valid_move):
            game.move(move)
            temp_game_reversi = copy.deepcopy(game)
            for choice in list(game.reversi_choice):
                game.reversi(list(game.reversi_choice[choice])[0])
                current_eval = minimax(game, depth - 1, True, maximizing_color)[1]
                game = copy.deepcopy(temp_game_reversi)
                if current_eval < min_eval:
                    min_eval = current_eval
                    best_move = move
                # print('level', depth, current_eval, move, choice, min_eval)
            game = copy.deepcopy(temp_game_move)
        return best_move, min_eval"""


def MiniMaxAlphaBeta(game, depth, maximizing_color):
    alpha = -inf
    beta = inf

    best_move = None
    best_choice = None
    max_eval = -inf
    temp_game_move = copy.deepcopy(game)
    for move in list(game.valid_move):
        game.move(move)
        temp_game_reversi = copy.deepcopy(game)
        for choice in list(game.reversi_choice):
            game.reversi(list(game.reversi_choice[choice])[0])
            current_eval = minimizeBeta(game, depth - 1, alpha, beta, maximizing_color)
            game = copy.deepcopy(temp_game_reversi)
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move
                best_choice = choice
            # print( 'level',depth,current_eval,move,choice,max_eval)
        game = copy.deepcopy(temp_game_move)

    return best_move, best_choice


def minimizeBeta(game, depth, a, b, maximizing_color):
    if depth == 0 or game.is_end():
        e = evaluate(game, maximizing_color)
        return e

    if depth != MAX_DEPTH and not game.get_valid_moves():
        eval = maximizeAlpha(game, depth - 1, a, b, maximizing_color)
        return eval

    beta = b

    temp_game_move = copy.deepcopy(game)
    for move in list(game.valid_move):
        game.move(move)
        temp_game_reversi = copy.deepcopy(game)
        for choice in list(game.reversi_choice):
            current_eval = inf
            if a < beta:
                game.reversi(list(game.reversi_choice[choice])[0])
                current_eval = maximizeAlpha(game, depth - 1, a, beta, maximizing_color)
                game = copy.deepcopy(temp_game_reversi)
            if current_eval < beta:
                beta = current_eval
            # print('level', depth, current_eval, move, choice, min_eval)
        game = copy.deepcopy(temp_game_move)
    return beta


def maximizeAlpha(game, depth, a, b, maximizing_color):
    if depth == 0 or game.is_end():
        e = evaluate(game, maximizing_color)
        return e

    if depth != MAX_DEPTH and not game.get_valid_moves():
        eval = minimizeBeta(game, depth - 1, a, b, maximizing_color)
        return eval

    alpha = a

    temp_game_move = copy.deepcopy(game)
    for move in list(game.valid_move):
        game.move(move)
        temp_game_reversi = copy.deepcopy(game)
        for choice in list(game.reversi_choice):
            current_eval = inf
            if alpha < b:
                game.reversi(list(game.reversi_choice[choice])[0])
                current_eval = minimizeBeta(game, depth - 1, alpha, b, maximizing_color)
                game = copy.deepcopy(temp_game_reversi)
            if current_eval > alpha:
                alpha = current_eval
            # print('level', depth, current_eval, move, choice, min_eval)
        game = copy.deepcopy(temp_game_move)
    return alpha
