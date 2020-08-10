import pygame, sys
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN

import cube


def assign_cube_coors(cube_to_assign, start_x, start_y, size_x, size_y):
    '''Preferably the ratio between size_x ans size_y is 4:3
       and size_x is divisible by 12 and size_y by 9'''

    def assign_side_coors(side_name, start_side_x, start_side_y):
        side = c.sides[side_name]
        s_x, s_y = m_x // 3, m_y // 3 # width and height of each square
        for j in range(3):
            for i in range(3):
                side.squares[j][i].rect =  pygame.Rect(start_side_x + i * (m_x // 3),
                                                         start_side_y + j * (m_x // 3),
                                                         s_x - 1, s_y - 1) # -1 for small edghes between squares

    x, y = size_x // 4, size_y // 3 # x, y of each side
    m_x, m_y = x - 3, y - 3 # modified side sizes to have spaces between sides

    c.sides['U'].rect = pygame.Rect(start_x + x, start_y, m_x, m_y)
    c.sides['L'].rect = pygame.Rect(start_x, start_y + y, m_x, m_y)
    c.sides['F'].rect = pygame.Rect(start_x + x, start_y + y, m_x, m_y)
    c.sides['R'].rect = pygame.Rect(start_x + 2 * x, start_y + y, m_x, m_y)
    c.sides['B'].rect = pygame.Rect(start_x + 3 * x, start_y + y, m_x, m_y)
    c.sides['D'].rect = pygame.Rect(start_x + x, start_y + 2 * y, m_x, m_y)

    assign_side_coors('U', start_x + x, start_y)
    assign_side_coors('L', start_x, start_y + y)
    assign_side_coors('F', start_x + x, start_y + y)
    assign_side_coors('R', start_x + 2 * x, start_y + y)
    assign_side_coors('B', start_x + 3 * x, start_y + y)
    assign_side_coors('D', start_x + x, start_y + 2 * y)


def draw_squares():
    for side in c.sides.values():
        for j in range(3):
            for i in range(3):
                pygame.draw.rect(screen, cube.COLORS[side.squares[j][i].color], side.squares[j][i].rect)


c = cube.Cube()
assign_cube_coors(c, 50, 5, 360, 270)
moves_to_do = zip(*c.from_notation("R2 U R U R' U' R' U' R' U R'2"))


FPS = 10
BACKGROUND_COLOR = (64, 64, 64)
WIDTH, HEIGHT = 500, 500
main_clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Rubiks cube simulator')
screen = pygame.display.set_mode((WIDTH, HEIGHT))

BUTTON_COLOR = (100,238,255)
BUTTON_WIDTH, BUTTON_HEIGHT = WIDTH // 8, HEIGHT // 15
BUTTONS = {}
BUTTON_NAMES = [['new', 'clear'],
                ['do', 'scramble'],
                ['solve', 'options']]
BUTTONS_SHAPE = (len(BUTTON_NAMES), len(BUTTON_NAMES[0]))


FONT = pygame.font.SysFont('bahnschrift', 12)
TEXTS = {}
TEXT_COLOR = (0, 0, 0)


def draw_text(text, font, color, surface, coordinates):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = coordinates
    surface.blit(textobj, textrect)

def create_buttons(names, start_x, start_y):
    max_j, max_i = len(names), len(names[0])
    j, i = BUTTONS_SHAPE
    for j in range(max_j):
        for i in range(max_i):
            BUTTONS[names[j][i]] = pygame.Rect(start_x + i * BUTTON_WIDTH, start_y + j * BUTTON_HEIGHT,
                                        BUTTON_WIDTH - 2, BUTTON_HEIGHT - 2)
            TEXTS[names[j][i]] = (start_x + i * BUTTON_WIDTH, start_y + j * BUTTON_HEIGHT)

create_buttons(BUTTON_NAMES,
               WIDTH - BUTTONS_SHAPE[1] * BUTTON_WIDTH // 0.9,
               HEIGHT - BUTTONS_SHAPE[0] * BUTTON_HEIGHT // 0.9)


def main_menu():
    while True:
        click = False

        events = pygame.event.get()

        for event in events:
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

        # if there are moves to do, do them and draw the cube
        try:
            side_name, rotation = next(moves_to_do)
            c.rotate_side(side_name, rotation)
            c.print_cube()
        except:
            pass

        draw_squares()

        mx, my = pygame.mouse.get_pos()
        if click:
            if BUTTONS['new'].collidepoint((mx, my)):
                c.generate_solved_cube()
            elif BUTTONS['scramble'].collidepoint((mx, my)):
                c.scramble()

        for text, button in zip(TEXTS.keys(), BUTTONS.values()):
            pygame.draw.rect(screen, BUTTON_COLOR, button)
            draw_text(text, FONT, TEXT_COLOR, screen, TEXTS[text])

        pygame.display.update()
        main_clock.tick(FPS)


main_menu()