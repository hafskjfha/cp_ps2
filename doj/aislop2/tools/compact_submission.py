"""Deterministically compact a solver, preserving its parsed Python behavior.

The packed form is an exact, inspectable lzma + base85 literal wrapper.  This
module deliberately does not change the repository's submission safety checker.
"""
from __future__ import annotations

import argparse
import ast
import base64
import builtins
import hashlib
import io
import itertools
import json
import keyword
import lzma
from pathlib import Path
import string
import tokenize


def identifiers():
    alphabet = string.ascii_lowercase + string.ascii_uppercase
    for width in range(1, 5):
        for value in range(len(alphabet) ** width):
            chars = []
            for _ in range(width):
                chars.append(alphabet[value % len(alphabet)])
                value //= len(alphabet)
            yield "".join(reversed(chars))


class Scope:
    def __init__(self, node, parent, kind):
        self.node, self.parent, self.kind = node, parent, kind
        self.names, self.globals, self.nonlocals = [], set(), set()
        self.mapping = {}

    def bind(self, name):
        if name not in self.names:
            self.names.append(name)

    def resolve(self, name):
        scope = self
        if name in self.globals:
            while scope.parent is not None:
                scope = scope.parent
        while scope is not None:
            if name in scope.mapping:
                return scope.mapping[name]
            scope = scope.parent
        return name


class ScopeBuilder(ast.NodeVisitor):
    """Assign lexical scopes explicitly, including comprehension first iterables."""
    def __init__(self, tree):
        self.root = self.scope = Scope(tree, None, "module")
        self.scopes = [self.root]
        self.visit(tree)

    def visit(self, node):
        node._compact_scope = self.scope
        return super().visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Store, ast.Del)):
            self.scope.bind(node.id)

    def visit_Global(self, node):
        self.scope.globals.update(node.names)

    def visit_Nonlocal(self, node):
        self.scope.nonlocals.update(node.names)

    def visit_Import(self, node):
        for alias in node.names:
            self.scope.bind(alias.asname or alias.name.split(".")[0])

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.scope.bind(alias.asname or alias.name)

    def enter(self, node, kind):
        parent = self.scope
        if kind in ("function", "comprehension") and parent.kind == "class":
            parent = parent.parent
        self.scope = Scope(node, parent, kind)
        self.scopes.append(self.scope)
        return self.scope

    def visit_FunctionDef(self, node):
        self.scope.bind(node.name)
        outer = self.scope
        for item in node.decorator_list + node.args.defaults + [x for x in node.args.kw_defaults if x is not None]:
            self.visit(item)
        self.enter(node, "function")
        node._compact_body_scope = self.scope
        for argument in node.args.posonlyargs + node.args.args + node.args.kwonlyargs + [x for x in (node.args.vararg, node.args.kwarg) if x]:
            argument._compact_scope = self.scope
            self.scope.bind(argument.arg)
        for item in node.body:
            self.visit(item)
        self.scope.names = [name for name in self.scope.names if name not in self.scope.globals | self.scope.nonlocals]
        self.scope = outer

    def visit_Lambda(self, node):
        outer = self.scope
        for item in node.args.defaults + [x for x in node.args.kw_defaults if x is not None]:
            self.visit(item)
        self.enter(node, "function")
        for argument in node.args.posonlyargs + node.args.args + node.args.kwonlyargs + [x for x in (node.args.vararg, node.args.kwarg) if x]:
            argument._compact_scope = self.scope
            self.scope.bind(argument.arg)
        self.visit(node.body)
        self.scope = outer

    def visit_ClassDef(self, node):
        self.scope.bind(node.name)
        outer = self.scope
        for item in node.bases + node.decorator_list:
            self.visit(item)
        for item in node.keywords:
            self.visit(item)
        self.enter(node, "class")
        for item in node.body:
            self.visit(item)
        self.scope = outer

    def comprehension(self, node, fields):
        outer = self.scope
        self.visit(node.generators[0].iter)
        self.enter(node, "comprehension")
        for index, generator in enumerate(node.generators):
            self.visit(generator.target)
            if index:
                self.visit(generator.iter)
            for item in generator.ifs:
                self.visit(item)
        for field in fields:
            self.visit(getattr(node, field))
        self.scope = outer

    def visit_ListComp(self, node):
        self.comprehension(node, ["elt"])

    visit_SetComp = visit_GeneratorExp = visit_ListComp

    def visit_DictComp(self, node):
        self.comprehension(node, ["key", "value"])


class Rename(ast.NodeTransformer):
    def __init__(self, attrs):
        self.attrs = attrs

    def visit_Name(self, node):
        node.id = node._compact_scope.resolve(node.id)
        return node

    def visit_arg(self, node):
        node.arg = node._compact_scope.resolve(node.arg)
        return node

    def visit_Attribute(self, node):
        node.attr = self.attrs.get(node.attr, node.attr)
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if node._compact_scope.kind == "class":
            node.name = self.attrs.get(node.name, node.name)
        else:
            node.name = node._compact_scope.resolve(node.name)
        return self.generic_visit(node)

    def visit_ClassDef(self, node):
        node.name = node._compact_scope.resolve(node.name)
        return self.generic_visit(node)

    def visit_Global(self, node):
        node.names = [node._compact_scope.resolve(name) for name in node.names]
        return node

    visit_Nonlocal = visit_Global

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            return None
        return self.generic_visit(node)


