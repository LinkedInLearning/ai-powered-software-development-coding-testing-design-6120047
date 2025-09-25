def f(a, b):
    r = []
    while b:
        r.append(a % 10)
        a //= 10
        b -= 1
    return r[::-1]

print(f(987654, 3))