import pygame, sys
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN

import cube


def assign_cube_coordinates(cube_to_assign, start_x, start_y, size_x, size_y):
    '''Assigns coordinates to each side.

       Preferably the ratio between size_x ans size_y is 4:3
       and size_x is divisible by 12 and size_y by 9.'''

    def assign_square_coordinates(side_name, start_side_x, start_side_y):
        '''Assigns coordinates to each square.'''

        side = c.sides[side_name]
        s_x, s_y = m_x // 3, m_y // 3 # width and height of each square
        SQUARE_SPACE_X = CUBE_WIDTH // 200
        SQUARE_SPACE_Y = CUBE_HEIGHT // 65

        for j in range(3):
            for i in range(3):
                side.squares[j][i].rect =  pygame.Rect(start_side_x + i * (m_x // 3),
                                                         start_side_y + j * (m_x // 3),
                                                         s_x - SQUARE_SPACE_X, s_y - SQUARE_SPACE_Y) # -1 for small edghes between squares

    x, y = size_x // 4, size_y // 3 # x, y of each side
    m_x, m_y = x - 3, y - 3 # modified side sizes to have spaces between sides

    c.sides['U'].rect = pygame.Rect(start_x + x, start_y, m_x, m_y)
    c.sides['L'].rect = pygame.Rect(start_x, start_y + y, m_x, m_y)
    c.sides['F'].rect = pygame.Rect(start_x + x, start_y + y, m_x, m_y)
    c.sides['R'].rect = pygame.Rect(start_x + 2 * x, start_y + y, m_x, m_y)
    c.sides['B'].rect = pygame.Rect(start_x + 3 * x, start_y + y, m_x, m_y)
    c.sides['D'].rect = pygame.Rect(start_x + x, start_y + 2 * y, m_x, m_y)

    assign_square_coordinates('U', start_x + x, start_y)
    assign_square_coordinates('L', start_x, start_y + y)
    assign_square_coordinates('F', start_x + x, start_y + y)
    assign_square_coordinates('R', start_x + 2 * x, start_y + y)
    assign_square_coordinates('B', start_x + 3 * x, start_y + y)
    assign_square_coordinates('D', start_x + x, start_y + 2 * y)

def draw_cube():
    '''Draws every square acording to assigned coordinates'''

    for side in c.sides.values():
        for j in range(3):
            for i in range(3):
                pygame.draw.rect(screen, cube.COLORS[side.squares[j][i].color], side.squares[j][i].rect)


TEXTS = {}
def assign_button_coordinates(names, start_x, start_y):
    '''Assigns each button its coordinates.
       The placement depends on the shape of BUTTON_NAMES'''

    max_j, max_i = len(names), len(names[0])
    j, i = BUTTONS_SHAPE
    for j in range(max_j):
        for i in range(max_i):
            BUTTONS[names[j][i]] = pygame.Rect(start_x + i * BUTTON_WIDTH, start_y + j * BUTTON_HEIGHT,
                                        BUTTON_WIDTH - 2, BUTTON_HEIGHT - 2)
            TEXTS[names[j][i]] = (start_x + i * BUTTON_WIDTH, start_y + j * BUTTON_HEIGHT)

def draw_text(text, font, color, surface, coordinates):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = coordinates
    surface.blit(textobj, textrect)

def draw_buttons():
    for text, button in zip(TEXTS.keys(), BUTTONS.values()):
        pygame.draw.rect(screen, BUTTON_COLOR, button)
        draw_text(text, FONT, TEXT_COLOR, screen, TEXTS[text])


COLOR_CHOICES = []
def assign_color_choice_coordinates(start_x, start_y):
    for i in range(6):
        COLOR_CHOICES.append(pygame.Rect(start_x + i * COLOR_CHOICE_WIDTH, start_y,
                                COLOR_CHOICE_WIDTH - 2, COLOR_CHOICE_HEIGHT - 2))

def draw_color_choices():
    for i, color in enumerate(cube.COLORS.values()):
        pygame.draw.rect(screen, color, COLOR_CHOICES[i])



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
BUTTON_NAMES = [['new', 'scramble'],
                ['do', 'o'],
                ['solve', 'options']]
BUTTONS_SHAPE = (len(BUTTON_NAMES), len(BUTTON_NAMES[0]))
assign_button_coordinates(BUTTON_NAMES,
               WIDTH - BUTTONS_SHAPE[1] * BUTTON_WIDTH // 0.9,
               HEIGHT - BUTTONS_SHAPE[0] * BUTTON_HEIGHT // 0.9)

FONT = pygame.font.SysFont('bahnschrift', 12)
TEXT_COLOR = (0, 0, 0)

COLOR_CHOICE_WIDTH = WIDTH // 18
COLOR_CHOICE_HEIGHT = COLOR_CHOICE_WIDTH
COLOR_CHOICE_X = WIDTH - 6 * COLOR_CHOICE_WIDTH
COLOR_CHOICE_Y = 1
assign_color_choice_coordinates(COLOR_CHOICE_X, COLOR_CHOICE_Y)

c = cube.Cube()
CUBE_WIDTH, CUBE_HEIGHT = WIDTH // 1.2, HEIGHT // 1.5
CUBE_X, CUBE_Y = WIDTH // 15, HEIGHT // 30
assign_cube_coordinates(c, CUBE_X, CUBE_Y, CUBE_WIDTH, CUBE_HEIGHT)
moves_to_do = zip(*c.from_notation("R2 U R U R' U' R' U' R' U R'2"))


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

        # if there are moves to do, do them
        try:
            side_name, rotation = next(moves_to_do)
            c.rotate_side(side_name, rotation)
        except StopIteration:
            pass

        screen.fill(BACKGROUND_COLOR)
        draw_cube()
        draw_color_choices()
        draw_buttons()

        mx, my = pygame.mouse.get_pos()
        if click:

            # used for painting the cube
            for side in c.sides.values():
                if side.rect.collidepoint((mx, my)):
                    for j in range(3):
                        for i in range(3):
                            if side.squares[j][i].rect.collidepoint((mx, my)):
                                side.squares[j][i].color = chosen_color
                    break

            # chosing painting color
            for i, color in enumerate(cube.COLORS):
                if COLOR_CHOICES[i].collidepoint((mx, my)):
                    chosen_color = color

            if BUTTONS['new'].collidepoint((mx, my)):
                c.generate_solved_cube()
            elif BUTTONS['scramble'].collidepoint((mx, my)):
                c.scramble()

        pygame.display.update()
        main_clock.tick(FPS)


main_menu()