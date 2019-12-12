"""day12.py
"""
import time
from numpy import lcm

class Moon:
    def __init__(self, x, y, z):
        self.init_pos = [x, y, z]
        self.init_vel = [0, 0, 0]

        self.pos = [x, y, z]
        self.vel = [0, 0, 0]

    def reset(self):
        self.pos = list(self.init_pos)
        self.vel = list(self.init_vel)

    def kinetic_energy(self):
        return sum(abs(x) for x in self.vel)

    def potential_energy(self):
        return sum(abs(x) for x in self.pos)

    def energy(self):
        return self.kinetic_energy() * self.potential_energy()

    def dumps(self):
        return ','.join(map(str, self.pos + self.vel))


class BodySystem:
    def __init__(self, bodies=[]):
        self.bodies = bodies
        self._cycles = None
        self._repeat_step = None

    def _calculate_all_states(self):
        step = 0
        initial_state = self.dumps()

        dimensions = [set() for _ in range(3)]
        cycle = [False for _ in range(3)]
        states = []

        while True:
            if step % 100_000 == 0:
                end = time.time()
                print(f'STEP: {step:10,} in {(end - start):.2f}')

            dim_dump = self.dump_dims()
            for i in range(3):
                if cycle[i]:
                    continue
                else:
                    if dim_dump[i] in dimensions[i]:
                        cycle[i] = step
                    else:
                        dimensions[i].add(dim_dump[i])
                        states.append(self.dump_dims())

            if all(cycle):
                least_common_multiple = lcm.reduce(cycle, dtype='int64')
                break
            self.step()
            step += 1

        self._repeat_step = least_common_multiple
        self._states = states

    def get_repeat_step(self):
        if self._repeat_step is None:
            self._calculate_all_states()
        return self._repeat_step

    def get_cycles(self):
        if self._cycles is None:
            self._calculate_all_states()
        return self._cycles

    def reset(self):
        for body in self.bodies:
            body.reset()

    def step(self):
        for i, body1 in enumerate(self.bodies[:-1]):
            for body2 in self.bodies[i:]:
                for k, (a, b) in enumerate(zip(body1.pos, body2.pos)):
                    if a > b:
                        body1.vel[k] -= 1
                        body2.vel[k] += 1
                    elif a < b:
                        body1.vel[k] += 1
                        body2.vel[k] -= 1
        for body in self.bodies:
            body.pos = [a + b for a, b in zip(body.pos, body.vel)]

    def step_for(self, steps):
        for _ in range(steps):
            self.step()

    def kinetic_energy(self):
        return sum(moon.kinetic_energy() for moon in self.bodies)

    def potential_energy(self):
        return sum(moon.potential_energy() for moon in self.bodies)

    def energy(self):
        return sum(moon.energy() for moon in self.bodies)

    def dumps(self):
        return '|'.join([','.join([str(x) for x in body.pos] + [str(x) for x in body.vel]) for body in self.bodies])

    def dump_x(self):
        return ','.join([(','.join([str(moon.pos[0]), str(moon.vel[0])])) for moon in self.bodies])

    def dump_y(self):
        return ','.join([','.join([str(moon.pos[1]), str(moon.vel[1])]) for moon in self.bodies])

    def dump_z(self):
        return ','.join([','.join([str(moon.pos[2]), str(moon.vel[2])]) for moon in self.bodies])

    def dump_dims(self):
        return self.dump_x(), self.dump_y(), self.dump_z()


def get_dim_cycles(system):
    step = 0
    initial_state = system.dumps()

    dimensions = [set() for _ in range(3)]
    cycle = [False for _ in range(3)]
    states = []

    while True:
        if step % 100_000 == 0:
            end = time.time()
            print(f'STEP: {step:10,} in {(end - start):.2f}')

        dim_dump = system.dump_dims()
        for i in range(3):
            if cycle[i]:
                continue
            else:
                if dim_dump[i] in dimensions[i]:
                    cycle[i] = step
                else:
                    dimensions[i].add(dim_dump[i])
                    states.append(system.dumps())

        if all(cycle):
            least_common_multiple = lcm.reduce(cycle, dtype='int64')
            break
        system.step()
        step += 1
    return least_common_multiple, cycle


with open('data.txt', 'r') as f:
    moons = []
    for line in f:
        obj = line.strip()[1: -1].split(',')
        x, y, z = [int(pos.split('=')[1]) for pos in obj]
        moons.append(Moon(x, y, z))

    start = time.time()

    system = BodySystem(bodies=list(moons))
    steps = 1000
    system.step_for(1000)
    print(f'Energy after {steps} steps: {system.energy()}')

    system.reset()
    repeat_step = system.get_repeat_step()
    print(f'Cycle restarts at step: {repeat_step}')

    end = time.time()
    print(f'Total time: {(end - start):.2f}')
