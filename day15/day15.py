"""day15.py
"""
from computer import Computer
import time


class RepairDroid(Computer):
    def __init__(self, *args, **kwargs):
        self.current = (0,0)
        self.moves = ['', (0,1), (0,-1), (-1,0), (1,0)]
        self.opposite_move = {
            1: 2,
            2: 1,
            3: 4,
            4: 3,
        }
        self.map = {}
        self.responses = '# o'
        super().__init__(*args, **kwargs)

    def move(self, i):
        self.inputs = [i]
        self.run()
        response = self.output[-1]
        check_location = tuple(a+b for a, b in zip(self.moves[i], self.current))
        if response == 2:
            self.destination = check_location
        self.map[check_location] = [self.responses[response], None]
        if response in [1, 2]:
            self.current = check_location
        return response

    def draw(self):
        # time.sleep(.01)
        keys = self.map.keys()
        # min_x, max_x, min_y, max_y = -21, 19, -19, 21
        min_x = min(keys, key=lambda x: x[0])[0]
        min_y = min(keys, key=lambda x: x[1])[1]
        max_x = max(keys, key=lambda x: x[0])[0]
        max_y = max(keys, key=lambda x: x[1])[1]

        out = ''
        for y in reversed(range(min_y, max_y+1)):
            out += ''.join([self.map.get((x, y), [' ', ''])[0] if (x,y) != self.current else 'D' for x in range(min_x, max_x+1)]) + '\n'
        return out

    def explore(self, move, draw=False):
        response = self.move(move)
        if draw:
            print(self.draw())
        if response == 0:
            return
        for i in range(1, 5):
            new_move = tuple(a+b for a, b in zip(self.moves[i], self.current))
            if new_move not in self.map:
                self.explore(i, draw=draw)
        if response in [1, 2]:
            self.move(self.opposite_move[move])
            if draw:
                print(self.draw())

    def get_dist(self, coord, dist):
        spot, loc_distance = self.map.get(coord, (None, None))
        if spot in ['#', None]:
            return
        elif (loc_distance is None or dist < loc_distance):
            self.map[coord][1] = dist
            for i in range(1, 5):
                new_move = tuple(a+b for a, b in zip(self.moves[i], coord))
                self.get_dist(new_move, dist+1)



if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        data = list(map(int, f.read().split(',')))
        
        droid = RepairDroid(data)
        droid.explore(2, draw=False)
        # print(droid.draw())
        droid.get_dist((0, 0), 0)
        print(f'Distance to destination: {droid.map[droid.destination]}')

        droid.get_dist(droid.destination, 0)
        vals = [x[1] for x in droid.map.values() if x[1] is not None]
        print(f'Distance to furthest part of room: {max(vals)}')