def dense_source(source):
    """Use one-space indentation and remove token gaps where lexically safe."""
    result, line, depth, previous = [], [], 0, None
    ignorable = {tokenize.ENCODING, tokenize.COMMENT, tokenize.NL, tokenize.ENDMARKER}
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        kind, value = token.type, token.string
        if kind in ignorable:
            continue
        if kind == tokenize.INDENT:
            depth += 1
        elif kind == tokenize.DEDENT:
            depth -= 1
        elif kind == tokenize.NEWLINE:
            if line:
                result.append(" " * depth + "".join(line))
            line, previous = [], None
        else:
            if previous is not None:
                # Whitespace is necessary precisely when joining changes tokens.
                try:
                    joined = [(t.type, t.string) for t in itertools.islice(
                        tokenize.generate_tokens(io.StringIO(previous[1] + value).readline), 2)]
                except (tokenize.TokenError, IndentationError):
                    joined = []
                if joined != [previous, (kind, value)] or (previous[0] == tokenize.NUMBER and kind == tokenize.NAME):
                    line.append(" ")
            line.append(value)
            previous = (kind, value)
    return "\n".join(result) + "\n"


def compact_source(source):
    tree = ast.parse(source)
    prohibited = (ast.AsyncFunctionDef, ast.AsyncFor, ast.AsyncWith, ast.NamedExpr, ast.Match, ast.ExceptHandler, ast.AnnAssign)
    if any(isinstance(node, prohibited) for node in ast.walk(tree)):
        raise ValueError("Unsupported scope construct: compaction would need additional scope handling.")
    reflective = {"eval", "exec", "compile", "locals", "globals", "vars", "getattr", "setattr", "delattr", "hasattr"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in reflective:
            raise ValueError("Cannot safely rename reflective code: " + node.func.id)
        if isinstance(node, ast.FunctionDef) and node.returns:
            raise ValueError("Return annotations are not supported by lexical renaming.")
        if isinstance(node, (ast.FunctionDef, ast.Lambda)) and any(arg.annotation for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs + [x for x in (node.args.vararg, node.args.kwarg) if x]):
            raise ValueError("Annotated arguments are not supported by lexical renaming.")
    builder = ScopeBuilder(tree)
    all_names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    imports = {alias.asname or alias.name.split(".")[0] for node in ast.walk(tree)
               if isinstance(node, (ast.Import, ast.ImportFrom)) for alias in node.names}
    pinned = set(dir(builtins)) | set(keyword.kwlist) | imports | {"_", "__name__"}
    pinned |= {node.arg for node in ast.walk(tree) if isinstance(node, ast.keyword)}
    # Existing method and attribute names may be passed through external objects;
    # rename only attributes rooted in self and exclude every external API name.
    attrs = {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "self" and not node.attr.startswith("__")}
    methods = {node.name for cls in ast.walk(tree) if isinstance(cls, ast.ClassDef)
               for node in cls.body if isinstance(node, ast.FunctionDef) and not node.name.startswith("__")}
    attrs |= methods
    standard_attrs = set().union(*(set(dir(value)) for value in (object, type, list, tuple, dict, set, str, bytes, int, float)))
    attrs -= standard_attrs
    external_attrs = {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)} - attrs
    attr_identifiers = (x for x in identifiers() if x not in external_attrs and x not in keyword.kwlist)
    attr_map = {name: next(attr_identifiers) for name in sorted(attrs)}
    global_names = set(builder.root.names)
    global_ids = ("_" + x for x in identifiers() if "_" + x not in pinned | all_names)
    for name in builder.root.names:
        if name not in pinned and not name.startswith("__"):
            builder.root.mapping[name] = next(global_ids)
    reserved_globals = pinned | (global_names - builder.root.mapping.keys()) | set(builder.root.mapping.values())
    for scope in builder.scopes[1:]:
        if scope.kind == "class":
            # Class methods/attributes are renamed uniformly through attr_map.
            scope.mapping = {name: attr_map[name] for name in scope.names if name in attr_map}
            continue
        reserved = reserved_globals.copy()
        parent = scope.parent
        while parent is not None:
            reserved.update(parent.mapping.values())
            reserved.update(set(parent.names) - parent.mapping.keys())
            parent = parent.parent
        candidates = (name for name in identifiers() if name not in reserved)
        for name in scope.names:
            if name not in pinned and not name.startswith("__"):
                scope.mapping[name] = next(candidates)
    tree = Rename(attr_map).visit(tree)
    ast.fix_missing_locations(tree)
    unparsed = ast.unparse(tree)
    dense = dense_source(unparsed)
    # Token compaction must preserve the already-renamed AST exactly.
    if ast.dump(ast.parse(dense), include_attributes=False) != ast.dump(ast.parse(unparsed), include_attributes=False):
        raise ValueError("Dense token serialization changed the parsed program.")
    compile(dense, "<compacted>", "exec")
    return dense


