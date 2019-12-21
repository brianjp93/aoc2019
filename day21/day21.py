"""day21.py
"""
from computer import Computer


with open('data.txt', 'r') as f:
    data = list(map(int, f.read().split(',')))
    comp = Computer(data)

    comp.run()
    print(''.join([chr(x) for x in comp.output]))
    comp.output = []
    instr = [

        # ##.#
        'NOT C T',
        'AND A T',
        'AND D T',
        'OR T J',

        # must jump if the tile in front of us is empty
        # .###
        'NOT A T',
        'OR T J',

        'WALK',
    ]

    instr = '\n'.join(instr) + '\n'
    instr = [ord(x) for x in instr]
    comp.inputs = instr
    comp.run()
    # print(comp.output)
    out = ''.join([chr(x) for x in comp.output if x < 128])
    print(out)
    print(comp.output[-1])


    instr = [
        # ##.#
        'NOT C T',
        'AND A T',
        'AND D T',
        'AND H T',
        'OR T J',

        'NOT B T',
        'AND D T',
        'AND H T',
        'OR T J',

        # must jump if the tile in front of us is empty
        # .###
        'NOT A T',
        'OR T J',

        'RUN',
    ]

    comp.reset()
    instr = '\n'.join(instr) + '\n'
    instr = [ord(x) for x in instr]
    comp.inputs = instr
    comp.run()
    # print(comp.output)
    out = ''.join([chr(x) for x in comp.output if x < 128])
    print(out)
    print(comp.output[-1])