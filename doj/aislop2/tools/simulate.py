"""Canonical reference model for the stamp-swap problem (standard library only)."""

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys


@dataclass
class Instance:
    n: int
    d: int
    c: int
    k: int
    a: list[int]
    t: list[int]
    s: list[int]


_INTEGER = re.compile(r'[+-]?[0-9]+', re.ASCII)


def parse_instance(text: str) -> Instance:
    """Parse exactly one instance, rejecting malformed data and illegal bounds."""
    if not isinstance(text, str):
        raise ValueError('instance text must be a string')
    try:
        text.encode('ascii')
    except UnicodeEncodeError as exc:
        raise ValueError('instance must contain ASCII text') from exc
    tokens = text.split()
    if len(tokens) < 4:
        raise ValueError('instance needs the N D C K header')
    if any(_INTEGER.fullmatch(token) is None for token in tokens):
        raise ValueError('instance contains a non-integer token')
    try:
        numbers = [int(token) for token in tokens]
    except ValueError as exc:
        raise ValueError('instance integer cannot be parsed') from exc
    n, d, c, k = numbers[:4]
    if not 3 <= n <= 30:
        raise ValueError('N must be in [3, 30]')
    if d not in (2, 3) or d > n:
        raise ValueError('D must be 2 or 3 and no larger than N')
    if not 2 <= c <= 6:
        raise ValueError('C must be in [2, 6]')
    if not 1 <= k <= 180:
        raise ValueError('K must be in [1, 180]')
    expected = 4 + 2*n*n + d*d
    if len(numbers) != expected:
        raise ValueError(f'instance has {len(numbers)} tokens; expected {expected}')
    if any(not 0 <= color < c for color in numbers[4:]):
        raise ValueError('color must be in [0, C)')
    size = n*n
    return Instance(n, d, c, k, numbers[4:4+size],
                    numbers[4+size:4+2*size], numbers[4+2*size:])


def format_instance(instance: Instance) -> str:
    """Write the statement's row-oriented input format."""
    lines = [f'{instance.n} {instance.d} {instance.c} {instance.k}']
    for values, width in [(instance.a, instance.n), (instance.t, instance.n),
                          (instance.s, instance.d)]:
        lines.extend(' '.join(map(str, values[i:i+width]))
                     for i in range(0, len(values), width))
    return '\n'.join(lines) + '\n'


def rotation_offsets(d: int, r: int) -> list[tuple[int, int]]:
    """Grid offsets contacted by stamp cells in REFERENCE row-major order."""
    if d not in (2, 3) or type(r) is not int or not 0 <= r <= 3:
        raise ValueError('invalid stamp dimension or rotation')
    if r == 0:
        return [(u, v) for u in range(d) for v in range(d)]
    if r == 1:
        return [(v, d-1-u) for u in range(d) for v in range(d)]
    if r == 2:
        return [(d-1-u, d-1-v) for u in range(d) for v in range(d)]
    return [(d-1-v, u) for u in range(d) for v in range(d)]


def simulate(instance: Instance, operations) -> tuple[list[int], list[int]]:
    """Return copied final grid and reference-oriented stamp; reject illegal moves."""
    operations = list(operations)
    if len(operations) > instance.k:
        raise ValueError(f'{len(operations)} operations exceed K={instance.k}')
    n, d = instance.n, instance.d
    rotations = [rotation_offsets(d, r) for r in range(4)]
    grid, stamp = instance.a.copy(), instance.s.copy()
    for step, operation in enumerate(operations):
        if not isinstance(operation, (list, tuple)) or len(operation) != 3:
            raise ValueError(f'operation {step} must contain three integers')
        if any(type(value) is not int for value in operation):
            raise ValueError(f'operation {step} must contain three integers')
        x, y, r = operation
        if not 0 <= x <= n-d or not 0 <= y <= n-d or not 0 <= r <= 3:
            raise ValueError(f'operation {step} is out of range: {operation}')
        # Each grid cell and each stamp cell occurs once, making sequential swaps
        # exactly equivalent to the statement's simultaneous contact swaps.
        for index, (p, q) in enumerate(rotations[r]):
            pos = (x+p)*n + y+q
            stamp[index], grid[pos] = grid[pos], stamp[index]
    return grid, stamp


def match_count(instance: Instance, grid: list[int]) -> int:
    if len(grid) != instance.n * instance.n:
        raise ValueError('final grid has the wrong number of cells')
    return sum(color == target for color, target in zip(grid, instance.t))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('instance', type=Path)
    parser.add_argument('output', nargs='?', type=Path,
                        help='solver output; read stdin if omitted')
    args = parser.parse_args()
    if __package__:
        from .validate_output import validate_output
    else:
        from validate_output import validate_output
    try:
        instance = parse_instance(args.instance.read_text(encoding='ascii'))
        answer = args.output.read_bytes() if args.output else sys.stdin.buffer.read()
        operations = validate_output(instance, answer)
        grid, stamp = simulate(instance, operations)
    except (OSError, ValueError) as exc:
        parser.exit(2, f'error: {exc}\n')
    print(json.dumps({'grid': grid, 'stamp': stamp,
                      'matches': match_count(instance, grid)}))


if __name__ == '__main__':
    main()
