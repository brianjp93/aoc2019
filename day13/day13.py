"""day13.py
"""
from computer import Computer
import time


convert = [' ', '|', '█', '-', 'o']

def count_blocks(data):
    return [x for x in data.values()].count(2)

def get_parts(data):
    out = {}
    parts = {}
    for i in range(0, len(data), 3):
        if data[i+2] == 4:
            ball = data[i:i+2]
            out['ball'] = ball
        if data[i+2] == 3:
            paddle = data[i:i+2]
            out['paddle'] = paddle

        parts[tuple(data[i:i+2])] = data[i+2]
    out['parts'] = parts
    return out

def draw(dict_data):
    out = []
    for y in range(25):
        out.append(''.join([convert[dict_data.get((x, y), 0)] for x in range(45)]) + '\n')
    return ''.join(out)

def get_init_blocks(data):
    comp = Computer(data, inputs=[])
    comp.run()
    output = comp.output
    parts = get_parts(output)['parts']
    blocks = count_blocks(parts)
    return blocks

def win_game(data):
    comp = Computer(data, inputs=[])

    blocks = None
    parts = {}
    ball = None
    paddle = None

    while blocks != 0:
        comp.run()
        output = comp.output
        newparts = get_parts(output)
        ball = newparts.get('ball', ball)
        paddle = newparts.get('paddle', paddle)
        # print(f'ball {ball}')
        # print(f'paddle {paddle}')
        parts.update(newparts['parts'])
        blocks = count_blocks(parts)
        comp.output = []

        display = draw(parts)
        score = parts.get((-1, 0), 0)
        display = f'{display}\n\nScore: {score}'
        # print(display)

        if paddle[0] > ball[0]:
            move = -1
        elif ball[0] > paddle[0]:
            move = 1
        else:
            move = 0
        comp.inputs = [move]
        # time.sleep(.05)
    return score


with open('data.txt', 'r') as f:
    data = list(map(int, f.read().split(',')))

    blocks = get_init_blocks(list(data))
    print(f'Init Blocks: {blocks}')

    data[0] = 2
    score = win_game(list(data))
    print(f'End Score: {score}')
