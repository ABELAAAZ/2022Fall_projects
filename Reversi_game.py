from GUI import *
from Reversi_class import *
import MiniMax
import copy
import random
import time

# if there is AI player, we can set the game difficulty -- depth of the minimax
MAX_DEPTH = 3


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

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Othello-Yannie & Bill')

    clock = pygame.time.Clock()
    clock.tick(FPS)
    print(MAX_DEPTH)
    # initial the board class
    game = Othello(black_ai=black_setting, white_ai=white_setting)

    draw(screen, game.board, BLACK)
    pygame.display.flip()

    # start the game, BLACK goes first
    wait_move(game, screen)


def wait_move(game, screen):
    if not game.get_valid_moves():
        if game.is_end():
            show_result(screen, game)
        wait_move(game, screen)
    draw(screen, game.board, game.current_turn)
    pygame.display.flip()

    if (game.current_turn == BLACK and game.black_ai is True) or (game.current_turn == WHITE and game.white_ai is True):
        time.sleep(0.800)
        best_move = MiniMax.minimax(copy.deepcopy(game), MAX_DEPTH, True, game.current_turn)[0]
        game.move(best_move)
        draw(screen, game.board, game.current_turn, True, game.reversi_choice)
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
                        draw(screen, game.board, game.current_turn, True, game.reversi_choice)
                        pygame.display.flip()
                        waiting_move = False
    wait_reversi(game, screen)


def wait_reversi(game, screen):
    if (game.current_turn == BLACK and game.black_ai is True) or (game.current_turn == WHITE and game.white_ai is True):
        time.sleep(0.800)
        game.reversi(list(game.reversi_choice[random.choice(list(game.reversi_choice))])[0])
        draw(screen, game.board, game.current_turn)
        pygame.display.flip()

        if game.is_end():
            show_result(screen, game)
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
                        draw(screen, game.board, game.current_turn)
                        pygame.display.flip()
                        time.sleep(0.200)
                        waiting_reversi = False

                        if game.is_end():
                            show_result(screen, game)
    wait_move(game, screen)
    return


if __name__ == '__main__':
    start_game()
