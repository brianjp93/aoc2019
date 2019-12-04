"""day4.py
"""


VALID_RANGE = (245318, 765747)

def is_valid(num, extra=True):
    num_str = str(num)
    if is_increasing(num):
        if has_same_adj(num, extra=extra):
            # if num >= VALID_RANGE[0] and num <= VALID_RANGE[1]:
                # if len(num_str) == 6:
            return True
    return False

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

def find_valid_count(extra=True):
    count = 0
    for i in range(VALID_RANGE[0], VALID_RANGE[1] + 1):
        if is_valid(i, extra=extra):
            count += 1
    return count

if __name__ == '__main__':
    valid_count = find_valid_count()
    print(valid_count)

    valid_count = find_valid_count(extra=False)
    print(valid_count)
