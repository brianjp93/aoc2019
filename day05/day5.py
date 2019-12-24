"""day5.py

https://adventofcode.com/2019/day/5

"""
from computer import Computer
Computer(list(map(int, open('data.txt', 'r').read().split(',')))).run()
