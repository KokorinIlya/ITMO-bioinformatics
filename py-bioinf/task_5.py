def get_lines(file_name):
    with open(file_name, 'r') as file:
        return [cur_line.strip() for cur_line in file.readlines()]


def parse(line: str):
    parts = line.split(')')
    result = []
    for cur_part in parts:
        if cur_part.strip() == '':
            continue
        assert cur_part.startswith('(')
        cur_part = cur_part[1:]
        result.append(
            [int(x) for x in cur_part.split()]
        )
    return result


def chromosome_to_cycle(chromosome):
    result = []
    for x in chromosome:
        assert x != 0
        if x > 0:
            node_from = 2 * x - 1
            node_to = 2 * x
        else:
            x = abs(x)
            node_from = 2 * x
            node_to = 2 * x - 1
        result.append(node_from)
        result.append(node_to)
    return result


def genome_to_cycle(genome):
    result = {}
    for cur_chromosome in genome:
        cur_cycle = chromosome_to_cycle(cur_chromosome)
        assert len(cur_cycle) >= 2 and len(cur_cycle) % 2 == 0

        v = cur_cycle[0]
        u = cur_cycle[-1]
        assert v not in result and u not in result
        result[v] = u
        result[u] = v

        for i in range(len(cur_cycle) // 2 - 1):
            v = cur_cycle[2 * i + 1]
            u = cur_cycle[2 * i + 2]
            assert v not in result and u not in result
            result[v] = u
            result[u] = v

    return result


def cycle_to_genome(cycles: dict, not_visited: set, start_node):
    cur_node = start_node
    result = []

    while True:
        assert cur_node not in not_visited

        if cur_node % 2 == 0:
            other_node = cur_node - 1
            cur_gene = -cur_node // 2
        else:
            other_node = cur_node + 1
            cur_gene = other_node // 2

        result.append(cur_gene)
        assert other_node in not_visited
        not_visited.remove(other_node)

        assert other_node in cycles
        new_node = cycles[other_node]
        if new_node in not_visited:
            not_visited.remove(new_node)
            cur_node = new_node
        else:
            return result


def cycles_to_genome(cycles: dict):
    not_visited = {
        node for node in cycles.keys()
    }
    result = []
    while len(not_visited) > 0:
        start_node = not_visited.pop()
        cur_chromosome = cycle_to_genome(cycles, not_visited, start_node)
        result.append(cur_chromosome)
    return result


def modify_cur_cycles(cur_cycles: dict, final_cycles: dict):
    assert cur_cycles.keys() == final_cycles.keys()
    not_visited = {
        node for node in cur_cycles.keys()
    }
    while len(not_visited) > 0:
        a = not_visited.pop()

        assert a in cur_cycles
        b = cur_cycles[a]
        assert b in not_visited
        not_visited.remove(b)

        assert b in final_cycles
        c = final_cycles[b]
        if c not in not_visited:
            assert c == a
            continue
        not_visited.remove(c)

        assert c in cur_cycles
        d = cur_cycles[c]
        assert d in not_visited
        not_visited.remove(d)

        assert cur_cycles[a] == b and cur_cycles[b] == a and \
               cur_cycles[c] == d and cur_cycles[d] == c

        cur_cycles[b] = c
        cur_cycles[c] = b

        cur_cycles[a] = d
        cur_cycles[d] = a
        return True

    return False


def block_to_string(block):
    assert block != 0
    if block < 0:
        return str(block)
    else:
        return f'+{block}'


def genome_to_string(genome):
    chromosome_strings = []
    for cur_chromosome in genome:
        cur_str = '(' + ' '.join(map(block_to_string, cur_chromosome)) + ')'
        chromosome_strings.append(cur_str)
    return ''.join(chromosome_strings)


def main():
    start_line, final_line = get_lines('rosalind_ba6d.txt')
    print(start_line)

    start_genome = parse(start_line)
    final_genome = parse(final_line)

    start_cycle = genome_to_cycle(start_genome)
    final_cycle = genome_to_cycle(final_genome)

    while modify_cur_cycles(start_cycle, final_cycle):
        cur_genome = cycles_to_genome(start_cycle)
        print(genome_to_string(cur_genome))


if __name__ == '__main__':
    main()
