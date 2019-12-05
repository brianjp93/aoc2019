
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
            coord = (coord[0] + move[0], coord[1] + move[1])
            complete_path.add(coord)
    return complete_path


def get_intersections(wire1, wire2):
    return wire1.intersection(wire2)


if __name__ == '__main__':
    wire1, wire2 = get_data('data.txt')
    wire1_set, wire2_set = get_point_set(wire1), get_point_set(wire2)
    intersections = get_intersections(wire1_set, wire2_set)
    print(intersections)
    print(f'# intersections: {len(intersections)}')