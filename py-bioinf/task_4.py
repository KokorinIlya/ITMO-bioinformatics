import math

GAP_OPEN_PENALTY = -11
GAP_EXTENSION_PENALTY = -1


def check_symmetry(score_matrix, keys):
    for key_a in keys:
        for key_b in keys:
            if (key_a, key_b) not in score_matrix or (key_b, key_a) not in score_matrix or \
                    score_matrix[(key_a, key_b)] != score_matrix[(key_b, key_a)]:
                return False
    return True


def read_score_matrix(file_name):
    result = {}
    with open(file_name, 'r') as file:
        all_keys = file.readline().strip().split()[1:]

        for cur_line in file:
            parts = cur_line.strip().split()
            cur_key = parts[0]
            cur_scores = [int(x) for x in parts[1:]]
            assert len(cur_scores) == len(all_keys)

            for another_key, cur_score in zip(all_keys, cur_scores):
                assert (another_key, cur_key) not in result or result[(another_key, cur_key)] == cur_score
                result[(cur_key, another_key)] = cur_score

        assert check_symmetry(result, all_keys)
    return result


def get_strings(file_name):
    with open(file_name, 'r') as file:
        return [cur_line.strip() for cur_line in file.readlines()]


def get_d(x, y):
    lx = len(x)
    ly = len(y)
    prev = {}

    M: list = [[-math.inf for _ in range(lx + 1)] for _ in range(ly + 1)]
    M[0][0] = 0

    Ix: list = [[-math.inf for _ in range(lx + 1)] for _ in range(ly + 1)]
    for i in range(ly + 1):
        Ix[i][0] = i * GAP_EXTENSION_PENALTY + GAP_OPEN_PENALTY
        if i > 0:
            prev[("Ix", i, 0)] = ("Ix", i - 1, 0)

    Iy: list = [[-math.inf for _ in range(lx + 1)] for _ in range(ly + 1)]
    for j in range(lx + 1):
        Iy[0][j] = j * GAP_EXTENSION_PENALTY + GAP_OPEN_PENALTY
        if j > 0:
            prev[("Iy", 0, j)] = ("Iy", 0, j - 1)

    return M, Ix, Iy, prev


def pretty_print_d(d):
    s = '\n'.join([' '.join([str(cur_elem) for cur_elem in cur_row]) for cur_row in d])
    print(s)
    print('--------------')


def calc_d(score_matrix, M, Ix, Iy, x, y, prev):
    for i in range(1, len(y) + 1):
        for j in range(1, len(x) + 1):
            cur_x = y[i - 1]
            cur_y = x[j - 1]
            assert (cur_x, cur_y) in score_matrix and \
                   (cur_y, cur_x) in score_matrix and \
                   score_matrix[(cur_y, cur_x)] == score_matrix[(cur_x, cur_y)]
            cur_cost = score_matrix[(cur_x, cur_y)]

            # M[i][j]
            M[i][j] = M[i - 1][j - 1] + cur_cost
            prev[("M", i, j)] = ("M", i - 1, j - 1)

            if Ix[i - 1][j - 1] + cur_cost > M[i][j]:
                M[i][j] = Ix[i - 1][j - 1] + cur_cost
                prev[("M", i, j)] = ("Ix", i - 1, j - 1)

            if Iy[i - 1][j - 1] + cur_cost > M[i][j]:
                M[i][j] = Iy[i - 1][j - 1] + cur_cost
                prev[("M", i, j)] = ("Iy", i - 1, j - 1)

            # Ix[i][j]
            Ix[i][j] = M[i - 1][j] + GAP_OPEN_PENALTY
            prev[("Ix", i, j)] = ("M", i - 1, j)

            if Ix[i - 1][j] + GAP_EXTENSION_PENALTY > Ix[i][j]:
                Ix[i][j] = Ix[i - 1][j] + GAP_EXTENSION_PENALTY
                prev[("Ix", i, j)] = ("Ix", i - 1, j)

            # Iy[i][j]
            Iy[i][j] = M[i][j - 1] + GAP_OPEN_PENALTY
            prev[("Iy", i, j)] = ("M", i, j - 1)

            if Iy[i][j - 1] + GAP_EXTENSION_PENALTY > Iy[i][j]:
                Iy[i][j] = Iy[i][j - 1] + GAP_EXTENSION_PENALTY
                prev[("Iy", i, j)] = ("Iy", i, j - 1)


def main():
    score_matrix = read_score_matrix('BLOSUM62.txt')
    print(score_matrix)
    x, y = get_strings('rosalind_ba5j.txt')
    print(x, y)
    M, Ix, Iy, prev = get_d(x, y)
    pretty_print_d(M)
    pretty_print_d(Ix)
    pretty_print_d(Iy)
    calc_d(score_matrix, M, Ix, Iy, x, y, prev)
    pretty_print_d(M)
    pretty_print_d(Ix)
    pretty_print_d(Iy)


if __name__ == '__main__':
    main()
