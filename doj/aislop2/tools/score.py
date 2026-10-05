"""Exact official score from the canonical simulator."""

import argparse
import json
from pathlib import Path
import sys

if __package__:
    from .simulate import Instance, match_count, parse_instance, simulate
    from .validate_output import validate_output
else:
    from simulate import Instance, match_count, parse_instance, simulate
    from validate_output import validate_output


def score(instance: Instance, operations) -> dict[str, int]:
    grid, _stamp = simulate(instance, operations)
    matches = match_count(instance, grid)
    cells = instance.n * instance.n
    return {'matches': matches, 'total_cells': cells,
            'score': (1_000_000 * matches) // cells}


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
        result = score(instance, operations)
    except (OSError, ValueError) as exc:
        parser.exit(2, f'invalid: {exc}\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
