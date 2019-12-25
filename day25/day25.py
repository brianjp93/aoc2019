"""day25.py
"""
from computer import Computer
from itertools import combinations

CHECKPOINT_ITEMS = ['asterisk','antenna','easter egg','space heater','jam','tambourine','festive hat','fixed point']

class Droid(Computer):
    def __init__(self, *args, **kwargs):
        self.sent = 0
        super().__init__(*args, **kwargs)

    def send(self, command):
        command = command + '\n'
        command = [ord(x) for x in command]
        self.inputs += command
        self.run()
        self.sent += 1
        if self.sent % 50 == 0:
            print(f'Sent {self.sent} commands to droid.')
        return self

    def send_all(self, commands):
        for c in commands:
            self.read()
            self.send(c)

    def take(self, item):
        command = f'take {item}\n'
        self.send(command)

    def drop(self, item):
        command = f'drop {item}\n'
        self.send(command)

    def drop_all(self, items):
        for item in items:
            self.read()
            self.drop(item)
        return self

    def take_all(self, items):
        for item in items:
            self.read()
            self.take(item)
        return self

    def try_all(self):
        print('Trying item combos.')
        tried = 0
        have = []
        for i in range(8):
            combos = combinations(CHECKPOINT_ITEMS, i)
            for combo in combos:
                if tried % 20 == 0:
                    print(f'Tried {tried} item combinations.')
                self.drop_all(set(have) - set(combo))
                self.take_all(set(combo) - set(have)).read()
                have = combo
                out = self.send('west').read()
                tried += 1
                if not 'Alert' in out:
                    return out


if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        data = list(map(int, f.read().split(',')))

    d = Droid(data)
    d.run()
    commands = [
        'south', 'south', 'south',
        'take fixed point', 'south', 'take festive hat',
        'west', 'west', 'take jam',
        'south', 'take easter egg', 'north',
        'east', 'east', 'north',
        'west', 'take asterisk', 'east',
        'north', 'west', 'north',
        'north', 'take tambourine', 'south',
        'south', 'east', 'north',
        'west', 'south', 'take antenna',
        'north', 'west', 'west',
        'take space heater','west',
    ]
    d.send_all(commands)
    out = d.try_all()
    print(out)
