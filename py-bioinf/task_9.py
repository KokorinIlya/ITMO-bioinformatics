def read_file(file_name):
    with open(file_name, 'r') as file:
        text = file.readline().strip()
        patterns = file.readline().strip().split()
        d = int(file.readline().strip())
    return text, patterns, d


def calc_dist(subtext, pattern):
    assert len(subtext) == len(pattern)
    result = 0
    for cur_t, cur_p in zip(subtext, pattern):
        if cur_p != cur_t:
            result += 1
    return result


def process_pattern(text, pattern, d):
    result = []
    for start_idx in range(len(text) - len(pattern) + 1):
        cur_substr = text[start_idx:start_idx + len(pattern)]
        cur_res = calc_dist(cur_substr, pattern)
        if cur_res <= d:
            result.append(start_idx)
    return result


def main():
    text, patterns, d = read_file('rosalind_ba9o.txt')
    result = []
    for cur_pattern in patterns:
        cur_result = process_pattern(text, cur_pattern, d)
        result.extend(cur_result)
    result.sort()
    print(' '.join(map(str, result)))


if __name__ == '__main__':
    main()
