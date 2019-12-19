"""day17.py
"""
from computer import Computer

class Aft(Computer):
    def __init__(self, *args, **kwargs):
        self.view = None
        super().__init__(*args, **kwargs)

    def get_view(self):
        if self.view is None:
            self.run()
            out = []
            for ch in self.output:
                out.append(str(chr(ch)))
            self.view = ''.join(out).strip()
        return self.view

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


if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        data = list(map(int, f.read().strip().split(',')))
        # print(data)
        aft = Aft(list(data))
        view = aft.get_view()
        print(view)
        print(aft.sum_alignment_params())

        data[0] = 2
        