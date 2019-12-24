"""day22.py

This problem was really tough and I looked at other solutions before completing this.
I need to look at it more to really understand what's happening.

"""
import time
from sympy import Symbol, simplify, mod_inverse

class Deck:
    def __init__(self, n):
        self.deck = [i for i in range(n)]

    def __repr__(self):
        return f'{self.deck}'

    def reverse(self):
        self.deck.reverse()
        return self

    def cut(self, n):
        l1 = self.deck[:n]
        l2 = self.deck[n:]
        self.deck = l2 + l1
        return self

    def deal_with_inc(self, n):
        nd = [0] * len(self.deck)
        count = 0
        index = 0
        while count != len(self.deck):
            modindex = index % len(self.deck)
            nd[modindex] = self.deck[count]
            index += n
            count += 1
        self.deck = nd
        return self

def shuffle(cmds, num_cards, repeat=1):
    d = Deck(num_cards)

    for _ in range(repeat):
        for cmd, n in cmds:
            if cmd == 'increment':
                d.deal_with_inc(int(n))
            elif cmd == 'new':
                d.reverse()
            elif cmd == 'cut':
                d.cut(int(n))
    return d

def find_initial_position(cmds, card_count, pos, shuffle_count):
    inc = 1
    offset = 0
    for cmd, n in cmds:
        if cmd == 'increment':
            # deal
            inc *= mod_inverse(int(n), card_count)
        elif cmd == 'new':
            # reverse
            inc *= -1
            offset += inc
        elif cmd == 'cut':
            # cut
            cut = int(n)
            offset += cut * inc
        else:
            raise Exception('Invalid Command')

        inc = inc % card_count
        offset = offset % card_count

    offset *= mod_inverse(1 - inc, card_count)
    inc = pow(inc, shuffle_count, card_count)
    return ((pos - offset) * inc + offset) % card_count


if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        lines = f.read().split('\n')
        cmds = [line.split()[-2:] for line in lines]

    # d = shuffle(list(cmds), 10_007, 1)
    # findcard = 2019
    # ind = d.deck.index(findcard)
    # print(f'Index of {findcard}: {ind}')

    pos = find_initial_position(cmds, 10007, 2019, -1)
    print(pos)

    n = 119315717514047
    r = 101741582076661
    pos = find_initial_position(cmds, n, 2020, r)
    print(pos)
