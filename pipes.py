from functools import reduce


class Data:
    def __call__(self, *args, **kwargs):
        return lambda x: x(*args, **kwargs)

    def __lt__(self, other):
        return lambda x: x < other

    def __le__(self, other):
        return lambda x: x <= other

    def __eq__(self, other):
        return lambda x: x == other

    def __ne__(self, other):
        return lambda x: x != other

    def __gt__(self, other):
        return lambda x: x > other

    def __ge__(self, other):
        return lambda x: x >= other

    def __hash__(self):
        return lambda x: hash(x)

    def __repr__(self):
        return lambda x: repr(x)

    def __str__(self):
        return lambda x: str(x)

    def __bytes__(self):
        return lambda x: bytes(x)

    def __bool__(self):
        return lambda x: bool(x)

    def __getattr__(self, item):
        return lambda x: x.__getattr__(item)

    def __setattr__(self, key, value):
        return lambda x: x.__setattr__(key, value)

    def __delattr__(self, item):
        return lambda x: x.__delattr__(item)

    def __len__(self):
        return lambda x: len(x)

    def __getitem__(self, item):
        return lambda x: (list(x) if isinstance(x, (map, filter)) else x).__getitem__(item)

    def __setitem__(self, key, value):
        return lambda x: (list(x) if isinstance(x, (map, filter)) else x).__setitem__(key, value)

    def __delitem__(self, key):
        return lambda x: (list(x) if isinstance(x, (map, filter)) else x).__delitem__(key)

    def __iter__(self):
        return lambda x: x.__iter__()

    def __reversed__(self):
        return lambda x: x.__reversed__()

    def __contains__(self, item):
        return lambda x: item in x

    def __add__(self, other):
        return lambda x: x + other

    def __sub__(self, other):
        return lambda x: x - other

    def __mul__(self, other):
        return lambda x: x * other

    def __truediv__(self, other):
        return lambda x: x / other

    def __floordiv__(self, other):
        return lambda x: x // other

    def __mod__(self, other):
        return lambda x: x % other

    def __pow__(self, power, modulo=None):
        return lambda x: x.__pow__(power, modulo)

    def __radd__(self, other):
        return lambda x: other + x

    def __rsub__(self, other):
        return lambda x: other - x

    def __rmul__(self, other):
        return lambda x: other * x

    def __rtruediv__(self, other):
        return lambda x: other / x

    def __rfloordiv__(self, other):
        return lambda x: other // x

    def __rmod__(self, other):
        return lambda x: other % x

    def __rpow__(self, power, modulo=None):
        return lambda x: x.__rpow__(power, modulo)

    def __neg__(self):
        return lambda x: x.__neg__()

    def __pos__(self):
        return lambda x: x.__pos__()

    def __abs__(self):
        return lambda x: abs(x)

    def __invert__(self):
        return lambda x: x

    def __complex__(self):
        return lambda x: x.__complex__()

    def __int__(self):
        return lambda x: int(x)

    def __float__(self):
        return lambda x: float(x)

    def __round__(self, n=None):
        return lambda x: x.__round__(n)

    def has(self, item):
        return lambda x: item in x

    def in_(self, lst):
        return lambda x: x in lst


class Pipe:
    def __init__(self, steps=None):
        if steps is None:
            steps = []
        self.steps = steps

    def __call__(self, data):
        reduction = reduce(lambda d, step: step(d), self.steps, data)
        return list(reduction) if isinstance(reduction, (map, filter)) else reduction

    def __gt__(self, other):
        return Pipe(self.steps + [curry(other[0], *tuple(other[1:])) if isinstance(other, (tuple, list)) else other])

    def __le__(self, other):
        f, lsts = (other, tuple()) if callable(other) else (other[0], tuple(other[1:]))
        return Pipe(self.steps + [lambda x: map(f, x, *lsts)])

    def __ge__(self, other):
        return Pipe(self.steps + [lambda x: reduce(other, x) if callable(other) else reduce(other[0], x, other[1])])

    def __lt__(self, other):
        return Pipe(self.steps+
                    [(lambda x: map(lambda f: f(x), other))])

    def __contains__(self, other):
        return Pipe(self.steps + [lambda x: filter(other, x)])

    def __floordiv__(self, other):
        return Pipe(self.steps +
                    [(lambda args: curry(other[0], *tuple(other[1:]), *tuple(args)))
                    if isinstance(other, (tuple, list)) else (lambda args: other(*tuple(args)))])


def curry(f, *args, **kwargs):
    return lambda *args1, **kwargs1: f(*(args + args1), **(kwargs | kwargs1))
