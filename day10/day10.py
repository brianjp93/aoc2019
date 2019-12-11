"""day10.py
"""
from math import atan2, sqrt, pi
from sympy import Rational

def find_slope(start, end):
    num = end[1] - start[1]
    den = end[0] - start[0]
    slope = Rational(num, den) if den != 0 else 'und'
    angle = get_angle(start, end)
    return slope, angle

def get_angle(start, end):
    y = end[1] - start[1]
    x = end[0] - start[0]
    angle = atan2(x, -y)
    if angle < 0:
        angle = (2*pi) + angle
    return angle 

def get_slopes_for(data, coord):
    slopes = {}
    for y in range(len(data)):
        for x in range(len(data[y])):
            if (x, y) != coord and data[y][x] == '#':
                key = find_slope(coord, (x, y))
                dist = get_distance(coord, (x, y))
                slopes[key] = slopes.get(key, [])
                slopes[key].append(((x, y), dist))
    return slopes

def get_distance(start, end):
    x = end[0] - start[0]
    y = end[1] - start[1]
    return sqrt(x**2 + y**2)

def count_all(data):
    counts = {}
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '#':
                slopes = get_slopes_for(data, (x, y))
                counts[(x, y)] = len(slopes.keys())
    return counts

def most_visible_asteroids(data):
    counts = count_all(data)
    best = max(counts, key=lambda x: counts[x])
    return best, counts

def get_vaporization_order(data):
    asteroid_count = sum(line.count('#') for line in data)
    slopes = get_slopes_for(data, best)
    slopes = [(x[1], y) for x, y in slopes.items()]
    slopes.sort(key=lambda x: x[0])

    asteroids = [x[1] for x in slopes]
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
