"""day3.py
"""

def get_data():
    with open('data.txt', 'r') as f:
        lines = [l.split(',') for l in f]
    return lines


def get_all_coords(instructions):
    coord = (0, 0)
    all_coords = [tuple(coord)]
    d = ((0, 1), (1, 0), (0, -1), (-1, 0))
    for instr in instructions:
        val = int(instr[1:])
        unit = d['URDL'.index(instr[0])]
        coord = (coord[0] + (unit[0]*val), coord[1] + (unit[1]*val))
        all_coords.append(coord)
    return all_coords


def find_all_intersections(c_list_1, c_list_2):
    """Get a list of intersecting points.

    Not considering if two lines are on top of eachother.

    """
    intersections = []
    for i in range(0, len(c_list_1)-1):
        c1, c2 = c_list_1[i], c_list_1[i+1]
        cx_start, cx_end = c1[0], c2[0]
        big_cx = max([cx_start, cx_end])
        small_cx = min([cx_start, cx_end])
        
        cy_start, cy_end = c1[1], c2[1]
        big_cy = max([cy_start, cy_end])
        small_cy = min([cy_start, cy_end])
        
        if cx_start != cx_end:
            c_change = 'x'
        else:
            c_change = 'y'
        for j in range(0, len(c_list_2)-1):
            d1, d2 = c_list_2[j], c_list_2[j+1]
            
            dx_start, dx_end = d1[0], d2[0]
            big_dx = max([dx_start, dx_end])
            small_dx = min([dx_start, dx_end])
            
            dy_start, dy_end = d1[1], d2[1]
            big_dy = max([dy_start, dy_end])
            small_dy = min([dy_start, dy_end])
            
            if c_change == 'y':
                if cx_start <= big_dx and cx_start >= small_dx:
                    # could be intersection
                    if dy_start <= big_cy and dy_start >= small_cy:
                        intersections.append((cx_start, dy_start))
                else:
                    continue
            else:
                if cy_start <= big_dy and cy_start >= small_dy:
                    # could be intersection
                    if dx_start <= big_cx and dx_start >= small_cx:
                        intersections.append((dx_start, cy_start))
                else:
                    continue
    intersections.remove((0,0))
    return intersections


def find_steps_to(inter, steps):
    x_int, y_int = inter
    number_of_steps = 0
    for i in range(0, len(steps)-1):
        cx1, cy1 = steps[i]
        cx2, cy2 = steps[i+1]
        
        cx_big = max([cx1, cx2])
        cx_small = min([cx1, cx2])
        
        cy_big = max([cy1, cy2])
        cy_small = min([cy1, cy2])
        if cx1 == cx2:
            if x_int == cx1:
                if y_int <= cy_big and y_int >= cy_small:
                    # intersects here
                    number_of_steps += abs(y_int - cy1)
                    return number_of_steps
                else:
                    #not intersect
                    pass
            number_of_steps += abs(cy1 - cy2)
        else:
            # y stays the same, horizontal move
            if y_int == cy1:
                if x_int <= cx_big and x_int >= cx_small:
                    # intersects here
                    number_of_steps += abs(x_int - cx1)
                    return number_of_steps
                else:
                    #not intersect
                    pass
            number_of_steps += abs(cx1 - cx2)
    print(f'Could not find # steps to coord {inter}')


if __name__ == '__main__':
    data = get_data()
    c1, c2 = get_all_coords(data[0]), get_all_coords(data[1])
    intersections = find_all_intersections(c1, c2)
    closest_intersection = min(intersections, key=lambda elt: abs(elt[0]) + abs(elt[1]))
    print(f'Manhattan distance to closest intersection: {sum(map(abs, closest_intersection))}')

    steps_to_intersections = [(find_steps_to(inter, c1), find_steps_to(inter, c2)) for inter in intersections]
    print(steps_to_intersections)
    steps_each = min(steps_to_intersections, key=sum)
    shortest_wire_path = sum(steps_each)
    print(f'Shortest total wire path: {shortest_wire_path}')
