"""Generate immutable, reproducible stamp-swap benchmark inputs.

Run ``python tools/generate_cases.py`` from any directory. The default writes
320 cases under the repository's cases/generated directory and manifest.json.
The first 20 belong to smoke, the first 100 to dev, and all 320 to stable.
Existing different files are rejected unless --overwrite is explicitly given.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import random
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SEED = 20260925
VERSION = 1
SUITE_COUNTS = {"smoke": 20, "dev": 100, "stable": 320}
FAMILIES = (
    "random", "near_target", "reachable", "checkerboard", "stripes",
    "repeated_stamp", "nearly_uniform", "local_adversarial",
)


def configurations() -> list[dict[str, Any]]:
    """Return the frozen configuration, without consulting benchmark results."""
    rng = random.Random(SEED)
    # Each block covers all families, both stamp sizes, and all color counts.
    combinations = [(f, d, c) for f in FAMILIES for d in (2, 3)
                    for c in range(2, 7)]
    configs = []
    for block in range(4):
        batch = combinations[:]
        rng.shuffle(batch)
        for offset, (family, d, c) in enumerate(batch):
            index = block * len(batch) + offset
            case_seed = SEED * 1_000_003 + index * 104_729
            case_rng = random.Random(case_seed)
            # Rotate through small, medium, and large boards independently of
            # family; preserve plenty of large boards for runtime measurements.
            low, high = ((3, 7), (8, 15), (16, 23), (24, 30))[index % 4]
            n = case_rng.randint(low, high)
            low_k, high_k = ((1, 5), (6, 35), (36, 100), (101, 180))[(index // 4) % 4]
            k = case_rng.randint(low_k, high_k)
            configs.append(dict(id=f"case_{index:03d}", seed=case_seed,
                                family=family, n=n, d=d, c=c, k=k))
    # Smoke always contains the exact size/budget endpoints and every family.
    forced = (
        ("random", 3, 2, 2, 1),
        ("random", 30, 3, 6, 180),
        ("reachable", 3, 3, 6, 180),
        ("near_target", 30, 2, 2, 1),
        ("checkerboard", 9, 2, 2, 60),
        ("checkerboard", 15, 3, 5, 100),
        ("stripes", 17, 2, 3, 90),
        ("stripes", 30, 3, 6, 180),
        ("repeated_stamp", 12, 2, 6, 80),
        ("repeated_stamp", 20, 3, 2, 140),
        ("nearly_uniform", 7, 2, 4, 40),
        ("nearly_uniform", 24, 3, 5, 120),
        ("local_adversarial", 11, 2, 4, 70),
        ("local_adversarial", 28, 3, 6, 180),
        ("reachable", 16, 2, 5, 120),
        ("reachable", 25, 3, 3, 160),
        ("near_target", 8, 3, 6, 10),
        ("near_target", 23, 2, 3, 150),
        ("random", 30, 2, 6, 180),
        ("random", 4, 3, 2, 5),
    )
    for config, (family, n, d, c, k) in zip(configs, forced):
        config.update(family=family, n=n, d=d, c=c, k=k)
    return configs


def apply_operation(grid: list[list[int]], stamp: list[list[int]],
                    operation: tuple[int, int, int]) -> None:
    """Literal reference-orientation swaps for reachable-case construction."""
    x, y, r = operation
    d = len(stamp)
    for u in range(d):
        for v in range(d):
            if r == 0:
                p, q = u, v
            elif r == 1:
                p, q = v, d - 1 - u
            elif r == 2:
                p, q = d - 1 - u, d - 1 - v
            else:
                p, q = d - 1 - v, u
            stamp[u][v], grid[x + p][y + q] = grid[x + p][y + q], stamp[u][v]


def make_case(config: dict[str, Any]) -> dict[str, Any]:
    """Return matrices and (for reachable cases) a legal construction witness."""
    n, d, c, k = (config[key] for key in ("n", "d", "c", "k"))
    family = config["family"]
    rng = random.Random(config["seed"])

    def matrix(size: int) -> list[list[int]]:
        return [[rng.randrange(c) for _ in range(size)] for _ in range(size)]

    a, t, s = matrix(n), matrix(n), matrix(d)
    witness = None
    if family == "near_target":
        t = [row[:] for row in a]
        fraction = rng.choice((0.015, 0.04, 0.10, 0.20))
        for cell in rng.sample(range(n * n), max(1, int(n * n * fraction))):
            x, y = divmod(cell, n)
            t[x][y] = (a[x][y] + rng.randrange(1, c)) % c
    elif family == "reachable":
        t = [row[:] for row in a]
        carried = [row[:] for row in s]
        length = rng.randint(1, k)
        witness = [(rng.randrange(n - d + 1), rng.randrange(n - d + 1),
                    rng.randrange(4)) for _ in range(length)]
        for operation in witness:
            apply_operation(t, carried, operation)
    elif family == "checkerboard":
        colors = rng.sample(range(c), rng.choice((2, c)))
        size = rng.choice((1, 1, 2, 3))
        t = [[colors[(x // size + y // size) % len(colors)]
              for y in range(n)] for x in range(n)]
    elif family == "stripes":
        vertical = rng.randrange(2)
        width = rng.choice((1, 2, 3, 5))
        palette = list(range(c))
        rng.shuffle(palette)
        t = [[palette[((y if vertical else x) // width) % c]
              for y in range(n)] for x in range(n)]
    elif family == "repeated_stamp":
        palette = rng.sample(range(c), rng.choice((1, min(2, c))))
        s = [[rng.choice(palette) for _ in range(d)] for _ in range(d)]
    elif family == "nearly_uniform":
        base = rng.randrange(c)
        a = [[base for _ in range(n)] for _ in range(n)]
        t = [[base for _ in range(n)] for _ in range(n)]
        s = [[base for _ in range(d)] for _ in range(d)]
        for board in (a, t):
            for cell in rng.sample(range(n * n), max(1, n * n // 12)):
                x, y = divmod(cell, n)
                board[x][y] = (base + rng.randrange(1, c)) % c
        for _ in range(rng.randrange(d * d + 1)):
            s[rng.randrange(d)][rng.randrange(d)] = rng.randrange(c)
    elif family == "local_adversarial":
        # Dispersed single-cell mistakes surrounded by correct cells require
        # recovering collateral damage. Add a cluster on alternating seeds.
        t = matrix(n)
        a = [row[:] for row in t]
        spacing = d + 1
        ox, oy = rng.randrange(spacing), rng.randrange(spacing)
        for x in range(ox, n, spacing):
            for y in range(oy, n, spacing):
                a[x][y] = (t[x][y] + rng.randrange(1, c)) % c
        if config["seed"] % 2:
            x, y = rng.randrange(n - d + 1), rng.randrange(n - d + 1)
            for u in range(d):
                for v in range(d):
                    a[x + u][y + v] = (t[x + u][y + v] + 1) % c
    elif family != "random":
        raise ValueError(f"Unknown family: {family}")
    return {**config, "a": a, "t": t, "s": s, "witness": witness}


def serialize_case(case: dict[str, Any]) -> bytes:
    lines = [" ".join(str(case[key]) for key in ("n", "d", "c", "k"))]
    for key in ("a", "t", "s"):
        lines.extend(" ".join(map(str, row)) for row in case[key])
    return ("\n".join(lines) + "\n").encode("ascii")


def build_outputs(output: Path) -> dict[Path, bytes]:
    """Build all bytes before writing, permitting an atomic preflight check."""
    output = output.resolve()
    files = {}
    entries = []
    for index, config in enumerate(configurations()):
        case = make_case(config)
        content = serialize_case(case)
        path = output / "generated" / f"{config['id']}.in"
        try:
            reference = path.relative_to(ROOT).as_posix()
        except ValueError:
            reference = path.as_posix()
        entry = dict(config, path=reference,
                     suites=[suite for suite, count in SUITE_COUNTS.items() if index < count],
                     sha256=hashlib.sha256(content).hexdigest())
        if case["witness"] is not None:
            entry["construction_operations"] = len(case["witness"])
        files[path] = content
        entries.append(entry)
    manifest = {"version": VERSION, "seed": SEED,
                "generator": "tools/generate_cases.py", "suite_counts": SUITE_COUNTS,
                "description": "Frozen nested suites; regenerate only before a new benchmark epoch.",
                "cases": entries}
    files[output / "manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
    return files


def write_outputs(output: Path, overwrite: bool = False) -> dict[str, int]:
    files = build_outputs(output)
    conflicts = [str(path) for path, content in files.items()
                 if path.exists() and path.read_bytes() != content]
    if conflicts and not overwrite:
        raise FileExistsError("Refusing to change frozen benchmark files; use --overwrite "
                              "only to intentionally start a new benchmark epoch: "
                              + ", ".join(conflicts[:5]))
    changed = 0
    for path, content in files.items():
        if path.exists() and path.read_bytes() == content:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        changed += 1
    return {"cases": SUITE_COUNTS["stable"], "written_files": changed,
            "unchanged_files": len(files) - changed}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "cases",
                        help="Output directory (default: repository cases directory)")
    parser.add_argument("--overwrite", action="store_true",
                        help="Explicitly replace different existing benchmark files")
    args = parser.parse_args()
    try:
        summary = write_outputs(args.output, args.overwrite)
    except FileExistsError as error:
        parser.exit(2, str(error) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
