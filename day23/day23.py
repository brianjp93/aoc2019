"""day23.py

Not too hard, but I wasn't a big fan of this one because I
found it hard to figure out when I was supposed to be checking
if the system was idle.

"""
from computer import Computer


if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        data = list(map(int, [x for x in f.read().split(',')]))
    comps = [Computer(list(data), inputs=[i, -1]) for i in range(50)]
    nat = [None, None]
    last_y = None
    first = True

    while True:
        for comp in comps:
            comp.inputs = [-1] if len(comp.inputs) == 0 else comp.inputs
            comp.run()
            output = comp.read()
            if output:
                for j in range(0, len(output), 3):
                    i, x, y = output[j:j+3]

                    if int(i) == 255:
                        nat = [x, y]
                        if first:
                            first = False
                            print(f'First y value sent to 255: {y}')
                    else:
                        comps[i].inputs += [x, y]

            if all(len(comp.inputs) == 0 for comp in comps):
                y = nat[1]
                if y == last_y:
                    print(f'{y} was just sent!')
                    exit()
                comps[0].inputs += list(nat)
                last_y = y


