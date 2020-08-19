"""day8.py
https://adventofcode.com/2019/day/8
"""
import pathlib

cwd = pathlib.Path(__file__).parent.absolute()
dpath = pathlib.PurePath(cwd, 'data.txt')

def get_layers(data, width, height):
    y = 0
    while True:
        layer = []
        for _ in range(height):
            row = data[width * y: (width * y) + width]
            layer.append(row)
            y += 1
        if ''.join(layer) == '':
            break
        yield layer


def decode(layers):
    layer = layers[0]
    decoded = []
    for i in range(len(layer)):
        decoded_row = []
        for j in range(len(layer[0])):
            c = get_non_2(layers, i, j)
            decoded_row.append(c)
        decoded.append(''.join(decoded_row))
    return decoded


def get_non_2(layers, row, index):
    for layer in layers:
        c = layer[row][index]
        if c != '2':
            return c


def display(image):
    for row in image:
        row = row.replace('0', '.').replace('2', '#').replace('1', '#')
        print(row)


if __name__ == '__main__':
    with open(dpath, 'r') as f:
        data = f.read()

        layers = list(get_layers(data, 25, 6))
        flat = ''.join(min(layers, key=lambda x: ''.join(x).count('0')))
        print(f'Part 1: {flat.count("1") * flat.count("2")}')

        image = decode(layers)
        display(image)
