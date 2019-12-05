inc = lambda n: all([int(b) >= int(a) for (a, b) in zip(str(n), str(n)[1:])])
adj = lambda n: any(a == b for a, b in zip(str(n), str(n)[1:]))
has_2 = lambda n: any(str(n).count(c) == 2 for c in str(n))
nums = range(245318, 765747 + 1)
print(f'part 1: {len(list(filter(inc, filter(adj, nums))))}')
print(f'Part 2: {len(list(filter(has_2, filter(inc, nums))))}')