"""day16.py
"""

class Fft:
    def __init__(self, data, mult=1):
        self.mult = mult
        self._init_data = data * self.mult
        self.data = data * self.mult
        self.data_len = len(self.data)
        self.mindex = int(''.join(map(str, self.data[:7])))
        self.pattern = {}

    def reset(self):
        self.data = list(self._init_data)

    def get_pattern(self, i):
        pattern = self.pattern.get(i, None)
        if pattern is None:
            pattern = [0]*i + [1]*i + [0]*i + [-1]*i
            self.pattern[i] = pattern
        return pattern

    def apply_phase(self):
        out = []
        for i in range(self.data_len//2+1):
            pattern = self.get_pattern(i+1)
            pattern_len = (i+1) * 4
            out.append(
                abs(
                    sum(
                        self.data[n] * pattern[(n+1) % pattern_len]
                        for n in range(i, self.data_len)
                    )
                ) % 10
            )
        for n in self.data[self.data_len//2:-1]:
            last_num = (out[-1] - n) % 10
            out.append(last_num)
        self.data = out

    def apply_many_phases(self, i):
        for _ in range(i):
            self.apply_phase()

    def apply_at_index(self, loops):
        data = self.data[self.mindex:]
        for i in range(loops):
            new_data = [sum(data) % 10]
            for n in data[:-1]:
                new_data.append((new_data[-1] - n) % 10)
            data = new_data
        return ''.join(map(str, data[:8]))

    def print_in_parts(self, data):
        slices = len(data) // self.mult
        out = []
        for j in range(self.mult):
            part = data[slices*j: slices*(j+1)]
            part = [f'{n:1}' for n in part]
            out.append(''.join(part))
        print(' | '.join(out))


with open('data.txt', 'r') as f:
    data = f.read().strip()
    data = [int(x) for x in data]

    message = Fft(data, mult=1)
    message.apply_many_phases(100)
    m = ''.join(map(str, message.data[:8]))
    print(f'Part 1: {m}')

    message = Fft(data, mult=10_000)
    m = message.apply_at_index(100)
    print(f'Part 2: {m}')
