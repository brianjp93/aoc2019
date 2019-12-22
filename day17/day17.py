"""day17.py
"""
from computer import Computer

class Aft(Computer):
    def __init__(self, *args, **kwargs):
        self.pos = (0, 0)
        self.view = None
        self.moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.facing = 0
        self.start = None
        self.end = None
        super().__init__(*args, **kwargs)
        self.get_view()
        self.get_start()

    def get_view(self):
        if self.view is None:
            self.run()
            out = []
            for ch in self.output:
                ch = str(chr(ch))
                out.append(ch)
            self.view = ''.join(out).strip()
        return self.view

    def get_start(self):
        view = self.get_view().split('\n')
        for y in range(len(view)):
            for x in range(len(view[y])):
                if view[y][x] == '^':
                    self.start = (x, y)
                near = (
                    view[y-1][x] if y-1 >= 0 else '',
                    view[y+1][x] if y+1 < len(view) else '',
                    view[y][x-1] if x-1 >=0 else '',
                    view[y][x+1] if x+1 < len(view[y]) else ''
                )
                if near.count('#') == 1 and near.count('^') != 1:
                    self.end = (x, y)

    def find_intersections(self):
        view = self.get_view().split('\n')
        intersections = []
        for y, line in enumerate(view[1: -1]):
            y += 1
            for x, ch in enumerate(line[1: -1]):
                x += 1
                if ch == '#':
                    if (view[y-1][x], view[y+1][x], view[y][x-1], view[y][x+1]) == ('#', '#', '#', '#'):
                        intersections.append((x, y))
        return intersections

    def sum_alignment_params(self):
        return sum(a*b for a, b in self.find_intersections())

    def get_movement_commands(self):
        pos = self.start
        move = self.dirs[self.facing]
        npos = None


if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        data = list(map(int, f.read().strip().split(',')))
        # print(data)
        aft = Aft(list(data))
        view = aft.get_view()
        print(view)
        print(aft.sum_alignment_params())

        data[0] = 2

        aft = Aft(list(data))
        print(aft.start)
        # view = 