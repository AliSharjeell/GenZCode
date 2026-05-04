# GenZ/Brainrot Programming Language

A complete compiler for a Gen-Z slang-based programming language built for academic purposes.

## Quick Start

```bash
# Run directly with interpreter
python -m src.main examples/hello.genz --interpret

# Compile to Python
python -m src.main examples/hello.genz -o output.py

# Run compiled Python
python output.py
```

## GenZ Syntax Examples

```javascript
// Variables
lowkey x: num = 42;
lowkey name: txt = "bruh";
lowkey nums: num[] = [1, 2, 3];

// Print
spill_tea("hello world");
spill_tea(x);

// Conditionals
sus (x > 10) {
    spill_tea("big number");
} deadass {
    spill_tea("small number");
}

// Loops
keep_yapping (x > 0) {
    spill_tea(x);
    x = x - 1;
}

// Functions
vibe_check factorial(n: num) {
    sus (n <= 1) {
        slay 1;
    } deadass {
        slay n * factorial(n - 1);
    }
}

// Control flow
bounce;       // break - bounce out
next_up;      // continue - next iteration

// Switch statement
ratio (x) {
    bet 1: { spill_tea("one"); }
    bet 2: { spill_tea("two"); }
    nvm: { spill_tea("other"); }
}

// Booleans
lowkey is_coding: num = no_cap;   // true
lowkey is_sus: num = fr_fr;        // false
```

## Keyword Reference

| GenZ | Traditional | Description |
|------|-------------|-------------|
| `lowkey` | `let/var` | Variable declaration |
| `num` | `int/float` | Numeric type |
| `txt` | `string` | String type |
| `sus` | `if` | Conditional |
| `deadass` | `else` | Else branch |
| `keep_yapping` | `while` | While loop |
| `spill_tea` | `print` | Output |
| `vibe_check` | `function` | Function declaration |
| `slay` | `return` | Return value |
| `bounce` | `break` | Exit loop |
| `next_up` | `continue` | Next iteration |
| `ratio` | `switch` | Switch statement |
| `bet` | `case` | Case in switch |
| `nvm` | `default` | Default case |
| `no_cap` | `true` | Boolean true |
| `fr_fr` | `false` | Boolean false |

## Built-in Functions

- `print(a, b, ...)` - Print values
- `len(array)` - Array/string length
- `range(n)` - Generate [0, n)
- `abs(n)` - Absolute value
- `pow(a, b)` - a to the power of b
- `sqrt(n)` - Square root
- `str(n)` - Convert to string
- `num(s)` - Convert to number

## Project Structure

```
GenZCode/
├── src/
│   ├── lexer/         # Tokenization
│   ├── parser/        # AST generation
│   ├── semantic/      # Type checking
│   ├── generator/     # Python code gen
│   └── interpreter/   # Direct execution
├── tests/             # Test suite
└── examples/          # Sample programs
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Compiler Pipeline

```
Source Code (.genz)
    │
    ▼
[Lexer] ──► Tokens
    │
    ▼
[Parser] ──► AST
    │
    ▼
[Semantic Analyzer] ──► Validated AST
    │
    ▼
[Interpreter] ──► Execute (--interpret)
         OR
[Generator] ──► Python code (-o output.py)
```

## For Course Assignment

This compiler demonstrates:
- Lexical analysis (tokenization)
- Parsing (recursive descent)
- AST representation
- Semantic analysis (type checking, scope)
- Code generation
- Interpretation

Built with Python for Compiler Construction course.