#!/usr/bin/env python3
"""Report cyclomatic complexity for Python source files.

This file used to contain a single placeholder comment left over from
generation, while the README described a complexity checker. What is
here now is the small tool the README always described, no more: it
parses each file with the standard library ast module and counts
branching nodes per function. It does not try to be a metrics suite.
"""

import argparse
import ast
import os
import sys

# Each of these node types adds one decision point on top of the base
# complexity of 1 for entering the function at all. BoolOp is handled
# separately below because "a and b and c" is two decisions in one node.
_BRANCH_NODES = (
    ast.If,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.ExceptHandler,
    ast.IfExp,
)


def function_complexity(node):
    """Cyclomatic complexity of one function definition.

    Nested functions count toward themselves, not toward the function
    that contains them: walking into a nested def would charge the
    outer function for branches its own control flow never reaches.
    The walk below therefore does not descend into nested function or
    class definitions when scoring the outer one; those are visited as
    their own entries by iter_functions.
    """
    complexity = 1
    stack = list(node.body)
    while stack:
        child = stack.pop()
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if isinstance(child, _BRANCH_NODES):
            complexity += 1
        elif isinstance(child, ast.BoolOp):
            complexity += len(child.values) - 1
        elif isinstance(child, ast.comprehension):
            # A comprehension filter is a branch the reader has to
            # follow even though no "if" statement was written.
            complexity += len(child.ifs)
        stack.extend(ast.iter_child_nodes(child))
    return complexity


def iter_functions(tree):
    """Yield every function definition in a parsed module."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node


def check_file(path):
    """Return (results, error) for one file.

    results is a list of (line number, function name, complexity).
    A file that does not parse returns an error string instead of a
    partial result: half a complexity report looks like a measurement
    and is worse than saying the file could not be read.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=path)
    except (OSError, SyntaxError, UnicodeDecodeError) as e:
        return [], str(e)
    results = [
        (node.lineno, node.name, function_complexity(node))
        for node in iter_functions(tree)
    ]
    return sorted(results), None


def collect_paths(path):
    """Expand a file or directory argument into the .py files to check."""
    if os.path.isfile(path):
        return [path]
    found = []
    for root, _, files in os.walk(path):
        for name in sorted(files):
            if name.endswith(".py"):
                found.append(os.path.join(root, name))
    return sorted(found)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Python files and report cyclomatic complexity per function."
    )
    parser.add_argument("path", help="A Python file, or a directory searched recursively for .py files.")
    parser.add_argument(
        "--max-complexity",
        type=int,
        default=None,
        help="Exit with status 1 if any function exceeds this complexity.",
    )
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: path not found: {args.path}", file=sys.stderr)
        return 1

    files = collect_paths(args.path)
    if not files:
        print(f"No Python files found under: {args.path}", file=sys.stderr)
        return 1

    failed = False
    over_limit = False
    for path in files:
        results, error = check_file(path)
        if error is not None:
            print(f"{path}: could not be analyzed: {error}", file=sys.stderr)
            failed = True
            continue
        for lineno, name, complexity in results:
            print(f"{path}:{lineno}: {name} complexity {complexity}")
            if args.max_complexity is not None and complexity > args.max_complexity:
                over_limit = True

    if failed or over_limit:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
