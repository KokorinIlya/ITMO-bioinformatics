def parse_file(file_name):
    with open(file_name, 'r') as file:
        n = int(file.readline().strip())
        dst = [
            [int(x) for x in file.readline().strip().split()]
            for _ in range(n)
        ]
        for i in range(n):
            assert len(dst[i]) == n
        for i in range(n):
            assert dst[i][i] == 0
            for j in range(i + 1, n):
                assert dst[i][j] == dst[j][i]
        return dst


class InternalNodeIdAllocator:
    def __init__(self, n):
        self.n = n

    def allocate(self):
        result = self.n
        self.n += 1
        return result


def get_limb_len(dst, n):
    assert n >= 3
    i = 0
    j = n - 1
    min_val = None
    result_k = None

    for cur_k in range(i + 1, j):
        cur_val = (dst[i][j] + dst[j][cur_k] - dst[i][cur_k]) // 2
        if min_val is None or cur_val < min_val:
            min_val = cur_val
            result_k = cur_k
    return i, result_k, min_val


def get_path_dfs(tree, v_from, v_to):
    assert v_from != v_to
    path: list = [(v_from, 0)]
    visited = {v_from}
    while True:
        assert len(path) > 0
        cur_v, _ = path[-1]
        if cur_v == v_to:
            return path
        assert cur_v in tree

        found_edge = False
        for v_next, edge_len in tree[cur_v].items():
            if v_next not in visited:
                path.append((v_next, edge_len))
                visited.add(v_next)
                found_edge = True
                break
        if not found_edge:
            assert path[-1][0] == cur_v
            path.pop()
        else:
            continue


def add_leaf(tree, path, allocator, new_leaf, limb_len, new_node_dist, total_leaf_count):
    assert len(path) >= 2
    prev_node = path[0][0]
    assert path[0][1] == 0
    next_node, edge_len = path[1]
    cur_path_len = 0
    cur_idx = 1

    while cur_path_len + edge_len < new_node_dist:
        assert cur_idx + 1 < len(path)
        cur_path_len += edge_len
        prev_node = path[cur_idx][0]
        assert path[cur_idx][1] == edge_len
        next_node, edge_len = path[cur_idx + 1]
        cur_idx += 1

    if cur_path_len + edge_len == new_node_dist:
        assert next_node >= total_leaf_count
        assert next_node in tree and new_leaf not in tree[next_node]
        tree[next_node][new_leaf] = limb_len

        assert new_leaf not in tree
        tree[new_leaf] = {
            next_node: limb_len
        }
    else:
        assert cur_path_len < new_node_dist < cur_path_len + edge_len
        prev_edge_len = new_node_dist - cur_path_len
        next_edge_len = edge_len - prev_edge_len
        assert prev_edge_len > 0 and next_edge_len > 0

        new_node = allocator.allocate()
        assert new_node >= total_leaf_count
        assert new_node not in tree
        tree[new_node] = {
            new_leaf: limb_len,
            next_node: next_edge_len,
            prev_node: prev_edge_len
        }

        assert new_leaf not in tree
        tree[new_leaf] = {
            new_node: limb_len
        }

        assert prev_node in tree and next_node in tree[prev_node] and tree[prev_node][next_node] == edge_len and \
               next_node in tree and prev_node in tree[next_node] and tree[next_node][prev_node] == edge_len
        del tree[next_node][prev_node]
        del tree[prev_node][next_node]
        assert new_node not in tree[next_node] and new_node not in tree[prev_node]
        tree[prev_node][new_node] = prev_edge_len
        tree[next_node][new_node] = next_edge_len


def additive_phylogeny(dst, n, allocator):
    if n == 1:
        return {}
    if n == 2:
        cur_dst = dst[0][1]
        return {
            0: {
                1: cur_dst
            },
            1: {
                0: cur_dst
            }
        }

    j = n - 1
    i, k, limb_len = get_limb_len(dst, n)
    tree = additive_phylogeny(dst, n - 1, allocator)
    path = get_path_dfs(tree, v_from=i, v_to=k)
    new_node_dist = dst[i][j] - limb_len
    assert new_node_dist > 0
    add_leaf(tree, path, allocator, j, limb_len, new_node_dist, len(dst))
    return tree


def main():
    dst = parse_file('rosalind_ba7c.txt')
    allocator = InternalNodeIdAllocator(len(dst))
    tree = additive_phylogeny(dst, len(dst), allocator)

    tree_items = sorted(tree.items())
    for from_node, edges in tree_items:
        cur_edges = sorted(edges.items())
        for to_node, edge_len in cur_edges:
            print(f'{from_node}->{to_node}:{edge_len}')


if __name__ == '__main__':
    main()
