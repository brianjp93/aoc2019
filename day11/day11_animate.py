"""day11_animate.py
"""
from day11 import HullPaintingRobot
from computer import Computer
import time

def run_robot(data, start_input, draw_step=True):
    robot = HullPaintingRobot()
    comp = Computer(list(data), inputs=[start_input])
    output = None
    last_index = 0
    while True:
        output = comp.run()
        new_outputs = comp.output[last_index:]
        last_index = len(comp.output)
        robot.command(new_outputs[0], new_outputs[1])
        if draw_step:
            out = robot.draw(with_ant=True, x_range=(0, 42), y_range=(-5, 0))
            print(out)
            time.sleep(.1)
        if output == 'HALT':
            break
        comp.inputs.append(robot.current_color())

    return robot


if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        data = list(map(int, f.read().split(',')))
        robot = run_robot(data, 1)
