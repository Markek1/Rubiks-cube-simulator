import pygame, sys
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN

import cube


def draw_cube(cube_to_draw, start_x, start_y, size_x, size_y):
    '''Preferably the ratio between size_x ans size_y is 4:3
       and size_x is divisible by 12 and size_y by 9'''

    def draw_side(side, start_side_x, start_side_y):
        s_x, s_y = m_x // 3, m_y // 3 # width and height of each square
        for j in range(3):
            for i in range(3):
                pygame.draw.rect(screen, cube.COLORS[side[j][i]],
                                pygame.Rect(start_side_x + i * (m_x // 3),
                                            start_side_y + j * (m_x // 3),
                                            s_x - 1, s_y - 1)) # -1 for small edghes between squares

    x, y = size_x // 4, size_y // 3 # x, y of each side
    m_x, m_y = x - 3, y - 3 # modified side sizes to have spaces between sides
    draw_side(cube_to_draw.sides['U'], start_x + x, start_y)
    draw_side(cube_to_draw.sides['L'], start_x, start_y + y)
    draw_side(cube_to_draw.sides['F'], start_x + x, start_y + y)
    draw_side(cube_to_draw.sides['R'], start_x + 2 * x, start_y + y)
    draw_side(cube_to_draw.sides['B'], start_x + 3 * x, start_y + y)
    draw_side(cube_to_draw.sides['D'], start_x + x, start_y + 2 * y)


def draw_buttons(button, color):
    if not edge_color:
        edge_color = color
    pygame.draw.rect(screen, color, button)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


FPS = 5
BACKGROUND_COLOR = (64, 64, 64)
BUTTON_COLOR = (0, 200, 255)
WIDTH, HEIGHT = 500, 500
main_clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Rubiks cube simulator')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 20)

c = cube.Cube()
moves_to_do = "R2 U R U R' U' R' U' R' U R'"

buttons = {}


def main_menu():
    while True:
        for side_name, rotation in zip(*c.from_notation(moves_to_do)):

            click = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            screen.fill(BACKGROUND_COLOR)

            c.rotate_side(side_name, rotation)
            draw_cube(c, 50, 50, 360, 270)

            draw_text('Main Menu', font, (255, 255, 255), screen, 20, 20)

            # mx, my = pygame.mouse.get_pos()

            button_new = pygame.Rect(WIDTH - WIDTH // 4, HEIGHT - HEIGHT // 4, WIDTH // 10, HEIGHT // 20)
            # button_2 = pygame.Rect(50, 200, 200, 50)

            if click:
                if button_1.collidepoint((mx, my)):
                    pass

            pygame.draw.rect(screen, BUTTON_COLOR, button_new)
            # pygame.draw.rect(screen, (255, 0, 0), button_2)

            pygame.display.update()
            main_clock.tick(FPS)


main_menu()