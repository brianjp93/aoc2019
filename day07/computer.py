"""computer.py
"""

class Computer:

    def __init__(self, program, inputs=[]):
        self.program = program
        self.i = 0
        self.output = None
        self.inputs = inputs
        self.needs_input = False
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
            99: {
                'run': self.halt, 'step': None
            },
        }

    def run(self):
        # Will run until HALT code or program ends
        self.needs_input = False
        while True:
            out = self.run_op()
            if out == 'HALT':
                return 'HALT'
            elif out == 'AWAIT INPUT':
                break

    def run_op(self):
        opcode = self.get_opcode()
        if opcode == 3:
            if len(self.inputs) == 0:
                self.needs_input = True
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
        modes = str(self.program[self.i])[:-2]
        a, b, c = [int(modes[x]) if len(modes)>=abs(x) else 0 for x in [-3, -2, -1]]
        x, y, z = [self.program[self.i + t] if self.i+t < len(self.program) else None for t in range(1, 4)]
        val1 = [lambda: self.program[x], lambda: x][c]()
        val2 = [lambda: self.program[y], lambda: y][b]()
        return val1, val2, z

    def halt(self):
        # print('HALT')
        return 'HALT'

    def add(self):
        val1, val2, z = self.get_vals()
        self.program[z] = val1 + val2

    def mul(self):
        val1, val2, z = self.get_vals()
        self.program[z] = val1 * val2

    def take_input(self):
        # val = input('Input: ')
        inp = self.inputs.pop(0)
        index = self.program[self.i+1]
        self.program[index] = int(inp)

    def write_output(self):
        index = self.program[self.i+1]
        # print(f'Diagnostic Code: {self.program[index]}')
        self.output = self.program[index]

    def jump_if_true(self):
        val1, val2, z = self.get_vals()
        if val1 != 0:
            self.i = val2
            return False

    def jump_if_false(self):
        val1, val2, z = self.get_vals()
        if val1 == 0:
            self.i = val2
            return False

    def less_than(self):
        val1, val2, z = self.get_vals()
        self.program[z] = int(val1 < val2)

    def equal_to(self):
        val1, val2, z = self.get_vals()
        self.program[z] = int(val1 == val2)
