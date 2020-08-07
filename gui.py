import pygame, sys
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN

import pygame_textinput
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


FPS = 10
BACKGROUND_COLOR = (64, 64, 64)
WIDTH, HEIGHT = 500, 500
main_clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Rubiks cube simulator')
screen = pygame.display.set_mode((WIDTH, HEIGHT))

BUTTON_COLOR = (0, 240, 255)
BUTTON_WIDTH, BUTTON_HEIGHT = WIDTH // 8, HEIGHT // 15
BUTTONS = {}
BUTTON_NAMES = [['new', 'clear'],
                ['do', 'scramble'],
                ['solve', 'options']]
BUTTONS_SHAPE = (len(BUTTON_NAMES), len(BUTTON_NAMES[0]))


FONT = pygame.font.SysFont('arialrounded', 12)
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

text_input = pygame_textinput.TextInput()

c = cube.Cube()
moves_to_do = zip(*c.from_notation("R2 U R U R' U' R' U' R' U R'"))

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
        except:
            pass
        draw_cube(c, 50, 50, 360, 270)

        mx, my = pygame.mouse.get_pos()
        if click:
            if BUTTONS['new'].collidepoint((mx, my)):
                c.generate_solved_cube()
            elif BUTTONS['scramble'].collidepoint((mx, my)):
                c.scramble()

        # Feed it with events every frame
        text_input.update(events)
        # Blit its surface onto the screen
        screen.blit(text_input.get_surface(), (100, 100))

        for text, button in zip(TEXTS.keys(), BUTTONS.values()):
            pygame.draw.rect(screen, BUTTON_COLOR, button)
            draw_text(text, FONT, TEXT_COLOR, screen, TEXTS[text])

        pygame.display.update()
        main_clock.tick(FPS)


main_menu()