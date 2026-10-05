"""Repeated strict immediate improvement; standard-library submission."""
import sys


def build_actions(n, d):
    rotations = []
    for r in range(4):
        offsets = []
        for u in range(d):
            for v in range(d):
                p,q = ((u,v), (v,d-1-u), (d-1-u,d-1-v), (d-1-v,u))[r]
                offsets.append(p*n+q)
        rotations.append(offsets)
    return [(tuple(x*n+y+v for v in rotations[r]), (x,y,r))
            for x in range(n-d+1) for y in range(n-d+1) for r in range(4)]


def transition(grid, stamp, indices):
    for j, pos in enumerate(indices):
        stamp[j], grid[pos] = grid[pos], stamp[j]


def solve(n, d, c, k, grid, target, stamp):
    actions = build_actions(n, d)
    operations = []
    for _ in range(k):
        best_gain = 0
        best = None
        for indices, operation in actions:
            gain = 0
            for j, pos in enumerate(indices):
                wanted = target[pos]
                gain += (stamp[j] == wanted) - (grid[pos] == wanted)
            if gain > best_gain:
                best_gain, best = gain, (indices, operation)
        if best is None:
            break
        indices, operation = best
        transition(grid, stamp, indices)
        operations.append(operation)
    return operations


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n,d,c,k = data[:4]
    count = n*n
    operations = solve(n,d,c,k,data[4:4+count],data[4+count:4+2*count],data[4+2*count:])
    print(len(operations))
    for operation in operations:
        print(*operation)


if __name__ == '__main__':
    main()
