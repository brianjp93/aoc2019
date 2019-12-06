"""day5.py
"""
from computer import Computer
Computer(list(map(int, open('data.txt', 'r').read().split(',')))).run()
