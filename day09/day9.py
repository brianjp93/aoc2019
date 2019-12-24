"""day9.py

https://adventofcode.com/2019/day/9

"""
from computer import Computer

with open('data.txt', 'r') as f:
    data = list(map(int, f.read().split(',')))
    # part 1
    comp = Computer(list(data), inputs=[1])
    comp.run()
    # part 2
    comp = Computer(list(data), inputs=[2])
    comp.run()
