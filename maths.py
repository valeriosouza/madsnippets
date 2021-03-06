import math

def gcd(a, b):
    """
    Return the greatest common divisor of a and b.

    >>> gcd(3, 6)
    3
    >>> gcd(19872, 526293)
    9
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

    >>> lcm(27, 9, 3)
    27
    >>> lcm(2384, 2179)
    5194736
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
        top = math.sqrt(x)
        for i in xrange(2, long(top) + 1):
            if not x % i:
                yield i
                x /= i
                prime = False
                break
            if not i % 10000000:
                print "%d/%d (%f%%)" % (i, top, 100.0 * i / top)
        if prime:
            yield x
            break

def mma(old, new, weight):
    """
    Performs a Moving Modified Average, using the old value, new value,
    and a weight.

    Weight must be greater than zero.
    """

    return ((weight - 1) * old + new) / weight
