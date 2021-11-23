def __gen_all_patterns(cur_pattern, pattern_len):
    assert len(cur_pattern) <= pattern_len
    if len(cur_pattern) == pattern_len:
        yield ''.join(cur_pattern)
    else:
        for cur_c in ['A', 'T', 'G', 'C']:
            cur_pattern.append(cur_c)
            yield from __gen_all_patterns(cur_pattern, pattern_len)
            cur_pattern.pop()


def gen_all_patterns(pattern_len):
    yield from __gen_all_patterns([], pattern_len)


def gen_k_mers(text, k):
    assert k <= len(text)
    for start_idx in range(len(text) - k + 1):
        cur_k_mer = text[start_idx:start_idx + k]
        assert len(cur_k_mer) == k
        yield cur_k_mer


def hamming_dist(pattern, k_mer):
    assert len(pattern) == len(k_mer)
    return sum(
        0 if p_c == m_c else 1 for p_c, m_c in zip(pattern, k_mer)
    )


def dist(pattern, text):
    assert len(text) >= len(pattern)
    min_dist = None
    for cur_k_mer in gen_k_mers(text, len(pattern)):
        cur_dist = hamming_dist(pattern, cur_k_mer)
        if min_dist is None or cur_dist < min_dist:
            min_dist = cur_dist
    assert min_dist is not None
    return min_dist


def dist_all(pattern, texts):
    return sum(
        dist(pattern, cur_text) for cur_text in texts
    )


def find_best_pattern(pattern_len, texts):
    assert len(
        set(
            (len(cur_text) for cur_text in texts)
        )
    ) == 1

    min_dist = None
    best_pattern = None

    for cur_pattern in gen_all_patterns(pattern_len):
        cur_dist = dist_all(cur_pattern, texts)
        if min_dist is None or cur_dist < min_dist:
            min_dist = cur_dist
            best_pattern = cur_pattern

    assert min_dist is not None and best_pattern is not None
    return best_pattern


def main():
    with open('rosalind_ba2b.txt', 'r') as file:
        pattern_size = int(file.readline())
        texts = [cur_line.strip() for cur_line in file.readlines()]
        best_pattern = find_best_pattern(pattern_size, texts)
        print(best_pattern)


if __name__ == '__main__':
    main()
