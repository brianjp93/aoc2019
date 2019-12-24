"""day17.py
"""
from computer import Computer

class Aft(Computer):
    def __init__(self, *args, **kwargs):
        self.pos = (0, 0)
        self.view = None
        self.moves = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0)
        ]
        self.facing = 2
        self.start = None
        self.end = None
        self.total_moves = None
        super().__init__(*args, **kwargs)
        self.get_view()
        self.get_start()

    def init2(self):
        self.reset()
        self.program[0] = 2

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
        view = self.get_view().strip().split('\n')
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
                if view[y][x] == '#':
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
        if self.total_moves:
            return self.total_moves

        total_moves = []
        view = self.get_view().split('\n')
        pos = self.start

        move_len = 0
        while pos != self.end:
            move = self.moves[self.facing]
            left_move = self.moves[(self.facing + 1) % 4]
            right_move = self.moves[(self.facing - 1) % 4]
            npos = tuple(a+b for a,b in zip(pos, move))
            left = tuple(a+b for a,b in zip(pos, left_move))
            right = tuple(a+b for a,b in zip(pos, right_move))
            # print(npos, left, right)
            nx, ny = npos
            if nx in range(len(view[0])) and ny in range(len(view)) and view[ny][nx] == '#':
                move_len += 1
                pos = npos
            elif left[0] in range(len(view[0])) and left[1] in range(len(view)) and view[left[1]][left[0]] == '#':
                total_moves.append(move_len)
                total_moves.append('L')
                move_len = 1
                pos = left
                self.facing = (self.facing + 1) % 4
            elif right[0] in range(len(view[0])) and right[1] in range(len(view)) and view[right[1]][right[0]] == '#':
                total_moves.append(move_len)
                total_moves.append('R')
                move_len = 1
                pos = right
                self.facing = (self.facing - 1) % 4
            else:
                print('???')

        total_moves.append(move_len)
        total_moves = list(map(str, total_moves))
        total_moves = [''.join(total_moves[i: i+2]) for i in range(1, len(total_moves), 2)]
        self.total_moves = total_moves
        return total_moves

    def get_parts(self):
        total_moves = ''.join(self.total_moves)
        a = 'L4L12R10L4L12L6L4'
        b = 'L6R8L4R8L12'
        c = 'L12R10L4'

        parts = [a, b, c]
        for part in parts:
            total_moves = ''.join(total_moves.split(part))
            print(total_moves)
        

    def send_parts(self):
        self.init2()
        self.run()
        self.output = []
        main = 'C,A,A,B,A,B,A,B,C,C'
        a = 'L,12,R,10,L,4'
        b = 'L,12,L,6,L,4,L,4'
        c = 'L,6,R,8,L,4,R,8,L,12'
        # print(''.join([c, a, a, b, a, b, a, b, c, c]))
        instr = '\n'.join([main, a, b, c]) + '\n'
        instr += 'n\n'
        instr = [ord(x) for x in instr]
        self.inputs += instr
        # print(self.inputs)
        self.run()
        return self.output[-1]


if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        data = list(map(int, f.read().strip().split(',')))
        # print(data)
        aft = Aft(list(data))
        view = aft.get_view()
        # print(view)
        print(aft.sum_alignment_params())

        aft = Aft(list(data))

        out = aft.send_parts()
        print(out)
