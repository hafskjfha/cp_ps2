"""Self-contained deterministic sequence simulated annealing solver.

Only standard-library imports are needed on the judge. Offline Optuna changes
DEFAULT_PARAMS and DEFAULT_SEED when exporting a submission; Optuna itself is
never imported here. Temperatures are measured in matching grid cells. Search
uses an iteration budget, so a fixed input, seed and parameters reproduce the
same answer. Benchmark exported parameters against the contest time limit.
"""

import math
import random
import sys


DEFAULT_SEED = 0
DEFAULT_PARAMS = {
    'iterations': 3000,
    'start_temp': 2.0,
    'end_temp': 0.05,
    'replace_weight': 4.0,
    'insert_weight': 1.0,
    'delete_weight': 1.0,
    'swap_weight': 1.0,
    'local_probability': 0.75,
    'local_radius': 2,
    'tail_bias': 2.0,
}


def normalize_params(params=None):
    """Reject misspellings/nonfinite values instead of silently mistuning."""
    result = DEFAULT_PARAMS.copy()
    if params:
        unknown = set(params) - set(result)
        if unknown:
            raise ValueError('unknown parameters: ' + ', '.join(sorted(unknown)))
        result.update(params)
    for key, value in result.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(key + ' must be numeric')
        if not math.isfinite(value):
            raise ValueError(key + ' must be finite')
    for key, lower, upper in (('iterations', 0, 20000), ('local_radius', 1, 30)):
        value = result[key]
        if int(value) != value or not lower <= value <= upper:
            raise ValueError(f'{key} must be an integer in [{lower}, {upper}]')
        result[key] = int(value)
    if not 0 < result['end_temp'] <= result['start_temp']:
        raise ValueError('need 0 < end_temp <= start_temp')
    if not 0 <= result['local_probability'] <= 1:
        raise ValueError('local_probability must be in [0, 1]')
    if not 0.25 <= result['tail_bias'] <= 8:
        raise ValueError('tail_bias must be in [0.25, 8]')
    weights = [result[name + '_weight']
               for name in ('replace', 'insert', 'delete', 'swap')]
    if min(weights) < 0 or sum(weights) <= 0:
        raise ValueError('mutation weights must be nonnegative with positive sum')
    return result


class Model:
    """Flattened grid model; contacts are in stamp REFERENCE cell order."""

    def __init__(self, data):
        values = list(map(int, data.split()))
        self.n, self.d, self.c, self.k = values[:4]
        n, d = self.n, self.d
        self.a = values[4:4+n*n]
        self.t = values[4+n*n:4+2*n*n]
        self.s = values[4+2*n*n:]
        self.width = n-d+1
        self.initial_score = sum(a == t for a, t in zip(self.a, self.t))
        rotations = (
            [(u, v) for u in range(d) for v in range(d)],
            [(v, d-1-u) for u in range(d) for v in range(d)],
            [(d-1-u, d-1-v) for u in range(d) for v in range(d)],
            [(d-1-v, u) for u in range(d) for v in range(d)],
        )
        self.contacts = [tuple((x+p)*n+y+q for p, q in offsets)
                         for x in range(self.width)
                         for y in range(self.width)
                         for offsets in rotations]

    def encode(self, operation):
        x, y, rotation = operation
        return 4*(x*self.width+y)+rotation

    def decode(self, move):
        return move//4//self.width, move//4 % self.width, move % 4

    def replay(self, sequence, states=None, start=0, keep_states=False):
        """Exactly replay the changed suffix, optionally caching its prefixes.

        states[i] is the state BEFORE operation i. A proposal may reuse those
        states only when its operations before start are unchanged.
        """
        if states is None:
            grid, stamp, score = self.a.copy(), self.s.copy(), self.initial_score
            start = 0
            prefix_states = [(grid.copy(), stamp.copy(), score)] if keep_states else None
        else:
            old_grid, old_stamp, score = states[start]
            grid, stamp = old_grid.copy(), old_stamp.copy()
            prefix_states = states[:start+1] if keep_states else None
        target, contacts = self.t, self.contacts
        for move in sequence[start:]:
            for index, position in enumerate(contacts[move]):
                old, new = grid[position], stamp[index]
                score += (new == target[position]) - (old == target[position])
                grid[position], stamp[index] = new, old
            if keep_states:
                prefix_states.append((grid.copy(), stamp.copy(), score))
        return score, grid, stamp, prefix_states

    def greedy(self):
        """Positive immediate gain warm start, with zero moves always legal."""
        grid, stamp = self.a.copy(), self.s.copy()
        target, contacts = self.t, self.contacts
        sequence = []
        for _ in range(self.k):
            best_move, best_gain = -1, 0
            for move, positions in enumerate(contacts):
                gain = 0
                for index, position in enumerate(positions):
                    wanted = target[position]
                    gain += (stamp[index] == wanted) - (grid[position] == wanted)
                if gain > best_gain:
                    best_move, best_gain = move, gain
            if best_move < 0:
                break
            for index, position in enumerate(contacts[best_move]):
                grid[position], stamp[index] = stamp[index], grid[position]
            sequence.append(best_move)
        return sequence


