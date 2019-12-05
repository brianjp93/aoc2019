# THIS ISN'T WORKING YET

data = [int(x) for x in open('data.txt').read().split(',')]
data1 = list(data)
data1[1], data1[2] = 12, 2
print(data1)

runcode = {
    1: lambda x, y, z: data1.__setitem__(data1[z], data1[x]+data1[y]),
    2: lambda x, y, z: data1.__setitem__(data1[z], data1[x]*data1[y]),
    99: lambda x, y, z: [data1.__setitem__(j, None) for j in range(x, len(data1))],
}
out = [runcode[data1[i]](i+1, i+2, i+3) if data1[i] is not None else None for i in range(0, len(data1), 4)]
print(out)
print(data1)