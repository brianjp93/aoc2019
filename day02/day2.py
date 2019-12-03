"""day2.py
"""

def run_1202(data):
    d = list(data)
    i = 0
    opcode = d[i]
    while opcode != 99:
        opcode = d[i]
        x, y, pos = d[i+1: i+4]
        if opcode == 1:
            d[pos] = d[x] + d[y]
        elif opcode == 2:
            d[pos] = d[x] * d[y]
        i += 4
    return d

def find_inputs(data, value):
    for i in range(100):
        for j in range(100):
            d = list(data)
            d[1] = i
            d[2] = j
            output = run_1202(d)
            if output[0] == value:
                return [i, j]


if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        data = [int(x) for x in f.read().split(',')]
        p1_data = list(data)
        p1_data[1] = 12
        p1_data[2] = 2
        part1 = run_1202(p1_data)
        print(f'Part 1: {part1[0]}')
        part2 = find_inputs(data, 19690720)
        print(f'Part 2: {100 * part2[0] + part2[1]}')
