import vec

a = [2.0, 6.1, 7.1]
b = [4.5, 2.2, 9.9]
c = [4.5, 2.2, 9.9, 5.5]

print(vec.add(a, b))
print(vec.sub(a, b))
print(vec.dot(a, b))

# vectors of different lengths
print(vec.add(a, c))
print(vec.sub(a, c))
print(vec.dot(a, c))

print(vec.mul(a, 2))
print(vec.div(b[:-1], b[-1]))
