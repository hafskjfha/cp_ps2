"""Profile a solver on a selected case without changing its source."""
import argparse
import cProfile
import io
import pstats
import runpy
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('solver', type=Path)
    parser.add_argument('--case', type=Path, default=Path('cases/generated/case_001.in'))
    parser.add_argument('--output', type=Path, default=Path('results/profile.txt'))
    args = parser.parse_args()
    profiler = cProfile.Profile()
    old_stdin, old_stdout = sys.stdin,sys.stdout
    try:
        sys.stdin = io.TextIOWrapper(io.BytesIO(args.case.read_bytes()))
        sys.stdout = io.StringIO()
        profiler.enable()
        runpy.run_path(str(args.solver), run_name='__main__')
        profiler.disable()
    finally:
        sys.stdin,sys.stdout = old_stdin,old_stdout
    stream = io.StringIO()
    pstats.Stats(profiler,stream=stream).strip_dirs().sort_stats('cumulative').print_stats(25)
    args.output.parent.mkdir(exist_ok=True,parents=True)
    args.output.write_text(stream.getvalue())
    print(stream.getvalue())


if __name__ == '__main__':
    main()
