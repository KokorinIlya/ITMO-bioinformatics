def create_suf_array(s):
    suffixes = [(s[cur_idx:], cur_idx) for cur_idx in range(len(s))]
    return sorted(suffixes)


def read_file(file_name):
    with open(file_name, 'r') as file:
        text = file.readline().strip()
        patterns = [cur_line.strip() for cur_line in file.readlines()]
    return text, patterns


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


def process_pattern(suf_arr, pattern):
    left_border = 0
    right_border = len(suf_arr)
    for symbol_idx in range(len(pattern)):
        new_left_border = get_left_border(pattern, suf_arr, left_border, right_border, symbol_idx)
        new_right_border = get_right_border(pattern, suf_arr, left_border, right_border, symbol_idx)

        left_border = new_left_border
        right_border = new_right_border
    return left_border, right_border


def main():
    text, patterns = read_file('rosalind_ba9h.txt')
    suf_arr = create_suf_array(text)
    result = []
    for cur_pattern in patterns:
        left, right = process_pattern(suf_arr, cur_pattern)
        for i in range(left, right):
            _, start_idx = suf_arr[i]
            result.append(start_idx)
    result.sort()
    print(' '.join(map(str, result)))


if __name__ == '__main__':
    main()
