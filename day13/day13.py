"""day13.py
"""
from computer import Computer
import time


convert = [' ', '|', '█', '-', 'o']

def count_blocks(data):
    return [x for x in parts.values()].count(2)

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


with open('data.txt', 'r') as f:
    data = list(map(int, f.read().split(',')))
    data[0] = 2
    comp = Computer(data, inputs=[])

    blocks = None
    parts = {}
    ball = None
    paddle = None

    loop = 0
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
        if loop == 0:
            print(f'Blocks Init: {blocks}.')
        comp.output = []

        # print(draw(parts))
        score = parts.get((-1, 0), 0)

        if paddle[0] > ball[0]:
            move = -1
        elif ball[0] > paddle[0]:
            move = 1
        else:
            move = 0
        comp.inputs = [move]
        loop += 1
    
    print(f'Score: {score}')
