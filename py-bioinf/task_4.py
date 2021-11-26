GAP_OPEN_PENALTY = -11
GAP_EXTENSION_PENALTY = -1
import math


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
        return ['.' + cur_line.strip() for cur_line in file.readlines()]


def get_d(x, y):
    M = [
        [
            0 if i == 0 and j == 0 else -math.inf
            for j in range(len(x))
        ]
        for i in range(len(y))
    ]

    Ix = [
        [
            i * GAP_EXTENSION_PENALTY + GAP_OPEN_PENALTY if j == 0 else -math.inf
            for j in range(len(x))
        ]
        for i in range(len(y))
    ]

    Iy = [
        [
            j * GAP_EXTENSION_PENALTY + GAP_OPEN_PENALTY if i == 0 else -math.inf
            for j in range(len(x))
        ]
        for i in range(len(y))
    ]

    return {
        "M": M,
        "Ix": Ix,
        "Iy": Iy
    }


def pretty_print_d(d):
    for cur_c, cur_d in d.items():
        print(cur_c)
        s = '\n'.join([' '.join([str(cur_elem) for cur_elem in cur_row]) for cur_row in cur_d])
        print(s)
        print('--------------')


def calc_d(score_matrix, d, x, y):
    for i in range(1, len(y)):
        for j in range(1, len(x)):
            cur_x = y[i]
            cur_y = x[j]
            assert (cur_x, cur_y) in score_matrix and \
                   (cur_y, cur_x) in score_matrix and \
                   score_matrix[(cur_y, cur_x)] == score_matrix[(cur_x, cur_y)]
            cur_cost = score_matrix[(cur_x, cur_y)]

            # TODO
            d["M"][i][j] = max(
                d["M"][i - 1][j - 1],
                d["Ix"][i - 1][j - 1],
                d["Iy"][i - 1][j - 1],
            ) + cur_cost

            d["Ix"][i][j] = max(
                d["M"][i - 1][j] + GAP_OPEN_PENALTY,
                d["Ix"][i - 1][j] + GAP_EXTENSION_PENALTY
            )

            d["Iy"][i][j] = max(
                d["M"][i][j - 1] + GAP_OPEN_PENALTY,
                d["Iy"][i][j - 1] + GAP_EXTENSION_PENALTY
            )


def main():
    score_matrix = read_score_matrix('BLOSUM62.txt')
    print(score_matrix)
    x, y = get_strings('rosalind_ba5j.txt')
    print(x, y)
    d = get_d(x, y)
    pretty_print_d(d)
    calc_d(score_matrix, d, x, y)
    pretty_print_d(d)


if __name__ == '__main__':
    main()
