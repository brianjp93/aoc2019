data = [int(x) for x in open('data.txt', 'r').readlines()]
compute1 = lambda n: n//3 - 2
part1 = sum(compute1(x) for x in data)

print(f'Part 1: {part1}')