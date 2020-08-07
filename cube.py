from collections import deque
from random import choice

from numpy import full, rot90

COLORS = {
    'y': (255, 255, 0),
    'r': (255, 0, 0),
    'g': (0, 255, 0),
    'o': (255, 128, 0),
    'b': (0, 0, 255),
    'w': (255, 255, 255),}
ALL_SIDE_NAMES = 'ULFRBD'
NOTATION = {
    "2":2,
    "'":-1,
    2:"2",
    1:"",
    -1:"'"}

class Cube:

    def __init__(self):
        self.generate_solved_cube()

    def generate_solved_cube(self):
        '''Fills each side with 1 color'''

        self.sides = {}
        for side_name, color  in zip(ALL_SIDE_NAMES, COLORS):
            self.sides[side_name] = full((3, 3), color)

    def scramble(self, num_of_moves=30):
        '''Calls rotate_side with random moves'''

        side_names = []
        rotations = []
        for _ in range(num_of_moves):
            side_names.append(choice(ALL_SIDE_NAMES))
            rotations.append(choice([-1, 1, 2]))
        for side_name, rotation in zip(side_names, rotations):
            self.rotate_side(side_name, rotation)


    def rotate_side(self, side_name, rotation):
        '''First rotates the selected side,
           then finds the effect of rotation on other sides
           and shifts parts of them'''

        self.sides[side_name] = rot90(self.sides[side_name], k=-rotation)

        if side_name == 'U':
            sides_and_slices = [['B', 0],
                                ['R', 0],
                                ['F', 0],
                                ['L', 0]]
        elif side_name == 'L':
            sides_and_slices = [['U', (slice(None, None, None), 0)],
                                ['F', (slice(None, None, None), 0)],
                                ['D', (slice(None, None, None), 0)],
                                ['B', (slice(2, None, -1), 2)]]
        elif side_name == 'F':
            sides_and_slices = [['U', 2],
                                ['R', (slice(None, None, None), 0)],
                                ['D', (0, slice(2, None, -1))],
                                ['L', (slice(2, None, -1), 2)]]
        elif side_name == 'R':
            sides_and_slices = [['B', (slice(None, None, None), 0)],
                                ['D', (slice(2, None, -1), 2)],
                                ['F', (slice(2, None, -1), 2)],
                                ['U', (slice(2, None, -1), 2)]]
        elif side_name == 'B':
            sides_and_slices = [['R', (slice(2, None, -1), 2) ],
                                ['U', (0, slice(2, None, -1))],
                                ['L', (slice(None, None, None), 0)],
                                ['D', 2],]
        elif side_name == 'D':
            sides_and_slices = [['L', 2],
                                ['F', 2],
                                ['R', 2],
                                ['B', 2]]

        self._shift(sides_and_slices, rotation)

    def _shift(self, sides_and_slices, rotation):
        '''Shifts given slices of sides by
           a given ammount'''

        cur_slices = []
        for sid, sli in sides_and_slices:
            cur_slices.append(self.sides[sid][sli].copy())
        cur_slices = deque(cur_slices)
        cur_slices.rotate(rotation)

        for i, (sid, sli) in enumerate(sides_and_slices):
            self.sides[sid][sli] = cur_slices[i]


    def print_cube(self):
        for i in range(3):
            print(f"\t\t{self.sides['U'][i]}")
        print()
        for i in range(3):
            for side in 'LFRB':
                print(self.sides[side][i], end='\t')
            print()
        print()
        for i in range(3):
            print(f"\t\t{self.sides['D'][i]}")
        print('-' * 60)


    @staticmethod
    def from_notation(string):
        '''Translates string of notation
           (for example "R R2 U' B")
           into cube rotations'''

        moves = string.upper().split()
        side_names = []
        rotations = []
        for move in moves:
            side_names.append(move[0])
            if len(move) > 1:
                rotations.append(NOTATION[move[1]])
            else:
                rotations.append(1)
        return side_names, rotations

    @staticmethod
    def to_notation(side_names, rotations):
        '''Translates cube rotations into notation'''

        return_notation = []
        for side_name, rotation in zip(side_names, rotations):
            return_notation.append(f"{side_name}{NOTATION[rotation]}")
        return ' '.join(return_notation)


if __name__ == '__main__':
    c = Cube()

    c.print_cube()

    # test_rot = "R2 U R U R' U' R' U' R' U R'"
    # for s_n, r in zip(*c.from_notation(test_rot)):
    #     c.rotate_side(s_n, r)

    c.scramble(10)

    c.print_cube()
    # print(c.to_notation(s_n, r))
