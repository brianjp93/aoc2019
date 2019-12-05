"""computer.py
"""

class Computer:

    def __init__(self, program):
        self.program = program
        self.i = 0
        self.op = {
            1: {
                'run': self.add,
                'step': 4
            },
            2: {
                'run': self.mul,
                'step': 4
            },
            3: {
                'run': self.take_input,
                'step': 2
            },
            4: {
                'run': self.write_output,
                'step': 2
            },
            5: {
                'run': self.jump_if_true,
                'step': 3
            },
            6: {
                'run': self.jump_if_false,
                'step': 3
            },
            7: {
                'run': self.less_than,
                'step': 4
            },
            8: {
                'run': self.equal_to,
                'step': 4
            },
            99: {
                'run': self.halt,
                'step': None
            },
        }

    def run(self):
        # Will run until HALT code or program ends
        while True:
            self.run_op()

    def run_op(self):
        opcode = self.get_opcode()
        do_increment = self.op[opcode]['run']()
        if do_increment:
            self.next()

    def next(self):
        """Increment i by given step for the current opcode.
        """
        opcode = self.get_opcode()
        self.i += self.op[opcode]['step']

    def get_opcode(self):
        instr = str(self.program[self.i])
        opcode = int(instr[-2:])
        return opcode

    def get_modes(self):
        instr = str(self.program[self.i])
        modes = instr[:-2]
        return [int(modes[x]) if len(modes)>=abs(x) else 0 for x in [-3, -2, -1]]

    def halt(self):
        print('HALT')
        exit()

    def add(self):
        a, b, c = self.get_modes()
        x, y, pos = self.program[self.i+1: self.i+4]
        val1 = [lambda: self.program[x], lambda: x][c]()
        val2 = [lambda: self.program[y], lambda: y][b]()
        self.program[pos] = val1 + val2
        return True

    def mul(self):
        a, b, c = self.get_modes()
        x, y, pos = self.program[self.i+1: self.i+4]
        val1 = [lambda: self.program[x], lambda: x][c]()
        val2 = [lambda: self.program[y], lambda: y][b]()
        self.program[pos] = val1 * val2
        return True

    def take_input(self):
        val = input('Input: ')
        index = self.program[self.i+1]
        self.program[index] = int(val)
        return True

    def write_output(self):
        index = self.program[self.i+1]
        print(f'Diagnostic Code: {self.program[index]}')
        return True

    def jump_if_true(self):
        x, y = self.program[self.i+1: self.i+3]
        a, b, c = self.get_modes()
        val1 = [lambda: self.program[x], lambda: x][c]()
        val2 = [lambda: self.program[y], lambda: y][b]()
        if val1 != 0:
            self.i = val2
            return False
        else:
            return True

    def jump_if_false(self):
        x, y = self.program[self.i+1: self.i+3]
        a, b, c = self.get_modes()
        val1 = [lambda: self.program[x], lambda: x][c]()
        val2 = [lambda: self.program[y], lambda: y][b]()
        if val1 == 0:
            self.i = val2
            return False
        else:
            return True

    def less_than(self):
        x, y, z = self.program[self.i+1: self.i+4]
        a, b, c = self.get_modes()
        val1 = [lambda: self.program[x], lambda: x][c]()
        val2 = [lambda: self.program[y], lambda: y][b]()
        self.program[z] = int(val1 < val2)
        return True

    def equal_to(self):
        x, y, z = self.program[self.i+1: self.i+4]
        a, b, c = self.get_modes()
        val1 = [lambda: self.program[x], lambda: x][c]()
        val2 = [lambda: self.program[y], lambda: y][b]()
        self.program[z] = int(val1 == val2)
        return True


if __name__ == '__main__':
    with open('test.txt', 'r') as f:
        data = list(map(int, f.read().split(',')))
        print(data)
        comp = Computer(data)
        comp.run()
