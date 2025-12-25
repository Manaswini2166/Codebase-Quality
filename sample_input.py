import imp   # deprecated module


def very_long_function(a, b, c, d, e, f):
    total = 0
    for i in range(10):
        for j in range(10):
            for k in range(10):
                if i > 2:
                    if j > 3:
                        total += i + j + k
    return total


def small_function(x):
    return x * 2
