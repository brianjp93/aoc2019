"""day19.py

I got the answer with this code but it's gross and I don't know
how to do it elegantly.

"""
from computer import Computer

with open('data.txt', 'r') as f:
    data = list(map(int, f.read().split(',')))
    comp = Computer(data)

def check_box(x, y):
    space = 99
    leftx, rightx = x, x+space
    topy, boty = y-space, y
    if any([leftx<0, rightx<0, topy<0, boty<0]):
        return [0, 0, 0, 0]
    return [check(leftx, topy), check(rightx, topy), check(leftx, boty), check(rightx, boty)]

def check(x, y):
    comp.reset()
    comp.inputs = [x, y]
    comp.run()
    out = comp.output[-1]
    return out

if __name__ == '__main__':
    
        # print(data)
        m = []
        y = 7
        x = 5
        # comp = Computer(data)
        # for y in range(50):
        #     lst = []
        #     for x in range(50):
        #         comp.reset()
        #         comp.inputs = [x, y]
        #         comp.run()
        #         # out = list(comp.output)
        #         lst.append(comp.output[0])
        #     m.append(lst)

        # SOME KIND OF GROSS HALF BINARY SEARCH
        found = False
        overshot = False
        while not found:
            if overshot:
                xout = yout = None
                while yout != 0:
                    oldy += 1
                    # print(f'checking {(oldx, oldy)}')
                    yout = check(oldx, oldy)
                while xout != 1:
                    oldx += 1
                    # print(f'checking {(oldx, oldy)}')
                    xout = check(oldx, oldy)

                # print(f'checking {(oldx, oldy)}')
                out = check_box(oldx, oldy)

                if all(out):
                    print(f'Found 100x100 space at {oldx, oldy-99}')
                    break
                else:
                    print(f'Found bad space at {oldx, oldy-99}')
                    

            if not overshot:
                xout = yout = None
                oldx, oldy = x, y
                while yout != 0:
                    y *= 2
                    # print(f'checking {(x, y)}')
                    yout = check(x, y)
                # x*=2
                while xout != 1:
                    x += 1
                    # print(f'checking {(x, y)}')
                    xout = check(x, y)


                # print(f'checking {(x, y)}')
                out = check_box(x, y)
                if all(out):
                    print(f'Found 100x100 space at {x, y-99}')
                    overshot = True

# 762, 1042
checkx, checky = 765, 1145
half = 20
minx = 10000
miny = 10000
# CHECK ALL SPACES IN THE VICINITY OF THE COORDINATES I FOUND
for y in range(checky-half, checky):
    for x in range(checkx-half, checkx):
        box = check_box(x, y)
        if all(box):
            truex = x
            truey = y-99
            print(f'box found at {(truex, truey)}')
            minx = min((truex, minx))
            miny = min((truey, miny))

print(f'Minimum: {(minx, miny)}')
