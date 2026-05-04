#!/usr/bin/env python3
"""GenZ/Brainrot Programming Language Compiler.

Usage:
    python -m src.main input.genz
    python -m src.main input.genz -o output.py
    python -m src.main input.genz --run  # compile and run
"""

import sys
import argparse
from pathlib import Path

from src.lexer import tokenize
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.generator.generator import generate_python


def compile_file(input_path: str, output_path: str = None, run: bool = False) -> None:
    """Compile a GenZ source file to Python."""
    # Read source
    with open(input_path, 'r', encoding='utf-8') as f:
        source = f.read()

    print(f"Compiling {input_path}...")

    # Lexical analysis
    print("  [1/4] Lexing...")
    tokens = tokenize(source)

    # Parsing
    print("  [2/4] Parsing...")
    ast = Parser(tokens).parse()

    # Semantic analysis
    print("  [3/4] Analyzing...")
    SemanticAnalyzer().analyze(ast)

    # Code generation
    print("  [4/4] Generating Python...")
    code = generate_python(ast)

    # Output
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"  Output written to {output_path}")
    else:
        print("\n--- Generated Python Code ---")
        print(code)
        print("--- End of Generated Code ---\n")

    # Run if requested
    if run:
        print("--- Running Generated Code ---")
        exec(code, {"__name__": "__main__"})


def main():
    parser = argparse.ArgumentParser(
        description="GenZ/Brainrot Programming Language Compiler"
    )
    parser.add_argument("input", help="Input GenZ source file")
    parser.add_argument("-o", "--output", help="Output Python file")
    parser.add_argument("-r", "--run", action="store_true", help="Run the generated code")

    args = parser.parse_args()

    try:
        compile_file(args.input, args.output, args.run)
    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()