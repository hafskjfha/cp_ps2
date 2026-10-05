"""Semantic and hostile-wrapper regression tests for the optional compactor."""
import ast
import base64
import contextlib
import io
import lzma
import os
import random
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.compact_submission import compact_source, decode_literal_wrapper, pack_source


def output(source):
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        exec(compile(source, "<test>", "exec"), {"__name__": "__main__"})
    return stream.getvalue()


class CompactionTests(unittest.TestCase):
    def parity(self, source):
        plain = compact_source(source)
        self.assertEqual(output(source), output(plain))
        packed = pack_source(plain)
        self.assertEqual(decode_literal_wrapper(packed), plain)
        self.assertEqual(output(source), output(packed))

    def test_nested_scopes_comprehensions_and_defaults(self):
        self.parity('''
outer = 11
def factory(value):
    def inner(extra=outer):
        return [value + j + extra for j in range(3)]
    def mutate():
        nonlocal value
        value += 1
    mutate()
    return inner
values = [1, 2, 3]
print(factory(5)())
print([values for values in values])
print([(lambda x: x+value)(4) for value in values])
print({key: key+outer for key in range(3)})
''')

    def test_globals_class_attributes_and_keywords(self):
        self.parity('''
counter = 3
class Base:
    cached = 8
    def __init__(self, number):
        self.number = number
    def calculate(self, multiplier=2):
        return self.cached + self.number * multiplier
class Child(Base):
    def calculate(self, multiplier=2):
        return super().calculate(multiplier) + 1
def alter():
    global counter
    counter += 2
    return counter
print(Child(7).calculate(multiplier=3), alter())
''')

    def test_token_spacing_has_no_compile_warnings(self):
        source = "print(1 if 2 else 3); print(1 .real); print(0xF); print('a' 'b')\n"
        dense = compact_source(source)
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            compile(dense, "<dense>", "exec")
        self.assertEqual(output(source), output(dense))

    def test_reflection_and_unsupported_scopes_fail_closed(self):
        for source in ("print(locals())", "x = (y:=1)", "def f(x:int): return x"):
            with self.subTest(source=source):
                with self.assertRaises(ValueError):
                    compact_source(source)

    def test_exact_wrapper_and_payload_limits(self):
        packed = pack_source("print(0)\n")
        self.assertEqual(decode_literal_wrapper(packed), "print(0)\n")
        mutations = [
            packed + "print('extra')\n",
            packed.replace("exec(", "eval(", 1),
            packed.replace("import base64,lzma", "import base64,lzma,os"),
            packed.replace("base64.b85decode(", "base64.b64decode("),
            "import base64,lzma\nexec(lzma.decompress(base64.b85decode(input())))\n",
        ]
        for changed in mutations:
            with self.subTest(source=changed[:80]):
                with self.assertRaises(ValueError):
                    decode_literal_wrapper(changed)
        with self.assertRaises(ValueError):
            decode_literal_wrapper(pack_source("x" * 1025), max_decoded=1024)
        compressed = lzma.compress(b"print(0)\n") + b"trailing"
        literal = repr(base64.b85encode(compressed))
        trailing = "import base64,lzma\nexec(lzma.decompress(base64.b85decode(" + literal + ")))\n"
        with self.assertRaises(ValueError):
            decode_literal_wrapper(trailing)

    def test_latin1_literal_roundtrip_and_real_file_execution(self):
        rng = random.Random(120938)
        source = "print(" + repr("".join(chr(rng.randrange(32, 127)) for _ in range(5000))) + ")\n"
        packed = pack_source(source, "latin1")
        self.assertEqual(decode_literal_wrapper(packed), source)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "packed.py"
            path.write_bytes(packed.encode("latin1"))
            process = subprocess.run([sys.executable, "-I", "-B", str(path)], capture_output=True, check=True)
        self.assertEqual(process.stdout.decode().replace("\r\n", "\n"), output(source))
        self.assertFalse(process.stderr)
        for changed in (packed.replace(".encode('latin1')", ".encode('utf8')"),
                        packed + "print('bad')\n",
                        packed.replace("import lzma", "import lzma,os"),
                        "import lzma\nexec(lzma.decompress(input().encode('latin1')))\n"):
            with self.subTest(source=changed[:80]):
                with self.assertRaises(ValueError):
                    decode_literal_wrapper(changed)

    def test_decoder_does_not_accept_or_execute_nested_payload(self):
        # It only decodes one source layer. The caller's normal source inspector
        # must reject this inner exec, rather than allowing recursive wrappers.
        inner = "exec('print(1)')\n"
        self.assertEqual(decode_literal_wrapper(pack_source(inner)), inner)
        self.assertTrue(any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "exec"
                            for n in ast.walk(ast.parse(inner))))

    def test_hash_seed_reproducibility(self):
        script = "from tools.compact_submission import *;import hashlib;print(hashlib.sha256(compact_source('def outer(value):\\n return [i+value for i in range(3)]\\nprint(outer(2))\\n').encode()).hexdigest())"
        digests = []
        root = Path(__file__).resolve().parents[1]
        for seed in ("0", "1", "12345"):
            env = os.environ.copy()
            env["PYTHONHASHSEED"] = seed
            process = subprocess.run([sys.executable, "-c", script], cwd=root, env=env, capture_output=True, check=True)
            self.assertFalse(process.stderr)
            digests.append(process.stdout)
        self.assertEqual(len(set(digests)), 1)


if __name__ == "__main__":
    unittest.main()
