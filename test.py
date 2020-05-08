a = {10.5: [0, '1992', '2268']}
b = {10.6: ['1975', 0, 0]}

print(a[10.5].count(True))
print(b[10.6].count(False))

if a.count(True) == b.count(False):
    for i in range(len(a)):
        a[i] = a[i] or b[i]
        b[i] = 0
print(a,b)