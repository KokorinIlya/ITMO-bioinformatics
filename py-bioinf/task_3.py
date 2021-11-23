def get_suffix(p):
    assert len(p) == 2
    return p[0][1:], p[1][1:]


def get_prefix(p):
    assert len(p) == 2
    return p[0][:-1], p[1][:-1]


def read_graph(file_name):
    with open(file_name, "r") as file:
        nodes = set()
        edges = {}

        k, d = map(int, file.readline().split())

        n = 0
        for line in map(lambda s: s.strip(), file):
            n += 1
            parts = line.split('|')
            assert len(parts) == 2 and len(parts[0]) == k and len(parts[1]) == k

            pref = get_prefix(parts)
            suf = get_suffix(parts)
            nodes.add(pref)
            nodes.add(suf)

            if pref not in edges:
                edges[pref] = []
            edges[pref].append(suf)

        return nodes, edges, n, k, d


def get_degrees(nodes, edges):
    in_deg = {}
    out_deg = {}
    for cur_node in nodes:
        in_deg[cur_node] = 0
        out_deg[cur_node] = 0

    for v, us in edges.items():
        for u in us:
            assert u in in_deg and u in out_deg and \
                   v in in_deg and v in out_deg
            out_deg[v] += 1
            in_deg[u] += 1

    return in_deg, out_deg


def get_start_node(nodes, in_deg, out_deg):
    for v in nodes:
        assert v in in_deg and v in out_deg
        cur_in_deg = in_deg[v]
        cur_out_deg = out_deg[v]
        if cur_out_deg > cur_in_deg:
            return v
    return next(iter(nodes))


def traverse_graph(edges, start_node):
    traverse_stack = []
    path = []
    traverse_stack.append(start_node)
    while len(traverse_stack) > 0:
        v = traverse_stack[-1]
        if v in edges and len(edges[v]) > 0:
            u = edges[v].pop()
            traverse_stack.append(u)
        else:
            path.append(v)
            traverse_stack.pop()
    return path[::-1]


def assemble_genome(path, d):
    result = [path[0][0]]
    for kmer_1, _ in path[1:d + 2]:
        result.append(kmer_1[-1])
    result.append(path[0][1])
    for _, kmer_2 in path[1:]:
        result.append(kmer_2[-1])
    return ''.join(result)


def main():
    nodes, edges, n, k, d = read_graph("rosalind_ba3j.txt")
    in_deg, out_deg = get_degrees(nodes, edges)
    start_node = get_start_node(nodes, in_deg, out_deg)
    path = traverse_graph(edges, start_node)
    genome = assemble_genome(path, d)
    assert len(genome) == 2 * k + d + n - 1
    print(genome)


if __name__ == '__main__':
    main()
