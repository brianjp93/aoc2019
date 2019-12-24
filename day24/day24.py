"""day24.py

https://adventofcode.com/2019/day/24

"""

dat = '''
#..##
##...
.#.#.
#####
####.
'''.strip()


class Eris:
    def __init__(self, dat):
        self.dat = self.read_data(dat)
        self.prev = set()

    def read_data(self, dat):
        d = {}
        for y, line in enumerate(dat.split('\n')):
            for x, c in enumerate(line):
                d[(x, y)] = c
        return d

    def next(self):
        state = {}
        for coord, c in self.dat.items():
            x, y = coord
            close = self.get_close(x, y)
            close_vals = tuple(self.dat.get(xy, '.') for xy in close)
            bcount = close_vals.count('#')
            if c == '.':
                if bcount <= 2 and bcount > 0:
                    state[coord] = '#'
                else:
                    state[coord] = '.'
            elif c == '#':
                if close_vals.count('#') == 1:
                    state[coord] = '#'
                else:
                    state[coord] = '.'
            else:
                print('????')
                raise Exception('WTF')
        self.dat = state

    def stop_at_repeat(self):
        state = self.get_state()
        self.prev.add(state)
        n = 0
        while True:
            self.next()
            state = self.get_state()
            if state in self.prev:
                print(f'Found State after {n} states.')
                break
            self.prev.add(state)
            n += 1


    def get_state(self):
        state = []
        for y in range(5):
            for x in range(5):
                if c := self.dat[(x, y)] == '#':
                    state.append((x, y))
        return tuple(state)

    def get_close(self, x, y):
        # up right down left
        return ((x, y+1), (x+1, y), (x, y-1), (x-1, y))

    def get_rating(self):
        drawing = ''.join(self.draw().split('\n'))
        return sum(2**i for i, x in enumerate(drawing) if x == '#')

    def draw(self):
        out = []
        for y in range(5):
            out.append(''.join([self.dat[(x, y)] for x in range(5)]))
        return '\n'.join(out)



if __name__ == '__main__':
    eris = Eris(dat)
    # print(eris.draw())
    eris.stop_at_repeat()
    # print(eris.draw())
    rating = eris.get_rating()
    print(rating)


    d = set()
    for y, line in enumerate(dat.split('\n')):
        for x, c in enumerate(line):
            if c == '#':
                d.add((x, y, 0))

    repeat = 200
    for _ in range(repeat):
        adj = {}
        for coord in d:
            x, y, layer = coord
            close = ((x+1, y), (x-1, y), (x, y-1), (x, y+1))
            for ncoord in close:
                if ncoord == (2, 2):
                    nlayer = layer - 1
                    if x == 1:
                        for ny in range(5):
                            nc = (0, ny, nlayer)
                            adj[nc] = adj.get(nc, 0) + 1
                    elif x == 3:
                        for ny in range(5):
                            nc = (4, ny, nlayer)
                            adj[nc] = adj.get(nc, 0) + 1
                    elif y == 1:
                        for nx in range(5):
                            nc = (nx, 0, nlayer)
                            adj[nc] = adj.get(nc, 0) + 1
                    elif y == 3:
                        for nx in range(5):
                            nc = (nx, 4, nlayer)
                            adj[nc] = adj.get(nc, 0) + 1
                    else:
                        raise Exception()

                elif any(n in (-1, 5) for n in ncoord):
                    nlayer = layer + 1
                    if ncoord[0] == -1:
                        nc = (1, 2, nlayer)
                    elif ncoord[0] == 5:
                        nc = (3, 2, nlayer)
                    if ncoord[1] == -1:
                        nc = (2, 1, nlayer)
                    elif ncoord[1] == 5:
                        nc = (2, 3, nlayer)
                    adj[nc] = adj.get(nc, 0) + 1
                else:
                    nc = (ncoord[0], ncoord[1], layer)
                    adj[nc] = adj.get(nc, 0) + 1

        nstate = set()
        for coord, n in adj.items():
            if coord in d:
                if n == 1:
                    nstate.add(coord)
            elif n in [1, 2]:
                    nstate.add(coord)
        d = nstate

    print(f'Bugs after {repeat} minutes: {len(d)}')
