"""day18.py
"""

LETTERS = 'abcdefghijklmnopqrstuvwxyz'

class Robit:
    def __init__(self, data):
        self.data = data
        self.start = self.get_start()
        self.keys = {}
        self.key_count = self.count_keys()
        self.current = self.start
        self.moves = (
            (1, 0),
            (0, -1),
            (-1, 0),
            (0, 1)
        )
        self.maze = {}
        self.open_maze = {}
        self.distance_from = {}

    def get_start(self):
        for y, line in enumerate(self.data):
            for x, ch in enumerate(line):
                if ch == '@':
                    self.data[y][x] = '.'
                    return (x, y)

    def count_keys(self):
        count = 0
        for y,line in enumerate(self.data):
            for x, ch in enumerate(line):
                if ch in LETTERS:
                    self.keys[ch] = x,y
                    count += 1
        return count


    def explore(self, start, dist, with_keys=[]):
        # (pos, distance, (doors))
        maze = {}
        q = [(start, dist)]

        CONTINUE_SEARCH_LETTERS = set([l for l in LETTERS] + ['.'])
        LOWERCASE_LETTERS = set([l for l in LETTERS])
        UPPERCASE_LETTERS = set([l for l in LETTERS.upper()])

        while q:
            pos, dist = q.pop(0)
            # print(f'Looking at pos: {pos}')
            x, y = pos
            c = self.data[y][x]
            if c == '#':
                continue
            elif c.lower() in CONTINUE_SEARCH_LETTERS:
                # print(c)
                if c in UPPERCASE_LETTERS:
                    if c.lower() in with_keys:
                        pass
                    else:
                        continue

                odist = maze.get(pos, None)
                if odist is None or dist < odist:
                    maze[pos] = dist
                else:
                    # don't continue searching if we went through the same doors and have
                    # a larger distance
                    continue
            else:
                raise Exception('UNEXPECTED LETTER')

            for i in range(4):
                npos = tuple(a+b for a, b in zip(self.moves[i], pos))
                q.append((npos, dist+1))
        return maze

    def valid_paths(self):
        key_list = self.keys.keys()
        
        valid = []
        q = [('origin', [], 0)]
        valid_count = 0
        shortest = 100000000
        invalid = set()
        while q:
            check, prev, dist = q.pop()
            if dist > shortest:
                print(f'Distance {dist} was greater than shortest: {shortest}')
                continue
            elif len(prev) == self.key_count:
                # print(f'Found valid path {"".join(prev)}')
                valid.append(''.join(prev))
                valid_count += 1
                shortest = min((shortest, dist))
                print(shortest)
                if valid_count % 10_000 == 0:
                    print(prev)
                    print(f'Valid Count: {valid_count:,}')
                continue
            else:
                explore_start = self.keys.get(check, self.start)
                maze = self.explore(explore_start, dist, with_keys=prev)
                next_check = (key for key in key_list if key not in prev)
                for key in next_check:
                    if self.keys[key] in maze:
                        if not maze[self.keys[key]] >= shortest:
                            q.append((key, prev + [key], maze[self.keys[key]]))
        return valid


if __name__ == '__main__':
    with open('test.txt', 'r') as f:
        data = [[x for x in line.strip()] for line in f]
        # print(data)

        robit = Robit(data)
        print(f'Keys: {robit.key_count}')
        print(f'Key Locations: {robit.keys}')
        print(robit.current)

        # maze = robit.explore(robit.start, 0, with_keys=['a'])
        # print(maze)
        # robit.explore_from_keys()
        # print('found all paths')
        # for key, value in maze.items():
            # print(key, value)
        # print(robit.keys['b'])

        # print(maze.get(robit.keys['b']))

        valid = robit.valid_paths()
        print(valid)
