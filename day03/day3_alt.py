"""
"""
shortest_manhattan = lambda points: min(points, key=lambda x: abs(x[0]) + abs(x[1]))
get_intersections = lambda x, y: x.intersection(y)

def get_data(fname):
    with open(fname, 'r') as f:
        return [l.split(',') for l in f]


def get_point_set(instructions):
    options = {
        'U': (0, 1),
        'R': (1, 0),
        'L': (-1, 0),
        'D': (0, -1),
    }
    coord = (0, 0)
    complete_path = set([coord])
    for instr in instructions:
        move, distance = options[instr[0]], int(instr[1:])
        for i in range(distance):
            coord = tuple([a + b for a, b in zip(coord, move)])
            complete_path.add(coord)
    return complete_path


if __name__ == '__main__':
    wire1, wire2 = get_data('data.txt')
    wire1_set, wire2_set = get_point_set(wire1), get_point_set(wire2)
    intersections = get_intersections(wire1_set, wire2_set)
    intersections.remove((0, 0))
    # print(intersections)
    print(f'# intersections: {len(intersections)}')
    closest_point = shortest_manhattan(intersections)
    print(f'Shortest Manhattan: {abs(closest_point[0]) + abs(closest_point[1])}')
