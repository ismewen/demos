a = [1, 2, 3, 4]
a.append(5)
a.insert(7, 8)
print(a)


a = [1, 2, 3, 4]
a.insert(1, 2) # [1, 2, 2, 3,4]
a.insert(10, 0) # [1, 2, ,2, 3, 4, 0]
print(a)

a = [1, 2, 3, 4]
c = a + [5, 6, 7]
print(c)

a = [1, 1, 2, 3]
print(a[1])
print(a[0])

print(a.index(1))
print(a.count(1))

a = [1, 2, 3, 4]
b = a[:]
b[0] = 2
print(a, b)

a = [1, 2, 3, 4, 5]
b = a[::2] #[1, 3, 5]
print(b)