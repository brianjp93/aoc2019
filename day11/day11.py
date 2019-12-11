"""day11.py
"""
from computer import Computer

class HullPaintingRobot:
    def __init__(self):
        self.current = (0, 0)
        self.directions = '^>v<'
        self.facing = '^'
        self.move = {
            '^': (0, 1),
            '>': (1, 0),
            'v': (0, -1),
            '<': (-1, 0)
        }
        self.matrix = {}

    def get(self, coord):
        return self.matrix.get(coord, '.')

    def current_color(self):
        return 0 if self.get(self.current) == '.' else 1

    def paint(self, color):
        self.matrix[self.current] = color

    def command(self, c1, c2):
        self.paint('#' if int(c1) else '.')
        facing_index = self.directions.index(self.facing)
        facing_index = facing_index + 1 if int(c2) else facing_index - 1
        if facing_index >= len(self.directions):
            facing_index = facing_index % 4
        self.facing = self.directions[facing_index]
        self.current = tuple(a+b for a, b in zip(self.current, self.move[self.facing]))

    def draw(self):
        max_x = max(self.matrix.keys(), key=lambda x: x[0])[0]
        min_x = min(self.matrix.keys(), key=lambda x: x[0])[0]
        max_y = max(self.matrix.keys(), key=lambda x: x[1])[1]
        min_y = min(self.matrix.keys(), key=lambda x: x[1])[1]
        for y in reversed(range(min_y, max_y+1)):
            for x in range(min_x, max_x+1):
                print(self.matrix.get((x, y), ' '), end='')
            print()


def run_robot(data, start_input):
    robot = HullPaintingRobot()
    comp = Computer(list(data), inputs=[start_input])
    output = None
    last_index = 0
    while output != 'HALT':
        output = comp.run()
        new_outputs = comp.output[last_index:]
        last_index = len(comp.output)
        robot.command(new_outputs[0], new_outputs[1])
        if output == 'HALT':
            break
        comp.inputs.append(robot.current_color())

    return robot


if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        data = list(map(int, f.read().split(',')))
        
        robot = run_robot(list(data), 0)
        print(f'Painted Pixels: {len(robot.matrix.values())}')
        print()
        robot = run_robot(list(data), 1)
        print('v LICENSE v')
        robot.draw()
