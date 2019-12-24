"""day18.py

not clever enough
This is doing many searches and it is too slow.
When there are 26 keys, we have maybe 26 factorial
path options.

"""
import time
import networkx as nx
import matplotlib.pyplot as plt

LETTERS = 'abcdefghijklmnopqrstuvwxyz'


class Node:
    def __init__(self, name):
        self.name = name
        self.connected = {}
        self.lt_set = set()
        self.gt_set = set()

    def __repr__(self):
        return f'{self.name}'

    def __getitem__(self, node):
        return self.connected[node][1]

    def __iter__(self):
        for item in self.connected.values():
            yield item

    def __lt__(self, node):
        tocheck = [node]
        while tocheck:
            lt_node = tocheck.pop()
            if self in lt_node.lt_set:
                return True
            else:
                tocheck += [x for x in lt_node.lt_set]
        return False

    def sorted(self):
        return sorted([n for n in self.connected.values()], key=lambda x: x[1])

    def connect(self, node, distance):
        self.connected[node.name] = (node, distance)
        node.connected[self.name] = (self, distance)

    def remove(self, node):
        if node.name in self.connected:
            del self.connected[node.name]
        if self.name in node.connected:
            del node.connected[self.name]

    def force_lt(self, node):
        self.lt_set.add(node)
        node.gt_set.add(self)

    def force_gt(self, node):
        pass

