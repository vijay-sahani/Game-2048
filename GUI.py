import sys
import pygame
from Spot import Spot
from main import Game2048

# pygame initialization
pygame.init()
pygame.font.init()
pygame.display.set_caption("Classic 2048")
# constants
EXTRA_HEIGHT = 50
WIDTH = 600
SCREEN = pygame.display.set_mode((WIDTH, WIDTH+EXTRA_HEIGHT), pygame.RESIZABLE)
ROWS = 4
TILE_SIZE = WIDTH//ROWS

fnt = pygame.font.SysFont("comiscans", TILE_SIZE)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
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


def get_clicked_pos(pos, rows, width, height) -> tuple[int]:
    gap1 = width // rows
    gap2 = height//rows
    x, y = pos
    row = x // gap1
    col = y // gap2
    if col < rows and col >= 0 and row < rows and row >= 0:
        return row, col
    return None


def build_board(rows, width, height) -> list[list:Spot]:
    grid = []
    gap1 = width // rows
    gap2 = height//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap1, gap2, rows)
            grid[i].append(spot)
    return grid


def font_helper(text, size, color=GREY):
    font = pygame.font.SysFont("comiscans", size)
    return font.render(text, True, color)


def show_score(screen, score: str, width, height):
    pos = pygame.Rect(0, height, width, EXTRA_HEIGHT)
    score_text = font_helper("Score: "+score, EXTRA_HEIGHT)
    screen.blit(score_text, score_text.get_rect(center=pos.center))


def draw_board_lines(screen, rows, width, height):
    gap1 = width // rows
    gap2 = height//rows
    for i in range(rows):
        pygame.draw.line(screen, GREY, (0, i*gap2),
                         (width, i*gap2), 3)
        for j in range(rows):
            pygame.draw.line(screen, GREY, (j*gap1, 0),
                             (j*gap1, height), 3)


def draw_changes(screen, rows, width, height, spot: Spot):
    TILE1 = width // rows
    TILE2 = height // rows
    num = font_helper(spot.number, TILE2 if spot.number != None and len(
        spot.number) < 3 else TILE2-(TILE2*40)//100, (0, 0, 0))
    x, y = get_clicked_pos((spot.x, spot.y), rows, width, height)
    pos = pygame.Rect(x * TILE1+1, y *
                      TILE2 + 1, TILE1, TILE2)
    if (COLORS.get(spot.number)):
        spot.set_color(COLORS.get(spot.number))
    screen.fill(spot.color, (x * TILE1+1, y *
                             TILE2 + 1, TILE1, TILE2))
    screen.blit(num, num.get_rect(center=pos.center))
    draw_board_lines(screen, rows,  width, height)
    pygame.display.update()
    pygame.time.delay(100*(10-rows)//10)  # reducing speed of delay by rows*10%


def draw(screen, grid: list[list:Spot], rows, width, height):
    TILE1 = width // rows
    TILE2 = height // rows
    screen.fill(WHITE)
    for row in grid:
        for spot in row:
            # update the size of font dynamically
            # if the size of the text is 3 or more which overflow's the board tile
            # so the font size is reduced by 40% to fit inside the tile size
            num = font_helper(spot.number, TILE2 if spot.number != None and len(
                spot.number) < 3 else TILE2-(TILE2*40)//100, (0, 0, 0))
            x, y = get_clicked_pos((spot.x, spot.y), rows, width, height)
            pos = pygame.Rect(x * TILE1+1, y *
                              TILE2 + 1, TILE1, TILE2)
            if (COLORS.get(spot.number)):
                spot.set_color(COLORS.get(spot.number))
            screen.fill(spot.color, (x * TILE1+1, y *
                                     TILE2 + 1, TILE1, TILE2))
            screen.blit(num, num.get_rect(center=pos.center))
    draw_board_lines(screen, rows,  width, height)


def get_square_under_mouse(board, rows, width, height):
    TILE1 = width // rows
    TILE2 = height // rows
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    x, y = [int(mouse_pos[0]//TILE1), int(mouse_pos[1]//TILE2)]
    try:
        if x >= 0 and y >= 0:
            return (board[y][x], x, y)
    except IndexError:
        pass
    return None, None, None


def update_board_size(board: list[list[Spot]], rows, width, height):
    gap1 = width // rows
    gap2 = height//rows
    for i in range(rows):
        for j in range(rows):
            board[i][j].update_height_width(gap1, gap2)


def main(screen, rows, width, height):
    grid: list[list:Spot] = build_board(rows, width, height)
    run = True
    selected_pos = None
    game_util = Game2048(rows)
    game_util.make_random_move(grid)
    TILE1 = width // rows
    TILE2 = height // rows
    while run:
        draw(screen, grid, rows, width, height)

        piece, x, y = get_square_under_mouse(grid, rows, width, height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or game_util.game_over(grid):
                run = False
                print("Game over")

            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE)
                width = event.w
                height = event.h-EXTRA_HEIGHT
                TILE1 = width // rows
                TILE2 = height // rows
                update_board_size(grid, rows, width, height)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                temp = selected_pos
                selected_pos = get_clicked_pos(pos, rows, width, height)
                try:
                    spot: Spot = grid[selected_pos[0]][selected_pos[1]]
                    if (spot.is_Empty() or temp == selected_pos):
                        selected_pos = None
                except:
                    pass

            elif (selected_pos and event.type == pygame.MOUSEMOTION):
                pos = pygame.mouse.get_pos()
                current_pos = get_clicked_pos(pos, rows, width, height)
                if (current_pos != None and selected_pos != current_pos):
                    game_util.update_board(
                        grid, selected_pos, current_pos, lambda spot: draw_changes(screen, rows, width, height, spot))
                    selected_pos = None
        if x != None and selected_pos != None:
            rect = (x * TILE1,
                    y * TILE2, TILE1, TILE2)
            pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)
        show_score(screen, str(game_util.score), width, height)
        pygame.display.flip()
        clock.tick(30)


def draw_text(text, pos, font, color, surface):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=pos.center)
    surface.blit(textobj, textrect)


def options_menu(screen, width, height):
    click = False
    BOX_SIZE = 200
    font = pygame.font.SysFont(None, BOX_SIZE//2)
    rows: list = (4, 5, 6, 7)  # Board rows
    while True:
        screen.fill(WHITE)
        draw_board_lines(screen, 4,  width, height+EXTRA_HEIGHT)
        title = font_helper("Choose board size", EXTRA_HEIGHT, BLACK)
        screen.blit(title, title.get_rect(center=(width // 2, 50)))
        mx, my = pygame.mouse.get_pos()
        offset = 0
        for row in rows:
            button = pygame.Rect(
                width//2-BOX_SIZE//2, 200-BOX_SIZE//2+offset, BOX_SIZE, BOX_SIZE//2)
            if button.collidepoint((mx, my)):
                if click:
                    main(screen, row, width, height)
            pygame.draw.rect(screen, GREY, button)
            draw_text(f'{row} x {row}', button,
                      font, WHITE, screen)
            offset += BOX_SIZE//2+10

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE)
                width = event.w
                height = event.h-EXTRA_HEIGHT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    options_menu(SCREEN, WIDTH, WIDTH)
