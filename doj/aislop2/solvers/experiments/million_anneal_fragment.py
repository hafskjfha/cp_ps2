import random
import math


class GlobalSequence:
    def __init__(self, initial, target, indices, sequence, nn):
        self.nn = nn
        self.indices = indices
        self.sequence = sequence[:]
        self.prefix = [initial[:]]
        for aid in sequence:
            row = self.prefix[-1][:]
            self.swap(row, aid)
            self.prefix.append(row)
        self.wishes = [None] * (len(sequence) + 1)
        self.wishes[-1] = target + [6] * (len(initial) - nn)
        for i in range(len(sequence) - 1, -1, -1):
            row = self.wishes[i + 1][:]
            self.swap(row, sequence[i])
            self.wishes[i] = row
        self.score = sum(a == b for a, b in zip(self.prefix[-1], target))

    def swap(self, row, aid):
        if aid >= 0:
            for j, p in enumerate(self.indices[aid]):
                row[p], row[self.nn + j] = row[self.nn + j], row[p]

    def propagate(self, changed, aid):
        if aid >= 0:
            nn = self.nn
            for j, p in enumerate(self.indices[aid]):
                a = changed.pop(p, None)
                b = changed.pop(nn + j, None)
                if a is not None:
                    changed[nn + j] = a
                if b is not None:
                    changed[p] = b

    def trial(self, left, candidate):
        row = self.prefix[left][:]
        touched = set(range(self.nn, len(row)))
        for old, new in zip(self.sequence[left:left + len(candidate)], candidate):
            if old >= 0:
                touched.update(self.indices[old])
            if new >= 0:
                touched.update(self.indices[new])
                self.swap(row, new)
        right = left + len(candidate)
        old = self.prefix[right]
        wishes = self.wishes[right]
        changed = {p: row[p] for p in touched if row[p] != old[p]}
        gain = sum((v == wishes[p]) - (old[p] == wishes[p]) for p, v in changed.items())
        return gain, changed

    def accept(self, left, candidate, gain, changed):
        right = left + len(candidate)
        self.sequence[left:right] = candidate
        for i in range(left, right):
            row = self.prefix[i][:]
            self.swap(row, self.sequence[i])
            self.prefix[i + 1] = row
        for i in range(right, len(self.sequence)):
            self.propagate(changed, self.sequence[i])
            row = self.prefix[i + 1]
            for p, v in changed.items():
                row[p] = v
        old = self.wishes[left]
        for i in range(right - 1, left - 1, -1):
            row = self.wishes[i + 1][:]
            self.swap(row, self.sequence[i])
            self.wishes[i] = row
        changed = {p: v for p, v in enumerate(self.wishes[left]) if v != old[p]}
        for i in range(left - 1, -1, -1):
            self.propagate(changed, self.sequence[i])
            row = self.wishes[i]
            for p, v in changed.items():
                row[p] = v
        self.score += gain


