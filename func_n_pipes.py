"""
Cased() | ((f, g), 1) | (1, 1) | (lambda n: n*fact(n-1))
"""
from functools import reduce, lru_cache


class Cased:
    def __init__(self, cases=None, save_keys=True):
        if cases is None:
            cases = []
        self.cases = cases
        self.saved_cases = []
        self.general = None
        self.save_keys = save_keys

    def __or__(self, next_case):
        self.saved_cases = []
        if isinstance(next_case, (tuple, list)):
            return Cased(self.cases + [next_case], save_keys=self.save_keys)
        else:
            self.general = next_case
            return self

    def save_k(self, data, computation):
        if self.save_keys and computation != data and (data not in [item[0] for item in self.saved_cases]):
            self.saved_cases.append((data, computation))
        return computation

    def __call__(self, data):
        try:
            for case in self.cases + self.saved_cases:
                if case[0] == data:
                    return self.save_k(data, case[1](data)) if callable(case[1]) else case[1]
                elif callable(case[0]) and case[0](data):
                    return self.save_k(data, case[1](data) if callable(case[1]) else case[1])
                elif isinstance(case[0], (list, tuple)):
                    for cond in case[0]:
                        if cond == data:
                            return self.save_k(data, case[1](data)) if callable(case[1]) else case[1]
                        elif callable(cond) and cond(data):
                            return self.save_k(data, case[1](data) if callable(case[1]) else case[1])
            # print(f'Calculating on {data}')
            return self.save_k(data, self.general(data)) if callable(self.general) else self.general
        except RecursionError:
            if isinstance(data, int):
                try:
                    was_sk = self.save_keys
                    if not was_sk:
                        self.save_keys = True
                    for i in (range(data) if data >= 0 else range(data, 0, -1)):
                        self.save_k(i, self(i))
                    comp = self(data)
                    if not was_sk:
                        self.save_keys = False
                        self.saved_cases = []
                    return comp
                except RecursionError:
                    raise RecursionError('Could not overcome python recursion limit, '
                                         'with some int predictive iterative computations\n'
                                         'Try to iteratively call with easier data or change max'
                                         ' recursion depth python parameter')
            else:
                raise RecursionError('Could not overcome python recursion limit, because data is not int\n'
                                     'Try to use save keys and iteratively call with easier data or change max'
                                     ' recursion depth python parameter')


class Value:
    def __init__(self, data):
        self.data = data

    def __or__(self, next_step):
        return Value(next_step(self.data))


class Fun:
    def __init__(self, steps=None):
        if steps is None:
            steps = []
        self.steps = steps

    def __or__(self, next_step):
        if not callable(next_step):
            return self(next_step)
        return Fun(self.steps + [next_step])

    def __call__(self, data):
        return reduce(lambda d, step: step(d), self.steps, data)

    # data >> Fun()
    def __rrshift__(self, data):
        return Value(self(data))

    # (...) >> (lambda x, y: x+y) | ...
    def __rshift__(self, reduce_func):
        return self | reduces(reduce_func)

    # ... ^ fact | ...
    def __xor__(self, map_fun):
        return self | maps(map_fun) | tuple

    def __and__(self, filter_fun):
        return self | filters(filter_fun) | tuple

    # ... << (f1| f1_2)
    # (f1, f2, f3) -> (r1, r2, r3)
    # lambda x: map(lambda f: f(x), other_funs)
    def __lshift__(self, other_funs):
        return self | (lambda x: tuple(map(lambda f: f(x), other_funs)))


def filters(f):
    return lambda series: filter(f, series)


def reduces(f):
    return lambda series: reduce(f, series)


def maps(f):
    return lambda series: map(f, series)


# rows = lambda mat: [[line[i] for line in mat] for i in range(len(mat[0]))]
throw = lambda x: x

cols = Fun() << (
    Fun() | len | range | tuple,
    throw
) | (lambda data: Fun() ^ (lambda i: Fun() ^ slice(i) | data[1]) | data[0])

methf = lambda name: lambda data: getattr(data, name)

call = lambda *args, **kwargs: lambda f: f(*args, **kwargs)

meth = lambda name, *args, **kwargs: Fun() | methf(name) | call(*args, **kwargs)

slice = lambda x, y=None: lambda seq: seq[x:y] if y else seq[x]

save_mapping = lambda f: Cased() | f
