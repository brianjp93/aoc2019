"""day10.py
"""
from math import atan2, sqrt, pi


def get_angle(start, end):
    y = end[1] - start[1]
    x = end[0] - start[0]
    angle = atan2(x, -y)
    if angle < 0:
        angle = (2*pi) + angle
    return angle 

def get_angles_for(data, coord):
    """

    Returns
    -------
    dict
        key : angles in radians
        value : [((coord -> tuple), manhattan_distance -> int)]
        Ex: {
            angle : [((x, y), manhattan_dist), ...],
            ...
        }

    """
    angles = {}
    for y in range(len(data)):
        for x in range(len(data[y])):
            if (x, y) != coord and data[y][x] == '#':
                key = get_angle(coord, (x, y))
                manhattan_dist = sum(abs((x, y)[a] - coord[a]) for a in [0, 1])
                angles[key] = angles.get(key, [])
                angles[key].append(((x, y), manhattan_dist))
    return angles

def count_all(data):
    counts = {}
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '#':
                angles = get_angles_for(data, (x, y))
                counts[(x, y)] = len(angles.keys())
    return counts

def most_visible_asteroids(data):
    counts = count_all(data)
    best = max(counts, key=lambda x: counts[x])
    return best, counts

def get_vaporization_order(data):
    asteroid_count = sum(line.count('#') for line in data)
    angles = get_angles_for(data, best)
    angles = [(x, y) for x, y in angles.items()]
    angles.sort(key=lambda x: x[0])

    asteroids = [x[1] for x in angles]
    for points in asteroids:
        points.sort(key=lambda x: x[1])

    vaporized = []
    while len(vaporized) < asteroid_count - 1:
        for i, point_list in enumerate(asteroids):
            if len(point_list) == 0:
                continue
            point = point_list.pop(0)
            vaporized.append(point[0])
    return vaporized

if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        data = [line.strip() for line in f]
        
        best, counts = most_visible_asteroids(data)
        print(f'Best Location: {best}')
        print(f'# Asteroids seen: {counts[best]}')

        vaporized = get_vaporization_order(data)
        print(f'200th Vaporized: {vaporized[199]}')
