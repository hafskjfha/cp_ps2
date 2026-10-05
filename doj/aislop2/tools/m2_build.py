"""Assemble measured experiment fragments into a standalone literal wrapper."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.compact_submission import pack_source, decode_literal_wrapper


def runtime_source():
    source = (ROOT / 'solvers/experiments/seven_construct_fast_bytearray_readable.py').read_text()
    original = '''        self.tie_masks = [0] * size.bit_length()
        for rank, aid in enumerate(order):
            bit = 1 << aid
            while rank:
                low = rank & -rank
                self.tie_masks[low.bit_length() - 1] |= bit
                rank ^= low'''
    assert source.count(original) == 1
    source = source.replace(original, '        self.tie_masks = m2_tie_masks(order)')
    fragment = (ROOT / 'solvers/experiments/m2_runtime_fragment.py').read_text()
    source = source.replace('\ndef main():', '\n' + fragment + '\ndef main():')
    return source


def save(source, stem):
    readable = ROOT / ('solvers/experiments/' + stem + '_readable.py')
    packed = ROOT / ('solvers/experiments/' + stem + '.py')
    compile(source, str(readable), 'exec')
    wrapper = pack_source(source)
    assert decode_literal_wrapper(wrapper) == source
    readable.write_text(source, encoding='utf8', newline='\n')
    packed.write_text(wrapper, encoding='ascii', newline='\n')
    print(packed, len(wrapper))


if __name__ == '__main__':
    save(runtime_source(), 'm2_runtime')
