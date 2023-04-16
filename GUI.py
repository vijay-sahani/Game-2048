from numpy import array
import pygame
from pygame.constants import KEYDOWN, KEYUP, K_SPACE
from Spot import Spot
from main import Game2048

# pygame initialization
pygame.init()
pygame.font.init()

# constants
EXTRA_HEIGHT = 50
WIDTH = 600
SCREEN = pygame.display.set_mode((WIDTH, WIDTH+EXTRA_HEIGHT), pygame.RESIZABLE)
ROWS = 4
TILE_SIZE = WIDTH//ROWS

fnt = pygame.font.SysFont("comiscans", TILE_SIZE)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
COLORS = {
    '2': (238, 228, 218),
    '4': (237, 224, 200),
    '8': (242, 177, 121),
    '16': (245, 149, 99),
    '32': (246, 124, 95),
    '64': (246, 94, 59),
    '128': (237, 207, 114),
    '256': (237, 204, 97),
    '512': (237, 200, 80),
    '1024': (237, 197, 63),
    '2048': (237, 194, 46)
}


def get_clicked_pos(pos, ROWS, width, height) -> tuple[int]:
    gap1 = width // ROWS
    gap2 = height//ROWS
    x, y = pos
    row = x // gap1
    col = y // gap2
    return row, col


def make_grid(ROWS, width, height) -> list[list:Spot]:
    grid = []
    gap1 = width // ROWS
    gap2 = height//ROWS
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            spot = Spot(i, j, gap1, gap2, ROWS)
            grid[i].append(spot)
    return grid


def font_helper(text, size, color=GREY):
    font = pygame.font.SysFont("comiscans", size)
    return font.render(text, True, color)


def show_score(screen, score: str, width, height):
    pos = pygame.Rect(0, height, width, EXTRA_HEIGHT)
    score_text = font_helper("Score: "+score, EXTRA_HEIGHT)
    screen.blit(score_text, score_text.get_rect(center=pos.center))


def draw_grid(screen, ROWS, width, height):
    gap1 = width // ROWS
    gap2 = height//ROWS
    for i in range(ROWS):
        pygame.draw.line(screen, GREY, (0, i*gap2),
                         (width, i*gap2), 3)
        for j in range(ROWS):
            pygame.draw.line(screen, GREY, (j*gap1, 0),
                             (j*gap1, height), 3)


def draw(screen, grid: list[list:Spot], ROWS, width, height):
    TILE1 = width // ROWS
    TILE2 = height // ROWS
    screen.fill(WHITE)
    for row in grid:
        for spot in row:
            # update the size of font dynamically
            # if the size of the text is 3 or more which overflow's the board tile
            # so the font size is reduced by 40% to fit inside the tile size
            num = font_helper(spot.number, TILE2 if spot.number != None and len(
                spot.number) < 3 else TILE2-(TILE2*40)//100, (0, 0, 0))
            x, y = get_clicked_pos((spot.x, spot.y), ROWS, width, height)
            pos = pygame.Rect(x * TILE1+1, y *
                              TILE2 + 1, TILE1, TILE2)
            if(COLORS.get(spot.number)):
                spot.set_color(COLORS.get(spot.number))
            screen.fill(spot.color, (x * TILE1+1, y *
                                     TILE2 + 1, TILE1, TILE2))
            screen.blit(num, num.get_rect(center=pos.center))
    draw_grid(screen, ROWS,  width, height)


def get_square_under_mouse(board, width, height):
    TILE1 = width // ROWS
    TILE2 = height // ROWS
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    x, y = [int(mouse_pos[0]//TILE1), int(mouse_pos[1]//TILE2)]
    try:
        if x >= 0 and y >= 0:
            return (board[y][x], x, y)
    except IndexError:
        pass
    return None, None, None


def update_make_grid(board: list[list[Spot]], width, height):
    gap1 = width // ROWS
    gap2 = height//ROWS
    for i in range(ROWS):
        for j in range(ROWS):
            board[i][j].update_height_width(gap1, gap2)


def main(screen, width, height):
    grid: list[list:Spot] = make_grid(ROWS, width, height)
    clock = pygame.time.Clock()
    run = True
    selected_pos = None
    game_util = Game2048()
    game_util.make_random_move(grid)
    TILE1 = width // ROWS
    TILE2 = height // ROWS
    while run:
        draw(screen, grid, ROWS, width, height)
        piece, x, y = get_square_under_mouse(grid, width, height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or game_util.game_over():
                run = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE)
                width = event.w
                height = event.h-EXTRA_HEIGHT
                TILE1 = width // ROWS
                TILE2 = height // ROWS
                update_make_grid(grid, width, height)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                temp = selected_pos
                selected_pos = get_clicked_pos(pos, ROWS, width, height)
                try:
                    spot: Spot = grid[selected_pos[0]][selected_pos[1]]
                    if(spot.is_Empty() or temp == selected_pos):
                        selected_pos = None
                except:
                    pass

            elif(selected_pos):
                if event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    current_pos = get_clicked_pos(pos, ROWS, width, height)
                    if(current_pos[1] != 4 and selected_pos != current_pos):
                        game_util.update_board(grid, selected_pos, current_pos)
                        selected_pos = None
        if x != None and selected_pos != None:
            rect = (x * TILE1,
                    y * TILE2, TILE1, TILE2)
            pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)
        show_score(screen, str(game_util.score), width, height)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == "__main__":
    main(SCREEN, WIDTH, WIDTH)
