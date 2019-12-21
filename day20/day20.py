"""day20.py
"""
import time

LETTERS = set(l for l in 'abcdefghijklmnopqrstuvwxyz')

class PortalMaze:
    def __init__(self, fname):
        self.map = {}
        self.portals = {}
        self.mapd = {}
        self.start = None
        self.end = None
        self.moves = ((0, 1), (1, 0), (0, -1), (-1, 0))
        self.xmax = 0
        self.ymax = 0
        self.read_data(fname)
        self.mark_portals()
        self.remove_dead_ends()
        self.outerportal = ((1, self.xmax-2), (1, self.ymax-1))

    def read_data(self, fname):
        with open(fname, 'r') as f:
            is_start_found = False
            for j, line in enumerate(f):
                for i, c in enumerate(line):
                    self.map[(i, j)] = c
                    if i > self.xmax:
                        self.xmax = i
                    if j > self.ymax:
                        self.ymax = j

    def is_outer(self, pos):
        if pos[0] in self.outerportal[0]:
            return True
        if pos[1] in self.outerportal[1]:
            return True
        return False

    def mark_portals(self):
        portals = {}
        for pos, c in self.map.items():
            if c == '.':
                for move in self.moves:
                    npos = tuple(a+b for a, b in zip(move, pos))
                    nc = self.map.get(npos, None)
                    if not nc is None and nc.lower() in LETTERS:
                        prev = tuple(a+b for a, b in zip(move, npos))
                        if move[0] < 0 or move[1] < 0:
                            name = self.map[prev] + nc
                        else:
                            name = nc + self.map[prev]
                        if name == 'AA':
                            self.start = pos
                            self.map[npos] = '#'
                        elif name == 'ZZ':
                            self.end = pos
                            self.map[npos] = '#'
                        else:
                            portals[name] = portals.get(name, list()) + [npos]
        for name, (p1, p2) in portals.items():
            for move in self.moves:
                npos = tuple(a+b for a,b in zip(move, p1))
                ch = self.map[npos]
                if ch == '.':
                    self.portals[p2] = npos
                    break
            for move in self.moves:
                npos = tuple(a+b for a,b in zip(move, p2))
                ch = self.map[npos]
                if ch == '.':
                    self.portals[p1] = npos
                    break

    def remove_dead_ends(self):
        allowed = set()
        for p in self.portals:
            start = self.portals[p]
            maze = self.explore_no_portals(start, 0)
            for end in list(self.portals.values()) + [self.start[:2], self.end[:2]]:
                if end in maze:
                    pos = end
                    odist = maze[pos]
                    allowed.add(pos)
                    while odist != 0:
                        odist = maze[pos]
                        for move in self.moves:
                            npos = tuple(a+b for a,b in zip(move, pos))
                            ndist = maze.get(npos, float('inf'))
                            if ndist == odist - 1:
                                allowed.add(npos)
                                pos = npos
                                    
        for pos, ch in self.map.items():
            if ch == '.' and not pos in allowed:
                self.map[pos] = '#'

    def explore_no_portals(self, start, dist):
        maze = {}
        q = [(start, dist)]
        while q:
            pos, dist = q.pop()
            ch = self.map.get(pos, None)
            if ch in ' #':
                continue
            else:
                if ch == '.':
                    odist = maze.get(pos, float('inf'))
                    if dist < odist:
                        maze[pos] = dist
                        for move in self.moves:
                            npos = tuple(a+b for a,b in zip(move, pos))
                            q.append((npos, dist+1))
        return maze


    def explore(self, start, dist):
        q = [(start, dist)]
        while q:
            pos, dist = q.pop()
            ch = self.map.get(pos, None)
            if ch in ' #':
                continue
            else:
                if ch.lower() in LETTERS:
                    pos = self.portals[pos]
                    ch = self.map[pos]

                if ch == '.':
                    odist = self.mapd.get(pos, float('inf'))
                    if dist < odist:
                        self.mapd[pos] = dist
                        for move in self.moves:
                            npos = tuple(a+b for a,b in zip(move, pos))
                            q.append((npos, dist+1))

    def draw(self):
        out = []
        for y in range(self.ymax+1):
            out.append(''.join(self.map[(x, y)] for x in range(self.xmax)))
        return '\n'.join(out)


class PortalMazeRecursive(PortalMaze):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def explore(self, start, layer, dist, limit=25):
        q = [(start, layer, dist)]
        while q:
            pos, layer, dist = q.pop()
            if layer > limit or layer < 0:
                continue
            ch = self.map.get(pos, None)
            if ch in ' #':
                continue
            else:
                if ch.lower() in LETTERS:
                    if self.is_outer(pos):
                        layer -= 1
                    else:
                        layer += 1
                    pos = self.portals[pos]
                    ch = self.map[pos]

                if ch == '.':
                    lpos = pos + (layer,)
                    odist = self.mapd.get(lpos, float('inf'))
                    if dist < odist:
                        self.mapd[lpos] = dist
                        for move in self.moves:
                            npos = tuple(a+b for a,b in zip(move, pos))
                            q.append((npos, layer, dist+1))

    def mark_portals(self):
        super().mark_portals()
        self.start = self.start + (0,)
        self.end = self.end + (0,)


if __name__ == '__main__':
    start = time.time()

    # Part 1
    pm = PortalMaze('data.txt')
    pm.explore(pm.start, 0)
    print(f'Shortest path: {pm.mapd[pm.end]}')

    # Part 2
    pm2 = PortalMazeRecursive('data.txt')
    pm2.explore(pm2.start[:2], 0, 0, limit=25)
    shortest = pm2.mapd[pm2.end]
    print(f'Shortest path: {shortest}')

    end = time.time()
    print(f'Finish Time: {(end-start):.2f}')