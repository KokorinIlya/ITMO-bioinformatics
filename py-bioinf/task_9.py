def read_file(file_name):
    with open(file_name, 'r') as file:
        text = file.readline().strip()
        patterns = file.readline().strip().split()
        d = int(file.readline().strip())
    return text, patterns, d


def create_suf_array(s):
    suffixes = [(s[cur_idx:], cur_idx) for cur_idx in range(len(s))]
    return sorted(suffixes)


def bin_search(left_border, right_border, pred):
    assert left_border + 1 <= right_border
    if pred(left_border):
        return left_border
    if not pred(right_border):
        return None

    cur_left = left_border
    cur_right = right_border

    while cur_left + 1 < cur_right:
        assert not pred(cur_left) and pred(cur_right)
        mid = (cur_left + cur_right) // 2
        if pred(mid):
            cur_right = mid
        else:
            cur_left = mid
    assert cur_left + 1 == cur_right and not pred(cur_left) and pred(cur_right)
    return cur_right


def get_left_border(pattern, suf_arr, left_border, right_border, symbol_idx):
    assert left_border + 1 <= right_border

    def pred(suf_idx):
        assert left_border <= suf_idx <= right_border
        if suf_idx == right_border:
            return True

        cur_suf, _ = suf_arr[suf_idx]
        if len(cur_suf) <= symbol_idx:
            return False
        return cur_suf[symbol_idx] >= pattern[symbol_idx]

    result = bin_search(left_border, right_border, pred)
    assert result is not None
    return result


def get_right_border(pattern, suf_arr, left_border, right_border, symbol_idx):
    assert left_border + 1 <= right_border

    def pred(suf_idx):
        assert left_border <= suf_idx <= right_border
        if suf_idx == right_border:
            return True

        cur_suf, _ = suf_arr[suf_idx]
        if len(cur_suf) <= symbol_idx:
            return False
        return cur_suf[symbol_idx] > pattern[symbol_idx]

    result = bin_search(left_border, right_border, pred)
    assert result is not None
    return result


def find_substring(suf_arr, substr):
    left_border = 0
    right_border = len(suf_arr)
    for symbol_idx in range(len(substr)):
        new_left_border = get_left_border(substr, suf_arr, left_border, right_border, symbol_idx)
        new_right_border = get_right_border(substr, suf_arr, left_border, right_border, symbol_idx)

        if new_left_border == new_right_border:
            return new_left_border, new_right_border

        left_border = new_left_border
        right_border = new_right_border
    return left_border, right_border


def calc_mismatches(text, pattern, begin_idx, end_idx):
    assert begin_idx < end_idx and end_idx - begin_idx == len(pattern)
    res = 0
    for i in range(begin_idx, end_idx):
        if text[i] != pattern[i - begin_idx]:
            res += 1
    return res


def try_match_part(text, suf_arr, pattern, cur_part, d, cur_start_idx):
    result = []
    left, right = find_substring(suf_arr, cur_part)
    for i in range(left, right):
        _, part_start_idx = suf_arr[i]
        if cur_start_idx > part_start_idx:
            continue

        pattern_start_idx = part_start_idx - cur_start_idx
        pattern_end_idx = pattern_start_idx + len(pattern)
        if pattern_end_idx > len(text):
            continue

        mismatches = calc_mismatches(text, pattern, pattern_start_idx, pattern_end_idx)
        if mismatches <= d:
            result.append(pattern_start_idx)
    return result


def process_pattern(text, suf_arr, pattern, d):
    part_len = len(pattern) // (d + 1)
    cur_start_idx = 0
    result = set()

    while cur_start_idx < len(pattern):
        cur_end_idx = cur_start_idx + part_len
        if cur_end_idx > len(pattern):
            cur_end_idx = len(pattern)
        cur_part = pattern[cur_start_idx:cur_end_idx]

        match_result = try_match_part(text, suf_arr, pattern, cur_part, d, cur_start_idx)
        result |= set(match_result)

        cur_start_idx = cur_end_idx
    return list(result)


def main():
    text, patterns, d = read_file('rosalind_ba9o.txt')
    suf_arr = create_suf_array(text)
    result = []

    for pattern in patterns:
        result.extend(process_pattern(text, suf_arr, pattern, d))

    result.sort()
    print(' '.join(map(str, result)))


if __name__ == '__main__':
    main()
