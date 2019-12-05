"""day2.py
"""

def lget(l, index, default=0):
    try:
        return l[index]
    except IndexError:
        return default

def run_1202(data):
    d = list(data)
    i = 0
    opcode = None
    last_diagnostics_code = None
    while opcode != 99:
        instr = str(d[i])
        modes, opcode = instr[:-2], int(instr[-2:])
        a, b, c = [int(lget(modes, x)) for x in [-3, -2, -1]]
        if opcode == 1:
            x, y, pos = d[i+1: i+4]
            val1 = (lambda: d[x], lambda: x)[c]()
            val2 = (lambda: d[y], lambda: y)[b]()
            d[pos] = val1 + val2
            i += 4
        elif opcode == 2:
            x, y, pos = d[i+1: i+4]
            val1 = (lambda: d[x], lambda: x)[c]()
            val2 = (lambda: d[y], lambda: y)[b]()
            d[pos] = val1 * val2
            i += 4
        elif opcode == 3:
            val = int(input('Input Val: '))
            index = d[i+1]
            d[index] = val
            i += 2
        elif opcode == 4:
            index = d[i+1]
            last_diagnostics_code = d[index]
            print(last_diagnostics_code)
            i += 2
        elif opcode == 5:
            x, y = d[i+1: i+3]
            val1 = (lambda: d[x], lambda: x)[c]()
            val2 = (lambda: d[y], lambda: y)[b]()
            if val1 != 0:
                i = val2
            else:
                i += 3
        elif opcode == 6:
            x, y = d[i+1: i+3]
            val1 = (lambda: d[x], lambda: x)[c]()
            val2 = (lambda: d[y], lambda: y)[b]()
            if val1 == 0:
                i = val2
            else:
                i += 3
        elif opcode == 7:
            x, y, z = d[i+1: i+4]
            val1 = (lambda: d[x], lambda: x)[c]()
            val2 = (lambda: d[y], lambda: y)[b]()
            d[z] = int(val1 < val2)
            i += 4
        elif opcode == 8:
            x, y, z = d[i+1: i+4]
            val1 = (lambda: d[x], lambda: x)[c]()
            val2 = (lambda: d[y], lambda: y)[b]()
            d[z] = int(val1 == val2)
            i += 4
        elif opcode == 99:
            print('HALT')
            break
        else:
            print(d)
            raise Exception(f'Invalid OPCODE {opcode} at instruction={i}.')
    return d

if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        data = [int(x) for x in f.read().split(',')]
        p1_data = list(data)
        part1 = run_1202(p1_data)