def global_anneal(n, d, c, k, initial, target, indices, sequence,
                  proposals=20000, temperature=0.45, seed_offset=0):
    if k < 3:
        return sequence
    upper = sum(min(initial.count(v), target.count(v)) for v in range(c))
    nn = n * n
    padded = sequence + [-1] * min(12, k - len(sequence))
    state = GlobalSequence(initial, target, indices, padded, nn)
    if state.score == upper:
        return sequence
    rng = random.Random(sum((i + 79) * v for i, v in enumerate(initial)) + k * 1279 + seed_offset)
    length = len(padded)
    if length < 2:
        return sequence
    best, best_score = padded[:], state.score
    side = n - d + 1
    count = len(indices)
    period = max(1, proposals // 4)
    for step in range(proposals):
        if step and step % period == 0:
            state = GlobalSequence(initial, target, indices, best, nn)
        left = rng.randrange(length)
        mode = rng.randrange(20)
        old = state.sequence[left]
        if mode < 13:
            if mode < 5 and old >= 0:
                x, rem = divmod(old, side * 4)
                y, rot = divmod(rem, 4)
                if mode == 0:
                    x = max(0, min(side - 1, x + rng.choice((-2, -1, 1, 2))))
                elif mode == 1:
                    y = max(0, min(side - 1, y + rng.choice((-2, -1, 1, 2))))
                elif mode < 4:
                    x = max(0, min(side - 1, x + rng.choice((-1, 0, 1))))
                    y = max(0, min(side - 1, y + rng.choice((-1, 0, 1))))
                new = (x * side + y) * 4 + rng.randrange(4)
            elif mode == 5:
                new = -1
            else:
                new = rng.randrange(count)
            candidate = [new]
        else:
            if mode < 16:
                right = min(length, left + rng.randrange(2, 7))
            else:
                right = rng.randrange(left + 1, length + 1)
            if right - left < 2:
                continue
            candidate = state.sequence[left:right]
            if mode in (13, 16):
                candidate[0], candidate[-1] = candidate[-1], candidate[0]
            elif mode in (14, 17):
                candidate = candidate[1:] + candidate[:1]
            elif mode == 18:
                rotation = rng.randrange(1, 4)
                candidate = [a // 4 * 4 + (a + rotation) % 4 if a >= 0 else a for a in candidate]
            else:
                candidate.reverse()
        if candidate == state.sequence[left:left + len(candidate)]:
            continue
        gain, changed = state.trial(left, candidate)
        temp = temperature * (1 - (step % period) / period) ** 2 + 0.035
        if gain >= 0 or rng.random() < math.exp(gain / temp):
            state.accept(left, candidate, gain, changed)
            if state.score > best_score:
                best, best_score = state.sequence[:], state.score
                if best_score == upper:
                    break
    return [aid for aid in best if aid >= 0]


def destroy_rebuild(n, d, c, k, initial, target, indices, sequence,
                    refine, actions, trials=16, passes=3, temperature=0.0):
    if k < 4 or not sequence:
        return sequence
    nn = n * n
    upper = sum(min(initial.count(v), target.count(v)) for v in range(c))
    def evaluate(path):
        row = initial[:]
        for aid in path:
            for j, p in enumerate(indices[aid]):
                row[p], row[nn+j] = row[nn+j], row[p]
        return sum(a == b for a, b in zip(row, target))
    current, best = sequence[:], sequence[:]
    score = best_score = evaluate(best)
    if score == upper:
        return best
    rng = random.Random(sum((i + 91) * v for i, v in enumerate(initial)) + k * 2017)
    for trial in range(trials):
        candidate = current + [-1] * min(8, k - len(current))
        number = min(len(candidate), (2, 4, 8, 16)[trial % 4])
        if trial % 3 == 0:
            left = rng.randrange(len(candidate) - number + 1)
            positions = range(left, left + number)
        else:
            positions = rng.sample(range(len(candidate)), number)
        mode = rng.randrange(3)
        for pos in positions:
            candidate[pos] = -1 if mode < 2 else rng.randrange(len(indices))
        candidate = refine(n, d, k, initial, target, actions, candidate,
                           passes=passes, seed_offset=trial * 14291 + 70001)
        value = evaluate(candidate)
        if value > best_score:
            best, best_score = candidate[:], value
            if value == upper:
                break
        if value >= score or temperature and rng.random() < math.exp((value-score)/temperature):
            current, score = candidate, value
        if trial % 8 == 7:
            current, score = best[:], best_score
    return best


def objective_walk(n, d, c, k, initial, target, indices, sequence,
                   refine, weighted_refine, actions, trials=12, mode=0, passes=3):
    if k < 4:
        return sequence
    nn = n * n
    upper = sum(min(initial.count(v), target.count(v)) for v in range(c))
    def evaluate(path):
        row = initial[:]
        for aid in path:
            for j, p in enumerate(indices[aid]):
                row[p], row[nn + j] = row[nn + j], row[p]
        return sum(a == b for a, b in zip(row, target)), row
    best = sequence[:]
    best_score, final = evaluate(best)
    if best_score == upper:
        return best
    current = best[:]
    rng = random.Random(sum((i + 101) * v for i, v in enumerate(initial)) + k * 2381)
    for trial in range(trials):
        if mode == 0:
            rate = (0.08, 0.15, 0.3, 0.5)[trial % 4]
            weights = [1 + (rng.random() < rate) for _ in range(nn)]
        elif mode == 1:
            rate = (0.04, 0.08, 0.15, 0.25)[trial % 4]
            weights = [1 - (rng.random() < rate) for _ in range(nn)]
        elif mode == 2:
            weights = [1] * nn
            x, y = rng.randrange(n), rng.randrange(n)
            radius = (2, 3, 4, 6)[trial % 4]
            for p in range(nn):
                px, py = divmod(p, n)
                if abs(px-x) + abs(py-y) <= radius:
                    weights[p] = 2
        elif mode == 3:
            rate = (0.1, 0.3, 0.6, 1.0)[trial % 4]
            weights = [1 + (a != b and rng.random() < rate) for a, b in zip(final, target)]
        elif mode == 4:
            chosen = trial % c
            weights = [1 + (v == chosen) for v in target]
        else:
            offset = rng.randrange(2 + trial % 4)
            weights = [1 + ((p // n if trial % 2 else p % n) % (2 + trial % 4) == offset)
                       for p in range(nn)]
        candidate = weighted_refine(n, d, k, initial, target, weights, actions, current, passes=1)
        candidate = refine(n, d, k, initial, target, actions, candidate, passes=passes,
                           seed_offset=trial * 17981 + 80311)
        value, row = evaluate(candidate)
        if value >= best_score:
            best, best_score, final = candidate[:], value, row
            if value == upper:
                break
        current = candidate if value >= best_score - 1 else best[:]
        if trial % 4 == 3:
            current = best[:]
    return best
