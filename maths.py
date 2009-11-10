import math

def gcd(a, b):
    """
    Return the greatest common divisor of a and b.
    """

    if not a:
        return b
    elif not b:
        return a

    while a and b and (a != b):
        if a > b:
            a -= b
        elif b > a:
            b -= a

    return a if a else b

def lcm(*args):
    """
    Return the least common denominator of the inputs.
    """

    numbers = set(int(i) for i in args)

    if not numbers:
        return 0

    numbers.discard(0)

    while len(numbers) > 1:
        first = numbers.pop()
        second = numbers.pop()

        numbers.add((first * second)/gcd(first, second))

    return numbers.pop()

def factor(x):
    """
    Returns a list of factors of x, excluding 1.
    >>> factor(12)
    [2, 2, 3]
    >>> factor(127)
    [127]
    >>> factor(720)
    [2, 2, 2, 2, 3, 3, 5]
    """

    return list(lazyfactor(x))

def lazyfactor(x):
    """
    Returns a generator of factors of x, excluding 1.
    """

    while x > 1:
        prime = True
        for i in xrange(2, long(math.sqrt(x)) + 1):
            if not x % i:
                yield i
                x /= i
                prime = False
                break
        if prime:
            yield x
            break