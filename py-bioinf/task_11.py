import math
from typing import TextIO


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


def parse_file(file_name):
    with open(file_name, 'r') as file:
        iters = int(file.readline().strip())
        file.readline()
        observations = file.readline().strip()
        file.readline()
        all_observations = file.readline().strip().split()
        file.readline()
        all_states = file.readline().strip().split()
        all_states_set = set(all_states)
        file.readline()
        transition_matrix = parse_transition_matrix(file, all_states_set)
        file.readline()
        emission_matrix = parse_emission_matrix(file, all_states_set, set(all_observations))
        return iters, observations, transition_matrix, emission_matrix, all_states, all_observations


def calc_forward(observations: str, states: list,
                 transitions: dict, emissions: dict, initial_distribution: list):
    forward = [
        [0. for _ in range(len(states))]
        for _ in range(len(observations))
    ]
    for cur_state_idx, cur_state in enumerate(states):
        first_observed = observations[0]
        assert (cur_state, first_observed) in emissions
        forward[0][cur_state_idx] = initial_distribution[cur_state_idx] * emissions[(cur_state, first_observed)]

    for i in range(1, len(observations)):
        cur_observed = observations[i]
        for cur_state_idx, cur_state in enumerate(states):
            assert (cur_state, cur_observed) in emissions
            emission_prob = emissions[(cur_state, cur_observed)]

            for prev_state_idx, prev_state in enumerate(states):
                assert (prev_state, cur_state) in transitions
                forward[i][cur_state_idx] += forward[i - 1][prev_state_idx] * transitions[(prev_state, cur_state)]
            forward[i][cur_state_idx] *= emission_prob

    obs_prob = 0.
    for cur_state_idx in range(len(states)):
        obs_prob += forward[-1][cur_state_idx]
    return forward, obs_prob


def calc_backward(observations: str, states: list,
                  transitions: dict, emissions: dict, initial_distribution: list):
    backward = [
        [0. for _ in range(len(states))]
        for _ in range(len(observations))
    ]
    for cur_state_idx in range(len(states)):
        backward[-1][cur_state_idx] = 1.

    for i in range(len(observations) - 2, -1, -1):
        next_observation = observations[i + 1]
        for cur_state_idx, cur_state in enumerate(states):
            for next_state_idx, next_state in enumerate(states):
                assert (cur_state, next_state) in transitions
                assert (next_state, next_observation) in emissions
                backward[i][cur_state_idx] += backward[i + 1][next_state_idx] * \
                                              transitions[(cur_state, next_state)] * \
                                              emissions[(next_state, next_observation)]

    obs_prob = 0.
    for first_state_idx, first_state in enumerate(states):
        first_observation = observations[0]
        assert (first_state, first_observation) in emissions
        obs_prob += backward[0][first_state_idx] * \
                    initial_distribution[first_state_idx] * \
                    emissions[(first_state, first_observation)]
    return backward, obs_prob


def normalize_transitions(transitions: dict, states: list):
    for cur_state in states:
        cur_sum = 0.
        for next_state in states:
            assert (cur_state, next_state) in transitions
            cur_sum += transitions[(cur_state, next_state)]
        for next_state in states:
            transitions[(cur_state, next_state)] /= cur_sum


def normalize_emissions(emissions: dict, states: list, all_observations: list):
    for state in states:
        cur_sum = 0.
        for observation in all_observations:
            assert (state, observation) in emissions
            cur_sum += emissions[(state, observation)]
        for observation in all_observations:
            emissions[(state, observation)] /= cur_sum


def learn(iterations: int, observations: str, states: list, all_observations: list,
          transitions: dict, emissions: dict, initial_distribution: list):
    cur_transitions = transitions
    cur_emissions = emissions

    for _ in range(iterations):
        next_transitions = {}
        next_emissions = {}

        forward, obs_prob_f = calc_forward(observations, states,
                                           cur_transitions, cur_emissions, initial_distribution)
        backward, obs_prob_b = calc_backward(observations, states,
                                             cur_transitions, cur_emissions, initial_distribution)
        assert math.isclose(obs_prob_b, obs_prob_f)

        for cur_state_idx, cur_state in enumerate(states):
            for next_state_idx, next_state in enumerate(states):
                assert (cur_state, next_state) in cur_transitions
                next_transitions[(cur_state, next_state)] = 0.

                for i in range(len(observations) - 1):
                    next_observation = observations[i + 1]
                    assert (next_state, next_observation) in cur_emissions
                    next_transitions[(cur_state, next_state)] += forward[i][cur_state_idx] * \
                                                                 cur_emissions[(next_state, next_observation)] * \
                                                                 backward[i + 1][next_state_idx]
                next_transitions[(cur_state, next_state)] *= \
                    cur_transitions[(cur_state, next_state)] / obs_prob_f

        for cur_state_idx, cur_state in enumerate(states):
            for cur_observation in all_observations:
                assert (cur_state, cur_observation) in cur_emissions
                next_emissions[(cur_state, cur_observation)] = 0.

                for i in range(len(observations)):
                    if observations[i] != cur_observation:
                        continue
                    next_emissions[(cur_state, cur_observation)] += forward[i][cur_state_idx] * \
                                                                    backward[i][cur_state_idx]
                next_emissions[(cur_state, cur_observation)] /= obs_prob_f

        normalize_transitions(next_transitions, states)
        normalize_emissions(next_emissions, states, all_observations)
        cur_emissions = next_emissions
        cur_transitions = next_transitions

    return cur_transitions, cur_emissions


def print_transitions(transitions, states):
    states_string = '\t'.join(states)
    print(f'{states_string}')
    for cur_state in states:
        print(f'{cur_state}\t', end='')
        for other_state in states:
            print("%.3f\t" % transitions[(cur_state, other_state)], end='')
        print()


def print_emissions(emissions, states, all_observations):
    obs_string = '\t'.join(all_observations)
    print(f'\t{obs_string}')
    for cur_state in states:
        print(f'{cur_state}\t', end='')
        for observation in all_observations:
            print("%.3f\t" % emissions[(cur_state, observation)], end='')
        print()


def main():
    iters, observations, transition_matrix, emission_matrix, states, all_observations = \
        parse_file('rosalind_ba10k.txt')
    initial_distribution = [1. / len(states) for _ in states]
    res_transitions, res_emissions = learn(iters, observations, states, all_observations,
                                           transition_matrix, emission_matrix, initial_distribution)
    print_transitions(res_transitions, states)
    print('--------')
    print_emissions(res_emissions, states, all_observations)


if __name__ == '__main__':
    main()
