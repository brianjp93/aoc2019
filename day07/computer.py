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


def get_highest_signals(data):
    """
    """
    max_val = 0
    max_input = None
    for n1 in range(5):
        for n2 in range(5):
            for n3 in range(5):
                for n4 in range(5):
                    for n5 in range(5):
                        signal = f'{n1}{n2}{n3}{n4}{n5}'
                        if is_allowed(signal):
                            output = run_with_signal(data, signal)
                            if output > max_val:
                                max_val = output
                                max_input = signal
    return (max_input, max_val)


def get_highest_signals_2(data):
    """
    """
    max_val = 0
    max_input = None
    for n1 in range(5, 10):
        for n2 in range(5, 10):
            for n3 in range(5, 10):
                for n4 in range(5, 10):
                    for n5 in range(5, 10):
                        signal = f'{n1}{n2}{n3}{n4}{n5}'
                        if is_allowed(signal):
                            # print(signal)
                            output = run_with_signal_2(data, signal)
                            if output > max_val:
                                max_val = output
                                max_input = signal
    return (max_input, max_val)


def is_allowed(signal):
    for c in signal:
        if signal.count(c) > 1:
            return False
    return True


def run_with_signal(data, signal):
    a = Computer(list(data), inputs=[int(signal[0]), 0])
    a.run()
    b = Computer(list(data), inputs=[int(signal[1]), a.output])
    b.run()
    c = Computer(list(data), inputs=[int(signal[2]), b.output])
    c.run()
    d = Computer(list(data), inputs=[int(signal[3]), c.output])
    d.run()
    e = Computer(list(data), inputs=[int(signal[4]), d.output])
    e.run()
    return e.output


def run_with_signal_2(data, signal):
    e_outputs = []
    a = Computer(list(data), inputs=[signal[0]])
    b = Computer(list(data), inputs=[signal[1]])
    c = Computer(list(data), inputs=[signal[2]])
    d = Computer(list(data), inputs=[signal[3]])
    e = Computer(list(data), inputs=[signal[4]])
    run_return = []
    first_run = True
    while run_return.count('HALT') != 5:
    # for i in range(10):
        if first_run:
            first_run = False
            a_input = 0
        else:
            a_input = e.output
        
        a.inputs.append(a_input)
        a_out = a.run()
        b.inputs.append(a.output)
        b_out = b.run()
        c.inputs.append(b.output)
        c_out = c.run()
        d.inputs.append(c.output)
        d_out = d.run()
        e.inputs.append(d.output)
        e_out = e.run()
        e_outputs.append(e.output)
        run_return = [a_out, b_out, c_out, d_out, e_out]
    # print(e_outputs)
    # print(f'finished in {i} loops')
    return e.output


if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        data = list(map(int, f.read().split(',')))

        out = get_highest_signals(data)
        print(out)

        out = get_highest_signals_2(data)
        print(out)

