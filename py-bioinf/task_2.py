import random


def gen_random_motif(dna, k):
    assert len(dna) >= k
    start_idx = random.randint(0, len(dna) - k)
    result = dna[start_idx:start_idx + k]
    assert len(result) == k
    return result


def get_counts(motifs):
    assert len(motifs) > 0
    k = len(motifs[0])
    assert len(
        set(
            len(cur_motif) for cur_motif in motifs
        )
    ) == 1

    result = {  # (number of symbol [A, T, G, C] occurrences at position #i) + 1
        'A': [1 for _ in range(k)],
        'T': [1 for _ in range(k)],
        'G': [1 for _ in range(k)],
        'C': [1 for _ in range(k)]
    }
    for cur_motif in motifs:
        assert len(cur_motif) == k
        for i in range(k):
            cur_c = cur_motif[i]
            result[cur_c][i] += 1
    return result


def estimate_prob(motif, counts):
    for c in ('A', 'T', 'G', 'C'):
        assert len(motif) == len(counts[c])

    res = 1
    for i in range(len(motif)):
        cur_c = motif[i]
        res *= counts[cur_c][i]
    return res


def get_most_probable_kmer(dna, k, counts):
    assert len(dna) >= k
    max_prob = -1.
    result = None
    for start_idx in range(len(dna) - k + 1):
        cur_kmer = dna[start_idx:start_idx + k]
        assert len(cur_kmer) == k
        cur_prob = estimate_prob(cur_kmer, counts)
        if cur_prob > max_prob:
            max_prob = cur_prob
            result = cur_kmer
    assert result is not None and max_prob > 0.
    return result


def get_most_probable_letter(counts, pos, k):
    assert 0 <= pos < k
    max_count = -1
    result = None
    for c in ('A', 'T', 'G', 'C'):
        cur_count = counts[c][pos]
        if cur_count > max_count:
            max_count = cur_count
            result = c
    assert result is not None and max_count > 0
    return result


def score(motifs):
    assert len(motifs) > 0
    k = len(motifs[0])
    assert len(
        set(
            len(cur_motif) for cur_motif in motifs
        )
    ) == 1

    result = 0
    counts = get_counts(motifs)
    consensus = [get_most_probable_letter(counts, pos, k) for pos in range(k)]

    for cur_motif in motifs:
        for pos in range(k):
            if cur_motif[pos] != consensus[pos]:
                result += 1
    return result


def randomized_motif_search(dnas, k):
    cur_motifs = [gen_random_motif(cur_dna, k) for cur_dna in dnas]
    best_motifs = cur_motifs
    min_score = score(best_motifs)

    while True:
        counts = get_counts(cur_motifs)
        cur_motifs = [get_most_probable_kmer(cur_dna, k, counts) for cur_dna in dnas]
        cur_score = score(cur_motifs)
        if cur_score < min_score:
            min_score = cur_score
            best_motifs = cur_motifs
        else:
            return best_motifs, min_score


def main():
    with open("rosalind_ba2f.txt", "r") as file:
        k, t = map(int, file.readline().split())
        dnas = [cur_line.strip() for cur_line in file.readlines()]

        best_motif = None
        min_score = None
        for _ in range(1000):
            cur_motif, cur_score = randomized_motif_search(dnas, k)
            if min_score is None or cur_score < min_score:
                min_score = cur_score
                best_motif = cur_motif

        assert best_motif is not None and min_score is not None
        print('\n'.join(best_motif))


if __name__ == '__main__':
    main()
