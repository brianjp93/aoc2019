"""day4.py
"""
VALID_RANGE = (245318, 765747)

def has_same_adj(num, run_length=2, extra=True):
    num_str = str(num)
    counts = []
    for c in num_str:
        if len(counts) > 0 and counts[-1][0] == c:
            counts[-1][1] += 1
        else:
            counts.append([c, 1])
        if extra:
            if counts[-1][1] >= 2:
                return True
        else:
            if len(counts) >= 2 and counts[-2][1] == 2:
                return True
    if not extra:
        if counts[-1][1] == 2:
            return True
    return False

def is_increasing(num):
    num_str = str(num)
    for i in range(len(num_str) - 1):
        if int(num_str[i]) > int(num_str[i+1]):
            return False
    return True

if __name__ == '__main__':
    nums = range(VALID_RANGE[0], VALID_RANGE[1] + 1)
    increasing = list(filter(is_increasing, nums))
    
    part1 = list(filter(has_same_adj, increasing))
    print(len(part1))

    part2 = list(filter(lambda x: has_same_adj(x, extra=False), increasing))
    print(len(part2))
