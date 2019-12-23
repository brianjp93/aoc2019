"""computer.py
"""

class Computer:

    def __init__(self, program, inputs=[], slow=False):
        self.program = program + ([0]*10000)
        self.init_program = self.program[:]
        self.i = 0
        self.output = []
        self.inputs = inputs
        self.relative_base = 0
        self.slow = slow
        self.op = {
            1: {
                'run': self.add, 'step': 4
            },
            2: {
                'run': self.mul, 'step': 4
            },
            3: {
                'run': self.take_input, 'step': 2
            },
            4: {
                'run': self.write_output, 'step': 2
            },
            5: {
                'run': self.jump_if_true, 'step': 3
            },
            6: {
                'run': self.jump_if_false, 'step': 3
            },
            7: {
                'run': self.less_than, 'step': 4
            },
            8: {
                'run': self.equal_to, 'step': 4
            },
            9: {
                'run': self.adjust_base, 'step': 2
            },
            99: {
                'run': self.halt, 'step': None
            },
        }

    def reset(self):
        self.program = self.init_program[:]
        self.output = []
        self.inputs = []
        self.i = 0
        self.relative_base = 0

    def read(self):
        output = self.output
        self.output = []
        return output

    def run(self):
        # Will run until HALT code or program ends
        self.needs_input = False
        while True:
            out = self.run_op()
            if out == 'HALT':
                return 'HALT'
            elif out == 'AWAIT INPUT':
                # print('Needs input')
                break

    def run_op(self):
        opcode = self.get_opcode()
        if opcode == 3 and not self.slow:
            if len(self.inputs) == 0:
                return 'AWAIT INPUT'
        do_increment = self.op[opcode]['run']()
        if do_increment is None:
            self.next()
        return do_increment

    def next(self):
        """Increment i by given step for the current opcode.
        """
        opcode = self.get_opcode()
        self.i += self.op[opcode]['step']

    def get_opcode(self):
        instr = str(self.program[self.i])
        opcode = int(instr[-2:])
        return opcode

    def get_vals(self):
        """Get indexes for values.
        0 : position
        1 : immediate
        2 : relative

        """
        modes = str(self.program[self.i])[:-2]
        a, b, c = [int(modes[x]) if len(modes)>=abs(x) else 0 for x in [-3, -2, -1]]
        val1, val2, val3 = [
            [
                self.program[self.i + index],
                self.i + index,
                self.program[self.i + index] + self.relative_base
            ][mode] for index, mode in zip(range(1, 4), [c, b, a])
        ]
        return val1, val2, val3

    def halt(self):
        # print('HALT')
        return 'HALT'

    def add(self):
        x, y, z = self.get_vals()
        self.program[z] = self.program[x] + self.program[y]

    def mul(self):
        x, y, z = self.get_vals()
        self.program[z] = self.program[x] * self.program[y]

    def take_input(self):
        # val = input('Input: ')
        x, y, z = self.get_vals()
        if self.slow:
            inp = input('Input: ')
        else:
            inp = self.inputs.pop(0)
        self.program[x] = int(inp)

    def write_output(self):
        x = self.get_vals()[0]
        self.output.append(self.program[x])
        # print(f'Diagnostic Code: {self.program[x]}')

    def jump_if_true(self):
        x, y, z = self.get_vals()
        if self.program[x] != 0:
            self.i = self.program[y]
            return False

    def jump_if_false(self):
        x, y, z = self.get_vals()
        if self.program[x] == 0:
            self.i = self.program[y]
            return False

    def less_than(self):
        x, y, z = self.get_vals()
        self.program[z] = int(self.program[x] < self.program[y])

    def equal_to(self):
        x, y, z = self.get_vals()
        self.program[z] = int(self.program[x] == self.program[y])

    def adjust_base(self):
        x = self.get_vals()[0]
        adjust = self.program[x]
        self.relative_base += adjust
