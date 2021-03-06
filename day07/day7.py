"""day7.py

https://adventofcode.com/2019/day/7

"""
from computer import Computer
from itertools import permutations
import pathlib

cwd = pathlib.Path(__file__).parent.absolute()
dpath = pathlib.PurePath(cwd, 'data.txt')


def get_highest_signals(data, allowed, run_once=True):
    max_val = (0, 0)
    max_input = None
    for signal in (''.join(p) for p in permutations(allowed)):
        output = run_with_signal(data, signal, run_once=run_once)
        max_val = max([max_val, (signal, output)], key=lambda x: x[1])
    return max_val

def run_with_signal(data, signal, run_once=True):
    e_outputs = []
    server = [Computer(list(data), inputs=[signal[x]]) for x in range(5)]
    first_run = True
    run_return = []
    while run_return.count('HALT') != 5:
        run_return = []
        for i, comp in enumerate(server):
            comp.inputs.append(server[i-1].output if not first_run or i!=0 else 0)
            run_return.append(comp.run())
        if first_run:
            first_run = False
            if run_once:
                break
    return server[-1].output

if __name__ == '__main__':
    with open(dpath, 'r') as f:
        data = list(map(int, f.read().split(',')))

        out = get_highest_signals(data, '01234', run_once=True)
        print(out)

        out = get_highest_signals(data, '56789', run_once=False)
        print(out)
