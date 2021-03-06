#!/usr/bin/env python

import itertools

substitutions = [
    ("J", "5:1:"),
    ("K", "4:1:"),
    ("M", "3:1:"),
    ("L", "2:1:"),
    ("Q", "1:1:"),
    ("S", "0:1:"),
    ("j", "5:0:"),
    ("k", "4:0:"),
    ("m", "3:0:"),
    ("l", "2:0:"),
    ("q", "1:0:"),
    ("s", "0:0:"),
    ("n", "9"),
    ("b", "8"),
    ("v", "7"),
    ("c", "6"),
    ("z", "5"),
    ("h", "4"),
    ("g", "3"),
    ("e", "2"),
    ("p", "1"),
    ("o", "0"),
    ("w", "9:"),
    ("i", "8:"),
    ("u", "7:"),
    ("d", "6:"),
    ("x", "5:"),
    ("r", "4:"),
    ("f", "3:"),
    ("y", "2:"),
    ("t", "1:"),
    ("a", "0:")
]

def decrypt(s):
    for pair in substitutions:
        s = s.replace(pair[0], pair[1])
    return [int(i) for i in s.split(":")]

def encrypt(l):
    s = ":".join(str(i) for i in l)
    for pair in reversed(substitutions):
        s = s.replace(pair[1], pair[0])
    return s

def hexagonal(n):
    return (n * 3) * (n - 1) + 1

def pairwise(i):
    # From itertools docs
    a, b = itertools.tee(i)
    next(b, None)
    return itertools.izip(a, b)

class Slot(object):

    def __init__(self):
        self.enabled = True
        self.conns = 0
        self.filled = False
        self.locked = False

    def __repr__(self):
        return "<Slot(%senabled, %sfilled(%d), %slocked)>" % (
            "" if self.enabled else "not ",
            "" if self.filled else "not ",
            self.conns,
            "" if self.locked else "not ")

    def __str__(self):
        if not self.enabled:
            return "X"
        elif self.filled:
            if self.locked:
                return "{%d}" % self.conns
            else:
                return "%d" % self.conns
        else:
            return "-"

class Hexiom(object):

    def __init__(self, level):
        self.level = decrypt(level)
        self.parse()

    def parse(self):
        # First, split off the level into its groups
        self.size, disabled_count, filled_count, locked_count = \
            self.level[:4]
        filled_count *= 3

        # Allocate slots
        self.slots = [Slot() for i in range(hexagonal(self.size))]

        disabled = self.level[4:4+disabled_count]
        for s in disabled:
            self.slots[s].enabled = False

        filled = self.level[4+disabled_count:4+disabled_count+filled_count]
        i = iter(filled)
        for conns, start_slot, finish_slot in itertools.izip(i, i, i):
            self.slots[finish_slot].filled = True
            self.slots[finish_slot].conns = conns

        locked = self.level[4+disabled_count+filled_count:]
        for s in locked:
            self.slots[s].locked = True

        # Allocate rings
        self.rings = [self.slots[i:j]
            for i, j in pairwise(hexagonal(x) for x in range(self.size + 1))
        ]

        self.demangle_rings()

    def demangle_rings(self):
        """
        Convert the rings to a fully linear format.
        
        Hexiom stores the higher rings strangely. Starting with ring 3, the
        3rd slot should actually be at the beginning of the ring, and in each
        higher ring, another slot becomes misplaced. This method simply
        cherry-picks each misplaced element out of the list and puts it at the
        beginning, where it belongs.
        """
        for i, ring in enumerate(self.rings[2:]):
            for index in range(i * 2 + 2, 0, -2):
                ring.append(ring.pop(index))

    def dump(self):
        for i, ring in enumerate(self.rings):
            print "Unrolled ring %d:" % (i + 1,)
            fmt = "[%s]" % " ".join("%s" * len(ring))
            print fmt % tuple(ring)
