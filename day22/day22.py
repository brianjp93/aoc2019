"""
"""
import time

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


def find_initial_position(cmds, num_cards, pos, repeats):
    start = time.time()

    for j in range(repeats):
        if j % 100000 == 0:
            print(f'Loop: {j:,}, Time: {(time.time()-start):.2f}')

        old_pos = pos
        for cmd, n in reversed(cmds):
            # print(cmd, n)
            if cmd == 'increment':
                inc = int(n)
                i = 0
                newpos = 1.1
                while int(newpos) != newpos:
                    newpos = (pos + (i*num_cards)) / inc
                    i+=1
                pos = newpos
            elif cmd == 'new':
                # d.reverse()
                pos = num_cards - pos - 1
            elif cmd == 'cut':
                cut = int(n)
                pos = (pos + cut) % num_cards
            else:
                print('invalid command')
    return pos


if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        lines = f.read().split('\n')
        cmds = [line.split()[-2:] for line in lines]

    d = shuffle(list(cmds), 10_007)
    findcard = 2019
    ind = d.deck.index(findcard)
    print(f'Index of {findcard}: {ind}')

    pos_order = find_initial_position(cmds, 119315717514047, 2020, 101741582076661)
    # print(len(pos_order))


    # print(Deck(10))
    # d = shuffle('test.txt', 10)
    # print(d)
    # pos = find_initial_position('test.txt', 10, 6)
    # print(pos)
