#!/usr/bin/env python3
"""GenZ/Brainrot Programming Language Compiler.

Usage:
    python -m src.main input.genz          # compile to Python (print output)
    python -m src.main input.genz -o out.py  # compile to file
    python -m src.main input.genz --run    # compile and run
    python -m src.main input.genz --interpret  # interpret directly

Phase flags (run up to a specific phase):
    python -m src.main input.genz --phase lexer   # tokenize only
    python -m src.main input.genz --phase parser  # parse only
    python -m src.main input.genz --phase semantic  # analyze only
"""

import sys
import argparse
from pathlib import Path

from src.lexer import tokenize
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.generator.generator import generate_python


def compile_file(input_path: str, output_path: str = None, run: bool = False, interpret: bool = False, phase: str = None) -> None:
    """Compile a GenZ source file to Python or run directly."""
    # Read source
    with open(input_path, 'r', encoding='utf-8') as f:
        source = f.read()

    print(f"Compiling {input_path}...")

    # Lexical analysis
    print("  [1/4] Lexing...")
    tokens = tokenize(source)

    if phase == "lexer":
        print(f"\n--- Tokens ({len(tokens)}) ---")
        for t in tokens:
            print(f"  {t}")
        print("--- End of Tokens ---\n")
        return

    # Parsing
    print("  [2/4] Parsing...")
    ast = Parser(tokens).parse()

    if phase == "parser":
        print(f"\n--- AST ---")
        print(ast)
        print("--- End of AST ---\n")
        return

    if interpret or run:
        # Use interpreter for direct execution
        print("  [3/4] Running with interpreter...")
        from src.interpreter.interpreter import Interpreter
        Interpreter().interpret(ast)
        print("  [4/4] Done!")
    else:
        # Semantic analysis
        print("  [3/4] Analyzing...")
        SemanticAnalyzer().analyze(ast)

        if phase == "semantic":
            print("  Semantic analysis passed!")
            return

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
            safe_builtins = {
                'abs': abs, 'bool': bool, 'float': float, 'input': input,
                'int': int, 'len': len, 'list': list, 'max': max, 'min': min,
                'print': print, 'range': range, 'round': round, 'str': str,
                'sum': sum, 'type': type, 'True': True, 'False': False, 'None': None,
                'RuntimeError': RuntimeError, 'NotImplementedError': NotImplementedError,
            }
            restricted_globals = {
                "__name__": "__main__",
                "__builtins__": safe_builtins,
            }
            exec(code, restricted_globals)


def run_string(source: str) -> None:
    """Run GenZ code directly from a string."""
    tokens = tokenize(source)
    ast = Parser(tokens).parse()
    from src.interpreter.interpreter import Interpreter
    Interpreter().interpret(ast)


def main():
    parser = argparse.ArgumentParser(
        description="GenZ/Brainrot Programming Language Compiler"
    )
    parser.add_argument("input", help="Input GenZ source file")
    parser.add_argument("-o", "--output", help="Output Python file")
    parser.add_argument("-r", "--run", action="store_true", help="Run the generated code")
    parser.add_argument("-i", "--interpret", action="store_true", help="Run directly with interpreter")
    parser.add_argument(
        "--phase",
        choices=["lexer", "parser", "semantic"],
        help="Stop after the specified phase (lexer, parser, or semantic)"
    )

    args = parser.parse_args()

    try:
        compile_file(args.input, args.output, args.run, args.interpret, args.phase)
    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()