def mutate(sequence, model, rng, params):
    """Return a legal replacement/insertion/deletion/order-swap and first edit.

    Larger tail_bias concentrates edits toward the end, making fewer later
    swaps depend on the edit. A replacement may alter its placement locally,
    or jump to any legal placement; stamp rotation can always change.
    """
    length = len(sequence)
    candidate = sequence.copy()
    if not length:
        return [rng.randrange(len(model.contacts))], 0
    weights = [params[name + '_weight']
               for name in ('replace', 'insert', 'delete', 'swap')]
    if length >= model.k:
        weights[1] = 0.0
    if length < 2:
        weights[3] = 0.0
    total = sum(weights)
    if total == 0:
        # E.g. insertion-only search already at K; keep the chain movable.
        kind = 0
    else:
        sample = rng.random()*total
        kind = 3
        for index, weight in enumerate(weights):
            sample -= weight
            if sample < 0:
                kind = index
                break
    position_count = length+1 if kind == 1 else length
    first = position_count-1-int(position_count*rng.random()**params['tail_bias'])
    first = max(0, first)
    if kind == 2:
        del candidate[first]
    elif kind == 3:
        second = rng.randrange(length-1)
        if second >= first:
            second += 1
        candidate[first], candidate[second] = candidate[second], candidate[first]
        first = min(first, second)
    else:
        if rng.random() < params['local_probability']:
            anchor = sequence[min(first, length-1)]
            x, y, _ = model.decode(anchor)
            radius = params['local_radius']
            x = rng.randint(max(0, x-radius), min(model.width-1, x+radius))
            y = rng.randint(max(0, y-radius), min(model.width-1, y+radius))
            new_move = model.encode((x, y, rng.randrange(4)))
        else:
            new_move = rng.randrange(len(model.contacts))
        if kind == 0:
            candidate[first] = new_move
        else:
            candidate.insert(first, new_move)
    return candidate, first


def solve(data: bytes, params: dict | None = None, seed: int = 0):
    """Greedy construction followed by SA; return the best visited sequence."""
    params = normalize_params(params)
    model = Model(data)
    current = model.greedy()
    current_score, _, _, states = model.replay(current, keep_states=True)
    best, best_score = current.copy(), current_score
    iterations = params['iterations']
    if iterations == 0 or best_score == model.n*model.n:
        return [model.decode(move) for move in best]
    rng = random.Random(seed)
    temperature = params['start_temp']
    decay = math.exp((math.log(params['end_temp']) - math.log(temperature)) /
                     max(1, iterations-1))
    for _ in range(iterations):
        proposal, first = mutate(current, model, rng, params)
        score, _, _, _ = model.replay(proposal, states=states, start=first)
        delta = score-current_score
        if delta >= 0 or rng.random() < math.exp(delta/temperature):
            # Copies for accepted prefixes only; rejected proposals never
            # mutate the cached current state or the retained best answer.
            current_score, _, _, states = model.replay(
                proposal, states=states, start=first, keep_states=True)
            current = proposal
            if score > best_score or (score == best_score and len(current) < len(best)):
                best, best_score = current.copy(), score
                if best_score == model.n*model.n:
                    break
        temperature *= decay
    return [model.decode(move) for move in best]


def format_answer(operations):
    return str(len(operations)) + '\n' + ''.join(
        f'{x} {y} {rotation}\n' for x, y, rotation in operations)


def main():
    data = sys.stdin.buffer.read()
    sys.stdout.write(format_answer(solve(data, seed=DEFAULT_SEED)))


if __name__ == '__main__':
    main()
