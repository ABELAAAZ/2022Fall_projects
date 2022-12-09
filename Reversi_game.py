from GUI import *
from Reversi_class import *
import MiniMax
import copy
import random
import time

# if there is AI player, we can set the game difficulty -- depth of the minimax
MAX_DEPTH = None


def start_game():
    # initial the pygame
    black_setting = int(input('BLACK side: Enter 1 to set BLACK side to AI, 0 to human player:'))
    while black_setting not in [0, 1]:
        print('You must enter 1 or 0')
        black_setting = int(input('Black side: Enter 1 to set black side to AI, 0 to human player:'))
    black_setting = True if black_setting == 1 else False

    white_setting = int(input('WHITE side: Enter 1 to set WHITE side to AI, 0 to human player:'))
    while white_setting not in [0, 1]:
        print('You must enter 1 or 0')
        white_setting = int(input('WHITE side: Enter 1 to set WHITE side to AI, 0 to human player:'))
    white_setting = True if white_setting == 1 else False

    difficulty=0
    if white_setting or black_setting:
        difficulty = int(input('Enter the difficulty of the game 1-4(3 is the medium level)'))
        while not 1<=difficulty <=4:
            print('You must enter from 1 to 4')
            difficulty = int(input('Enter the difficulty of the game 1-4(3 is the medium level)'))
        print(f'The difficulty of AI will be at level{difficulty}')
    global MAX_DEPTH
    MAX_DEPTH=difficulty

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Othello-Yannie & Bill')

    clock = pygame.time.Clock()
    clock.tick(FPS)
    # initial the board class
    game = Othello(black_ai=black_setting, white_ai=white_setting)

    draw(game.board, BLACK)
    pygame.display.flip()

    # start the game, BLACK goes first
    wait_move(game)


def wait_move(game):
    """
    Wait the current player to drop his piece, then show the valid reversi_choice,then call the wait_reversi function.
    if there is no valid place to drop piece, skip this turn, turn to opponents' turn. If for both player can not drop
    the piece (stalemate situation) then end the game
    :param game: the game object
    :return:
    """
    if not game.get_valid_moves():
        if game.is_end():
            show_result(game)
        wait_move(game)
    draw(game.board, game.current_turn)
    pygame.display.flip()

    best_choice = None
    if (game.current_turn == BLACK and game.black_ai is True) or (game.current_turn == WHITE and game.white_ai is True):
        time.sleep(0.800)
        best_move, best_choice = MiniMax.MiniMaxAlphaBeta(copy.deepcopy(game), MAX_DEPTH, game.current_turn)
        game.move(best_move)
        draw(game.board, game.current_turn, True, game.reversi_choice)
        pygame.display.flip()

    else:
        waiting_move = True
        while waiting_move:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if not GRID <= event.pos[1] < HEIGHT - GRID or not GRID <= event.pos[0] < WIDTH - GRID:
                        print('Not a board grid')
                        continue
                    grid = get_location((event.pos[1], event.pos[0]))
                    if game.is_valid(grid, VALID_MOVE):
                        game.move(grid)
                        draw(game.board, game.current_turn, True, game.reversi_choice)
                        pygame.display.flip()
                        waiting_move = False
    wait_reversi(game, best_choice)


def wait_reversi(game, best_choice):
    """
    Wait the current player to reversi pieces in one direction, then call the wait_reversi function.
    :param game:
    :param best_choice:
    :return:
    """
    if (game.current_turn == BLACK and game.black_ai is True) or (game.current_turn == WHITE and game.white_ai is True):
        time.sleep(0.800)
        #game.reversi(list(game.reversi_choice[random.choice(list(game.reversi_choice))])[0])
        game.reversi(list(game.reversi_choice[best_choice])[0])
        draw(game.board, game.current_turn)
        pygame.display.flip()

        if game.is_end():
            show_result(game)
    else:
        waiting_reversi = True
        # wait for choosing the flip direction.
        while waiting_reversi:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if not GRID <= event.pos[1] < HEIGHT - GRID or not GRID <= event.pos[0] < WIDTH - GRID:
                        print('Not a board grid')
                        continue
                    grid = get_location((event.pos[1], event.pos[0]))
                    if game.is_valid(grid, REVERSI_CHOICE):
                        game.reversi(grid)
                        draw(game.board, game.current_turn)
                        pygame.display.flip()
                        time.sleep(0.200)
                        waiting_reversi = False

                        if game.is_end():
                            show_result(game)
    wait_move(game)
    return


if __name__ == '__main__':
    start_game()
