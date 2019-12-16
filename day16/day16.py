"""day16.py
"""

class Fft:
    def __init__(self, data):
        self.mult = 20
        self._init_data = data * self.mult
        self.data = data * self.mult
        self.pattern = {}

    def reset(self):
        self.data = list(self._init_data)

    def get_pattern(self, i):
        pattern = self.pattern.get(i, None)
        if pattern is None:
            pattern = [1]*i + [0]*i + [-1]*i + [0]*i
            self.pattern[i] = pattern
        return pattern

    def apply_phase(self):
        out = []
        data_len = len(str(self.data))
        for i in range(data_len):
            pattern = self.get_pattern(i+1)
            pattern_len = len(pattern)
            # nums = [int(self.data[n]) * pattern[(n-i)%pattern_len] for n in range(i, data_len) if pattern[(n-i)%pattern_len] != 0]
            nums = [int(self.data[n]) * pattern[(n-i)%pattern_len] for n in range(data_len)]
            print(''.join([f'{c:2}' for c in nums]))
            # self.print_in_parts(nums)
            num = abs(sum(nums)) % 10
            out.append(str(num))
        self.data = ''.join(out)

    def apply_many_phases(self, i):
        for _ in range(i):
            print(f'Applying phase {_+1}')
            self.apply_phase()

    def print_in_parts(self, data):
        slices = len(data) // self.mult
        out = []
        for j in range(self.mult):
            part = data[slices*j: slices*(j+1)]
            part = [f'{n:2}' for n in part]
            out.append(''.join(part))
        print(' | '.join(out))


with open('test0.txt', 'r') as f:
    data = f.read().strip()

    # print(apply_phase(data, 1))
    message = Fft(data)
    message.apply_many_phases(5)
    print(message.data)