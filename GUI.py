import pygame
from Othello import Othello
import pygame.freetype

WIDTH = 600
HEIGHT = 600
GRID = (WIDTH - WIDTH / 5) / 8  # grid size = 60
PIECE_RADIUS = int(0.8 * GRID / 2)  # radius = 24
FPS = 30
BLACK = 1
WHITE = -1
VALID_MOVE = 2
REVERSI_CHOICE = 3
PIECE_COLOR = {BLACK: (0, 0, 0), WHITE: (254, 254, 244), VALID_MOVE: (128, 128, 128), REVERSI_CHOICE: (242, 133, 0)}
DIRECTION_NO = {(-1, 0): "1", (1, 0): "2", (0, -1): "3", (0, 1): "4", (1, 1): "5", (1, -1): "6", (-1, -1): "7",
                (-1, 1): "8"}


def draw(surf, board, turn, is_reversi=False, choices=None):
    surf = pygame.display.set_mode((WIDTH, HEIGHT))
    surf.fill((42, 110, 63))
    for i in range(1, 10):
        pygame.draw.line(surf, (0, 0, 0), (GRID * i, GRID), (GRID * i, WIDTH - GRID))
        pygame.draw.line(surf, (0, 0, 0), (GRID, GRID * i), (HEIGHT - GRID, GRID * i))

    f = pygame.font.SysFont("Calibri", 20, bold=False, italic=False)
    if turn == BLACK:
        textcontent = "BLACK"
    else:
        textcontent = "WHITE"
    text = f.render(f"Turn: {textcontent}", True, (0, 0, 0))
    textrect = text.get_rect()
    textrect.center = (300, 30)
    surf.blit(text, textrect)

    # draw circle
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0:
                pygame.draw.circle(surf, PIECE_COLOR[board[i][j]], ((i + 1 + 0.5) * GRID, (j + 1 + 0.5) * GRID),
                                   PIECE_RADIUS,
                                   width=PIECE_RADIUS)

    # if it is wait_reversi, we need add number for each direction.
    f_reversi = pygame.font.SysFont("Calibri", 18, bold=False, italic=False)
    if is_reversi:
        for k, v in choices.items():
            for grid in v:
                (r, c) = grid
                textnumber = f_reversi.render(f"{DIRECTION_NO[k]}", True, (0, 0, 0))
                textnumberreact = textnumber.get_rect()
                textnumberreact.center = ((r + 1 + 0.5) * GRID, (c + 1 + 0.5) * GRID)
                surf.blit(textnumber, textnumberreact)

    return surf


def draw_background(surf):
    surf.fill((42, 110, 63))
    for i in range(1, 10):
        pygame.draw.line(surf, (0, 0, 0), (GRID * i, GRID), (GRID * i, WIDTH - GRID))
        pygame.draw.line(surf, (0, 0, 0), (GRID, GRID * i), (HEIGHT - GRID, GRID * i))


def get_location(coordinate):
    (x, y) = coordinate
    row = int(x // GRID) - 1
    col = int(y // GRID) - 1
    return row, col


def show_result(surf, game):
    repre = {1: "BLACK", -1: "WHITE", 0: "TIE"}
    winner = repre[game.winner]
    surf = pygame.display.set_mode((WIDTH, HEIGHT))
    surf.fill((42, 110, 63))
    f = pygame.font.SysFont("Calibri", 20, bold=False, italic=False)
    textwinner = f"WINNER:{winner} "
    textcalculation = f"BLACK pieces:{game.black_count}      WHITE pieces:{game.white_count} "
    text1 = f.render(f" {textwinner}", True, (0, 0, 0))
    text2 = f.render(f" {textcalculation}", True, (0, 0, 0))
    textrect1 = text1.get_rect()
    textrect2 = text2.get_rect()
    textrect1.center = (300, 250)
    textrect2.center = (300, 350)
    surf.blit(text1, textrect1)
    surf.blit(text2, textrect2)
    pygame.display.flip()
    waiting_end = True
    while waiting_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
    return surf


def start_game():
    # initial the pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Othello-Yannie & Bill')

    clock = pygame.time.Clock()
    clock.tick(FPS)

    # initial the board class
    game = Othello()
    draw(screen, game.board, BLACK)
    pygame.display.flip()

    # start the game, BLACK first
    wait_move(game, screen)


def wait_move(game, screen):
    waiting_move = True
    if not game.get_valid_moves():
        wait_move(game, screen)
    draw(screen, game.board, game.current_turn)
    pygame.display.flip()

    while waiting_move:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                grid = get_location((event.pos[0], event.pos[1]))

                if game.is_valid(grid, VALID_MOVE):
                    game.move(grid)
                    draw(screen, game.board, game.current_turn, True, game.reversi_choice)
                    pygame.display.flip()
                    waiting_move = False
    wait_reversi(game, screen)


def wait_reversi(game, screen):
    waiting_reversi = True
    # wait for choosing the flip direction.
    while waiting_reversi:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                grid = get_location((event.pos[0], event.pos[1]))

                if game.is_valid(grid, REVERSI_CHOICE):
                    game.reversi(grid)

                    draw(screen, game.board, game.current_turn)
                    pygame.display.flip()
                    waiting_reversi = False

                    if game.is_end():
                        show_result(screen, game)
    wait_move(game, screen)
    return


if __name__ == '__main__':
    start_game()
