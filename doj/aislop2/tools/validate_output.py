"""Strict output validation, before any result is scored."""

import argparse
import json
from pathlib import Path
import re
import sys

if __package__:
    from .simulate import Instance, parse_instance
else:
    from simulate import Instance, parse_instance


MAX_OUTPUT_BYTES = 100_000
_INTEGER = re.compile(rb'[+-]?[0-9]+')


def validate_output(instance: Instance, output: bytes | str) -> list[tuple[int, int, int]]:
    """Validate size, ASCII integer grammar, exact token count and all move bounds."""
    if isinstance(output, str):
        try:
            output = output.encode('ascii')
        except UnicodeEncodeError as exc:
            raise ValueError('output must contain ASCII text') from exc
    if not isinstance(output, bytes):
        raise ValueError('output must be bytes or a string')
    if len(output) > MAX_OUTPUT_BYTES:
        raise ValueError(f'output exceeds {MAX_OUTPUT_BYTES} bytes')
    tokens = output.split()
    if not tokens:
        raise ValueError('missing operation count')
    if any(_INTEGER.fullmatch(token) is None for token in tokens):
        raise ValueError('output contains a non-integer token')
    try:
        values = [int(token) for token in tokens]
    except ValueError as exc:
        raise ValueError('output integer cannot be parsed') from exc
    count = values[0]
    if not 0 <= count <= instance.k:
        raise ValueError(f'operation count {count} is outside [0, {instance.k}]')
    expected = 1 + 3*count
    if len(values) != expected:
        raise ValueError(f'output has {len(values)} tokens; expected {expected}')
    operations = []
    for step in range(count):
        x, y, r = values[1+3*step:4+3*step]
        if not 0 <= x <= instance.n-instance.d:
            raise ValueError(f'operation {step}: x={x} is out of range')
        if not 0 <= y <= instance.n-instance.d:
            raise ValueError(f'operation {step}: y={y} is out of range')
        if not 0 <= r <= 3:
            raise ValueError(f'operation {step}: r={r} is out of range')
        operations.append((x, y, r))
    return operations


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('instance', type=Path)
    parser.add_argument('output', nargs='?', type=Path,
                        help='solver output; read stdin if omitted')
    args = parser.parse_args()
    try:
        instance = parse_instance(args.instance.read_text(encoding='ascii'))
        output = args.output.read_bytes() if args.output else sys.stdin.buffer.read()
        operations = validate_output(instance, output)
    except (OSError, ValueError) as exc:
        parser.exit(2, f'invalid: {exc}\n')
    print(json.dumps({'valid': True, 'operations': len(operations)}))


if __name__ == '__main__':
    main()
