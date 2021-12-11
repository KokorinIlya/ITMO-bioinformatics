from typing import TextIO, Optional
import math


# noinspection DuplicatedCode
def parse_transition_matrix(file: TextIO, all_states: set):
    states = file.readline().strip().split()
    assert set(states) == all_states
    cur_states_set = set()
    result = {}
    for _ in range(len(states)):
        cur_parts = file.readline().strip().split()
        cur_state = cur_parts[0]
        cur_transitions = [float(x) for x in cur_parts[1:]]
        assert math.isclose(sum(cur_transitions), 1., abs_tol=1e-2)

        assert cur_state not in cur_states_set
        assert cur_state in all_states
        cur_states_set.add(cur_state)

        assert len(cur_transitions) == len(states)
        for cur_prob, to_state in zip(cur_transitions, states):
            assert (cur_state, to_state) not in result
            result[(cur_state, to_state)] = cur_prob

    assert cur_states_set == all_states
    return result


# noinspection DuplicatedCode
def parse_emission_matrix(file: TextIO, all_states: set, all_observation: set):
    observations = file.readline().strip().split()
    assert set(observations) == all_observation
    cur_states_set = set()
    result = {}
    for _ in range(len(all_states)):
        cur_parts = file.readline().strip().split()
        cur_state = cur_parts[0]
        cur_emissions = [float(x) for x in cur_parts[1:]]
        assert math.isclose(sum(cur_emissions), 1., abs_tol=1e-2)

        assert cur_state not in cur_states_set
        assert cur_state in all_states
        cur_states_set.add(cur_state)

        assert len(cur_emissions) == len(observations)
        for cur_prob, observation in zip(cur_emissions, observations):
            assert (cur_state, observation) not in result
            result[(cur_state, observation)] = cur_prob

    assert cur_states_set == all_states
    return result


# noinspection DuplicatedCode
def parse_file(file_name):
    with open(file_name, 'r') as file:
        observations = file.readline().strip()
        file.readline()
        all_observation = set(file.readline().strip().split())
        file.readline()
        all_states = file.readline().strip().split()
        all_states_set = set(all_states)
        file.readline()
        transition_matrix = parse_transition_matrix(file, all_states_set)
        file.readline()
        emission_matrix = parse_emission_matrix(file, all_states_set, all_observation)
        return observations, transition_matrix, emission_matrix, all_states


def viterbi_forward(observations: str, states: list,
                    initial_distribution: list,
                    transition_matrix: dict, emission_matrix: dict):
    probs = [
        [
            0. for _ in range(len(states))
        ]
        for _ in range(len(observations))
    ]
    paths = [
        [
            -1 for _ in range(len(states))
        ]
        for _ in range(len(observations))
    ]
    for j in range(len(states)):
        cur_state = states[j]
        first_observation = observations[0]
        assert (cur_state, first_observation) in emission_matrix
        emission_p = emission_matrix[(cur_state, first_observation)]
        probs[0][j] = initial_distribution[j] * emission_p

    for i in range(1, len(observations)):
        for j in range(len(states)):
            cur_state = states[j]
            cur_observation = observations[i]
            assert (cur_state, cur_observation) in emission_matrix
            emission_p = emission_matrix[(cur_state, cur_observation)]

            max_prob = -1.
            best_prev_state_idx: Optional[int] = None
            for k in range(len(states)):
                prev_state = states[k]
                assert (prev_state, cur_state) in transition_matrix
                transition_p = transition_matrix[(prev_state, cur_state)]

                cur_prob = probs[i - 1][k] * transition_p * emission_p
                if max_prob is None or cur_prob > max_prob:
                    max_prob = cur_prob
                    best_prev_state_idx = k

            assert max_prob >= 0. and best_prev_state_idx is not None
            probs[i][j] = max_prob
            paths[i][j] = best_prev_state_idx

    return probs, paths


def viterbi_backward(states, probs, paths):
    max_start_p = -1.
    best_start_idx = None
    for j in range(len(states)):
        cur_p = probs[-1][j]
        if cur_p > max_start_p:
            max_start_p = cur_p
            best_start_idx = j
    assert best_start_idx is not None and max_start_p >= 0.

    result = [states[best_start_idx]]

    cur_state_idx = best_start_idx
    cur_i = len(probs) - 1
    while cur_i >= 0:
        assert cur_state_idx >= 0
        cur_state_idx = paths[cur_i][cur_state_idx]
        cur_i -= 1
        if cur_state_idx >= 0:
            result.append(states[cur_state_idx])
    assert cur_i == -1 and cur_state_idx == -1
    return result[::-1]


def main():
    observations, transition_matrix, emission_matrix, states = parse_file('rosalind_ba10c.txt')
    initial_distribution = [1. / len(states) for _ in states]
    probs, paths = viterbi_forward(observations, states,
                                   initial_distribution,
                                   transition_matrix, emission_matrix)
    best_path = viterbi_backward(states, probs, paths)
    print(''.join(best_path))


if __name__ == '__main__':
    main()