class Robit:
    def __init__(self, data):
        self.data = data
        self.start = self.get_start()
        self.keys = {}
        self.key_count = self.count_keys()
        self.current = self.start
        self.moves = (
            (1, 0),
            (0, -1),
            (-1, 0),
            (0, 1)
        )
        self.maze = {}
        self.nodes = {}
        self.distance_to_keys = {} 
        self.conditions = None

    def get_start(self):
        for y, line in enumerate(self.data):
            for x, ch in enumerate(line):
                if ch == '@':
                    self.data[y][x] = '.'
                    return (x, y)

    def count_keys(self):
        count = 0
        for y,line in enumerate(self.data):
            for x, ch in enumerate(line):
                if ch in LETTERS:
                    self.keys[ch] = x,y
                    count += 1
        return count

    def explore(self, start, dist, with_keys=[]):
        # (pos, distance, (doors))
        maze = {}
        q = [(start, dist)]

        CONTINUE_SEARCH_LETTERS = set([l for l in LETTERS] + ['.'])
        LOWERCASE_LETTERS = set([l for l in LETTERS])
        UPPERCASE_LETTERS = set([l for l in LETTERS.upper()])

        while q:
            pos, dist = q.pop(0)
            # print(f'Looking at pos: {pos}')
            x, y = pos
            c = self.data[y][x]
            if c == '#':
                continue
            elif c.lower() in CONTINUE_SEARCH_LETTERS:
                # print(c)
                if c in UPPERCASE_LETTERS:
                    if c.lower() in with_keys:
                        pass
                    else:
                        continue

                odist = maze.get(pos, None)
                if odist is None or dist < odist:
                    maze[pos] = dist
                else:
                    # don't continue searching if we went through the same doors and have
                    # a larger distance
                    continue
            else:
                raise Exception('UNEXPECTED LETTER')

            for i in range(4):
                npos = tuple(a+b for a, b in zip(self.moves[i], pos))
                q.append((npos, dist+1))
        return maze

    def get_nodes(self):
        """get all distances between origin and every key.

        Assume we have every key

        """
        if self.nodes:
            return self.nodes
        keys = self.keys.keys()

        self.nodes['@'] = Node('@')
        for key in keys:
            self.nodes[key] = Node(key)

        maze = self.explore(self.start, 0, with_keys=keys)
        for c, pos in self.keys.items():
            self.nodes['@'].connect(self.nodes[c], maze[pos])

        for key, key_pos in self.keys.items():
            maze = self.explore(key_pos, 0, with_keys=keys)
            for otherkey, pos in self.keys.items():
                if key != otherkey:
                    self.nodes[key].connect(self.nodes[otherkey], maze[pos])

    def get_graph(self):
        keys = self.keys.keys()
        graph = nx.Graph()

        graph.add_nodes_from(keys)

        maze = self.explore(self.start, 0, with_keys=keys)
        for c, pos in self.keys.items():
            dist = maze[pos]
            graph.add_edge('@', c, weight=dist)

        for i, (key, key_pos) in enumerate(list(self.keys.items())[:-1]):
            maze = self.explore(key_pos, 0, with_keys=keys)
            for otherkey, pos in list(self.keys.items())[i+1:]:
                if key != otherkey:
                    dist = maze[pos]
                    graph.add_edge(key, otherkey, weight=dist)

        self.graph = graph

    def draw_graph(self):
        self.get_graph()
        nx.draw_shell(self.graph, with_labels=True, font_weight='bold')
        plt.show()

    def get_path(self, key, maze=None, start=None):
        start = start if start else self.start
        if maze is None:
            maze = self.explore(start, 0, with_keys=self.keys.keys())
        end = self.keys[key]
        path = [end]
        doors = []
        through_keys = []

        pos = end
        dist = maze[pos]
        while pos != start:
            for i in range(4):
                newpos = tuple(a+b for a, b in zip(self.moves[i], pos))
                if maze.get(newpos, None) == dist-1:
                    pos = newpos
                    dist = maze[newpos]
                    path.append(pos)
                    c = self.data[pos[1]][pos[0]]
                    if c in LETTERS.upper():
                        doors.append(c)
                    elif c in LETTERS.lower():
                        if c != key:
                            through_keys.append(c)
                    break
        path, doors, through_keys = list(reversed(path)), list(reversed(doors)), list(reversed(through_keys))
        return path, doors, through_keys

    def draw_path(self, path):
        """
        """
        have_keys = []
        paths = set()
        total = 0
        for a,b in zip(path, path[1:]):
            # print(f'getting path between {a} and {b}')
            if a == '@':
                path, doors, _ = self.get_path(b, start=None)
            else:
                path, doors, _ = self.get_path(b, start=self.keys[a])
            total += len(path)
            for door in doors:
                if not door.lower() in have_keys:
                    print('INVALID PATH')
                    print(f'Cannot go through {door} yet.')
            have_keys.append(b)
            paths = paths | set(path)

        convert = {
            '.': ' ',
            '#': '■'
        }
        out = []
        # print(paths)
        for y, line in enumerate(self.data):
            l = []
            for x, c in enumerate(line):
                if c in LETTERS:
                    pass
                else:
                    c = convert.get(c, c)
                    if (x, y) in paths:
                        c = '*'
                l.append(c)
            out.append(''.join(l))
        out = '\n'.join(out)
        print(out)
        print(total)
        return out

    def get_conditions(self):
        maze = self.explore(self.start, 0, with_keys=self.keys.keys())

        explicit = []
        equalities = []
        for key, pos in self.keys.items():
            path, doors, through_keys = self.get_path(key)
            for kbefore in through_keys:
                explicit.append(kbefore)
                explicit.append(key)
                equalities.append([[kbefore], [key]])
            for door in doors:
                c = door.lower()
                # print(f'{c} before {key}')
                self.nodes[key].force_lt(self.nodes[c])
                explicit.append(c)
                explicit.append(key)

                found = False
                equalities.append([[c], [key]])

        nodes = [n for n in self.nodes.values() if n.name in explicit]
        nodes.sort()
        top = self.nodes['@']
        # groups = [[nodes[0].name]]
        # for n1, n2 in zip(nodes, nodes[1:]):
        #     print(n1 < n2)
        #     if (n1 < n2):
        #         groups.append([n2.name])
        #     else:
        #         groups[-1].append(n2.name)
        # any_order = [n for n in self.keys.keys() if n not in explicit]

        # print(equalities)
        # print(groups)
        # print(any_order)

        # print(top['g'] < top['b'])
        # print(top['b'] < top['g'])
        # print(top['c'] < top['b'])
        # return groups, any_order
        self.conditions = equalities
        return equalities

    def find_shortest(self, key='@', keys_needed=None, p='', not_allowed=None):
        """
        """
        # print(f'Checking key {key} and keys_needed {keys_needed}')
        if not self.nodes:
            self.get_nodes()
        if keys_needed is None:
            keys_needed = set(self.keys.keys())
        if not keys_needed:
            return 0, key

        dictkey = (key, tuple(sorted(list(keys_needed))))
        cached = self.distance_to_keys.get(dictkey, None)
        if cached:
            return cached

        # get condition
        if not self.conditions:
            self.get_conditions()

        if not_allowed is None:
            not_allowed = {x[1][0] for x in self.conditions if x[0][0] in keys_needed}

        # print(not_allowed)

        out = 10000000
        new_path = None
        for next_key in keys_needed:
            if next_key not in not_allowed:
                nshort = self.find_shortest(key=next_key, keys_needed=keys_needed - set(next_key), p=next_key)
                d = self.nodes[key][next_key] + nshort[0]
                if d < out:
                    out = d
                    new_path = p + nshort[1]
                    # print(f'found shorter path with key {key} and next {next_key}')
                else:
                    pass

        self.distance_to_keys[dictkey] = (out, new_path)
        return out, new_path


    def find_shortest_no_doors(self, key='@', keys_needed=None, p=''):
        """
        """
        # print(f'Checking key {key} and keys_needed {keys_needed}')
        if keys_needed is None:
            keys_needed = set(self.keys.keys())
        if not keys_needed:
            return 0, key

        dictkey = (key, tuple(sorted(list(keys_needed))))
        cached = self.distance_to_keys.get(dictkey, None)
        if cached:
            return cached

        # print(not_allowed)

        out = 10000000
        new_path = None
        for next_key in keys_needed:
            nshort = self.find_shortest(key=next_key, keys_needed=keys_needed - set(next_key), p=p+next_key)
            d = self.nodes[key][next_key] + nshort[0]
            if d < out:
                out = d
                new_path = p + nshort[1]
                # print(f'found shorter path with key {key} and next {next_key}')
            else:
                pass

        self.distance_to_keys[dictkey] = (out, new_path)
        return out, new_path

