"""day1.py

AOC Day 1

"""


def get_data():
    with open('data.txt', 'r') as f:
        return [int(x) for x in f]


def part1_compute(mass):
    return (mass // 3) - 2


def part2_compute(mass):
    fuel = part1_compute(mass)
    total = 0
    while fuel > 0:
        total += fuel
        fuel = (fuel // 3) - 2
    return total


if __name__ == '__main__':
    data = get_data()
    output_1 = sum(part1_compute(x) for x in data)
    output_2 = sum(part2_compute(x) for x in data)
    print(f'Part 1: {output_1}')
    print(f'Part 2: {output_2}')
