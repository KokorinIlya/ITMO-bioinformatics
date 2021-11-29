class Variable:
    def __init__(self, name):
        self.name = name


class Constant:
    def __init__(self, value):
        self.value = value


op_by_symbol = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '^': lambda x, y: x ** y,
    '*': lambda x, y: x * y
}


class Operation:
    def __init__(self, symbol):
        self.op = op_by_symbol[symbol]


def parse():
    with open('unimulti2.in', 'r') as file:
        return [
            Operation(cur_part) if cur_part in op_by_symbol.keys() else
            Variable(cur_part) if cur_part in {'x', 'y'} else
            Constant(int(cur_part))
            for cur_part in file.readline().split()
        ]


def calc(exp, x, y):
    if max(abs(x), abs(y)) > 10:
        return None

    stack = []
    variables = {
        'x': x,
        'y': y
    }
    for cur_exp in exp:
        if isinstance(cur_exp, Variable):
            stack.append(variables[cur_exp.name])
        elif isinstance(cur_exp, Constant):
            stack.append(cur_exp.value)
        else:
            assert isinstance(cur_exp, Operation)
            assert len(stack) >= 2
            y = stack.pop()
            x = stack.pop()
            stack.append(cur_exp.op(x, y))
    assert len(stack) == 1
    return stack[0]


def is_min_extremum(cur_value, near_value):
    assert cur_value is not None and near_value is not None
    return cur_value < near_value


def is_max_extremum(cur_value, near_value):
    assert cur_value is not None and near_value is not None
    return cur_value > near_value


def has_multiple_extremums(exp, is_extremum):
    has_extremum = False
    ds = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for x in range(-10, 11):
        for y in range(-10, 11):
            cur_value = calc(exp, x, y)
            assert cur_value is not None

            all_match = True
            for dx, dy in ds:
                nx = x + dx
                ny = y + dy
                near_value = calc(exp, nx, ny)
                if near_value is not None and not is_extremum(cur_value, near_value):
                    all_match = False
                    break
            if all_match:
                if has_extremum:
                    return True
                else:
                    has_extremum = True

    return False


def has_plateaus(exp):
    ds = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]
    for x in range(-10, 11):
        for y in range(-10, 11):
            cur_value = calc(exp, x, y)
            assert cur_value is not None
            for dx, dy in ds:
                nx = x + dx
                ny = y + dy
                near_value = calc(exp, nx, ny)
                if near_value is not None and near_value == cur_value:
                    return True
    return False


def main():
    exp = parse()

    with open('unimulti2.out', 'w') as file:
        if has_multiple_extremums(exp, is_max_extremum):
            file.write('Multiple local maxima: Yes\n')
        else:
            file.write('Multiple local maxima: No\n')

        if has_multiple_extremums(exp, is_min_extremum):
            file.write('Multiple local minima: Yes\n')
        else:
            file.write('Multiple local minima: No\n')

        if has_plateaus(exp):
            file.write('Plateaus: Yes\n')
        else:
            file.write('Plateaus: No\n')


if __name__ == '__main__':
    main()