def get_robit():
    with open('data.txt', 'r') as f:
        data = [[x for x in line.strip()] for line in f]
        # print(data)

        start = time.time()

        robit = Robit(data)
        robit.get_nodes()
    return robit

if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        data = [[x for x in line.strip()] for line in f]
        # print(data)

        start = time.time()

        robit = Robit(data)
        print(f'Keys: {robit.key_count}')
        print(f'Key Locations: {robit.keys}')
        # print(robit.current)


        distance, path = robit.find_shortest()
        print(distance)
        print(path)

        # path = '@deacfigbh'
        # path = '@dhjymtlxsewbgcunqovrpkfaiz'
        # robit.draw_path(path)



        end = time.time()
        print(f'Total time: {(end-start):.02f} seconds.')


    with open('data1.txt', 'r') as f:
        data = [[x for x in line.strip()] for line in f]
        robit = Robit(data)
        robit.get_nodes()
        out1 = robit.find_shortest_no_doors()

    with open('data2.txt', 'r') as f:
        data = [[x for x in line.strip()] for line in f]
        robit = Robit(data)
        robit.get_nodes()
        out2 = robit.find_shortest_no_doors()

    with open('data3.txt', 'r') as f:
        data = [[x for x in line.strip()] for line in f]
        robit = Robit(data)
        robit.get_nodes()
        out3 = robit.find_shortest_no_doors()

    with open('data4.txt', 'r') as f:
        data = [[x for x in line.strip()] for line in f]
        robit = Robit(data)
        robit.get_nodes()
        out4 = robit.find_shortest_no_doors()

    print(out1, out2, out3, out4)
    print(out1[0] + out2[0] + out3[0] + out4[0])