def literal_container(compressed, encoding):
    if encoding == "latin1":
        # Python's encoding cookie decodes each source byte to one character.
        # Escape characters changed by source parsing, including CR normalization.
        quote = min(("'", '"'), key=lambda char: compressed.count(char.encode()))
        literal = compressed.decode("latin1").replace("\\", "\\\\").replace("\x00", "\\x00").replace("\r", "\\r").replace(quote, "\\" + quote)
        return "# coding: latin-1\nimport lzma\nexec(lzma.decompress(" + quote * 3 + literal + quote * 3 + ".encode('latin1')))\n"
    if encoding != "base85":
        raise ValueError("Unknown packing encoding.")
    literal = repr(base64.b85encode(compressed))
    return "import base64,lzma\nexec(lzma.decompress(base64.b85decode(" + literal + ")))\n"


def pack_source(source, encoding="base85"):
    """Choose lossless LZMA settings by actual container size, deterministically."""
    data = source.encode("utf-8")
    candidates = []
    for lc in range(5):
        for lp in range(min(1, 4 - lc) + 1):
            for pb in range(5):
                compressed = lzma.compress(data, format=lzma.FORMAT_ALONE, filters=[
                    {"id": lzma.FILTER_LZMA1, "preset": 9, "dict_size": 1 << 20,
                     "lc": lc, "lp": lp, "pb": pb}])
                candidates.append(literal_container(compressed, encoding))
    return min(candidates, key=lambda value: len(value.encode("latin1" if encoding == "latin1" else "ascii")))


def decode_literal_wrapper(source, max_decoded=1_000_000):
    """Decode *only* this exact literal wrapper without executing any code.

    Consumers must run their normal static checker on the returned source.  No
    other exec call is made acceptable, and nested wrappers remain rejected.
    """
    tree = ast.parse(source)
    templates = [
        ("base85", ast.parse("import base64,lzma\nexec(lzma.decompress(base64.b85decode(b'')))\n")),
        ("latin1", ast.parse("import lzma\nexec(lzma.decompress(''.encode('latin1')))\n")),
    ]
    try:
        decoding = tree.body[1].value.args[0].args[0]
        if isinstance(decoding.func, ast.Attribute) and decoding.func.attr == "encode":
            literal, encoding = decoding.func.value, "latin1"
        else:
            literal, encoding = decoding.args[0], "base85"
    except (AttributeError, IndexError) as exc:
        raise ValueError("Not the supported literal wrapper.") from exc
    required = bytes if encoding == "base85" else str
    if not isinstance(literal, ast.Constant) or not isinstance(literal.value, required):
        raise ValueError("Packed payload must be one literal constant.")
    payload = literal.value
    literal.value = required()
    template = dict(templates)[encoding]
    if ast.dump(tree, include_attributes=False) != ast.dump(template, include_attributes=False):
        raise ValueError("Packed wrapper contains extra or changed executable syntax.")
    try:
        compressed = base64.b85decode(payload) if encoding == "base85" else payload.encode("latin1")
        decoder = lzma.LZMADecompressor(memlimit=128 * 1024 * 1024)
        decoded = decoder.decompress(compressed, max_length=max_decoded + 1)
        if len(decoded) > max_decoded or not decoder.eof or decoder.unused_data:
            raise ValueError("Packed payload exceeds limits or has trailing compressed data.")
        return decoded.decode("utf-8")
    except (ValueError, UnicodeError, lzma.LZMAError) as exc:
        raise ValueError("Invalid or oversized compressed source.") from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--plain", action="store_true")
    parser.add_argument("--encoding", choices=["base85", "latin1"], default="base85")
    parser.add_argument("--decoded", type=Path)
    args = parser.parse_args()
    original = args.source.read_bytes()
    dense = compact_source(original.decode("utf-8"))
    result = dense if args.plain else pack_source(dense, args.encoding)
    if not args.plain and decode_literal_wrapper(result) != dense:
        raise ValueError("Packed source did not round-trip.")
    encoded = result.encode("latin1" if not args.plain and args.encoding == "latin1" else "utf-8")
    args.output.write_bytes(encoded)
    if args.decoded:
        args.decoded.write_text(dense, encoding="utf-8", newline="\n")
    print(json.dumps({"original_bytes": len(original), "dense_bytes": len(dense.encode()),
                      "output_bytes": len(encoded), "output_sha256": hashlib.sha256(encoded).hexdigest(),
                      "decoded_sha256": hashlib.sha256(dense.encode()).hexdigest()}))


if __name__ == "__main__":
    main()
