"""day6.py

https://adventofcode.com/2019/day/6

"""

class Universe:
    def __init__(self, fname):
        self.orbits = self.compile_orbits(fname)

    def compile_orbits(self, fname):
        orbits = {}
        with open(fname, 'r') as f:
            for line in f:
                m1, m2 = line.strip().split(')')
                o = orbits.get(m1, {'(': None, ')': [], 'd': None})
                o[')'].append(m2)
                orbits[m1] = o
                o = orbits.get(m2, {'(': None, ')': [], 'd': None})
                o['('] = m1
                orbits[m2] = o
        orbits['COM']['d'] = 0
        return orbits

    def find_distance(self, start='COM'):
        o = self.orbits[start]
        for mass in o[')']:
            prev_mass = self.orbits[mass]['(']
            self.orbits[mass]['d'] = 1 + self.orbits[prev_mass]['d']
            self.find_distance(start=mass)

    def count_total_orbits(self):
        return sum(x['d'] for x in self.orbits.values())

    def path_to_com(self, start):
        path = []
        while start != 'COM':
            path.append(start)
            start = self.orbits[start]['(']
        path.append('COM')
        return path

    def find_dist_between(self, m1, m2):
        p1, p2 = list(reversed(self.path_to_com(m1))), list(reversed(self.path_to_com(m2)))
        for i, (a, b) in enumerate(zip(p1, p2)):
            if a != b:
                return len(p1[i+1:]) + len(p2[i+1:])


if __name__ == '__main__':
    universe = Universe('data.txt')
    universe.find_distance()
    print(universe.count_total_orbits())
    print(universe.find_dist_between('YOU', 'SAN'))
