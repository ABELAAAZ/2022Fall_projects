import pygame


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
DIRECTION_NO = {(0, -1): "L", (0, 1): "R", (-1, 0): "U", (1, 0): "D", (1, 1): "DR", (-1, 1): "UR", (-1, -1): "UL",
                (1, -1): "DL"}


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
    text = f.render(f" {textcontent}' s turn", True, (0, 0, 0))
    textrect = text.get_rect()
    textrect.center = (300, 30)
    surf.blit(text, textrect)

    # draw circle
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0:
                pygame.draw.circle(surf, PIECE_COLOR[board[i][j]], ((j + 1 + 0.5) * GRID, (i + 1 + 0.5) * GRID),
                                   PIECE_RADIUS,
                                   width=PIECE_RADIUS)

    # if it is wait_reversi, we need add notice for each direction.
    f_reversi = pygame.font.SysFont("Calibri", 18, bold=False, italic=False)
    if is_reversi:
        for k, v in choices.items():
            for grid in v:
                (r, c) = grid
                textnumber = f_reversi.render(f"{DIRECTION_NO[k]}", True, (0, 0, 0))
                textnumberreact = textnumber.get_rect()
                textnumberreact.center = ((c + 1 + 0.5) * GRID, (r + 1 + 0.5) * GRID)
                surf.blit(textnumber, textnumberreact)

    return surf


def show_result(surf, game):
    surf = pygame.display.set_mode((WIDTH, HEIGHT))
    surf.fill((42, 110, 63))
    for i in range(1, 10):
        pygame.draw.line(surf, (0, 0, 0), (GRID * i, GRID), (GRID * i, WIDTH - GRID))
        pygame.draw.line(surf, (0, 0, 0), (GRID, GRID * i), (HEIGHT - GRID, GRID * i))

    for i in range(8):
        for j in range(8):
            if game.board[i][j] != 0:
                pygame.draw.circle(surf, PIECE_COLOR[game.board[i][j]], ((j + 1 + 0.5) * GRID, (i + 1 + 0.5) * GRID),
                                   PIECE_RADIUS,
                                   width=PIECE_RADIUS)

    repre = {1: "BLACK", -1: "WHITE", 0: "TIE"}
    winner = repre[game.winner]

    f = pygame.font.SysFont("Calibri", 20, bold=False, italic=False)
    textwinner = f"WINNER:{winner} "
    textcalculation = f"BLACK pieces:{game.black_count}      WHITE pieces:{game.white_count} "
    text1 = f.render(f" {textwinner}", True, (254, 254, 244))
    text2 = f.render(f" {textcalculation}", True, (254, 254, 244))
    textrect1 = text1.get_rect()
    textrect2 = text2.get_rect()
    pygame.draw.rect(surf, (0, 0, 0), (0, 0, 600, 60), 0)
    textrect1.center = (300, 20)  # (300, 250)
    textrect2.center = (300, 40)  # (300, 350)
    surf.blit(text1, textrect1)
    surf.blit(text2, textrect2)
    pygame.display.flip()
    waiting_end = True
    while waiting_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
    return surf


def get_location(coordinate):
    (x, y) = coordinate
    row = int(x // GRID) - 1
    col = int(y // GRID) - 1
    return row, col
