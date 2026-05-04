# GenZ/Brainrot Programming Language - Specification

## Project Overview
A compiler for a "Gen-Z / Brainrot" style programming language for academic purposes (Compiler Construction course).

## Team
- **Architect Andy**: Grammar, AST design, pipeline architecture
- **Lexer/Parser Penny**: Tokenization, recursive descent parser
- **Semantic Sam**: Scope, type checking, symbol tables
- **Generator Gary**: Code generation (target: Python)

---

## Grammar Specification (EBNF)

### Lexical Structure
```ebnf
letter      ::= 'a'..'z' | 'A'..'Z' | '_'
digit       ::= '0'..'9'
ident       ::= letter (letter | digit)*
number      ::= digit+
string      ::= '"' (printable_char - '"')* '"'
comment     ::= '//' (printable_char - '\n')*
whitespace  ::= ' ' | '\t' | '\n' | '\r'
```

### Keywords
| GenZ Keyword | Traditional Equivalent | Description |
|--------------|------------------------|-------------|
| `lowkey` | `let/var` | Variable declaration |
| `num` | `int/float` | Numeric type |
| `txt` | `string` | String type |
| `sus` | `if` | Conditional |
| `deadass` | `else` | Else branch |
| `no_cap` | `true` | Boolean true |
| `fr_fr` | `false` | Boolean false |
| `keep_yapping` | `while` | While loop |
| `spill_tea` | `print` | Output statement |
| `vibe_check` | `function` | Function declaration |
| `slay` | `return` | Return statement |
| `bestie` | `break` | Break loop |
| `its_giving` | `continue` | Continue loop |

### Operators
```ebnf
add         ::= '+'
sub         ::= '-'
mul         ::= '*'
div         ::= '/'
mod         ::= '%'
assign      ::= '='
eq          ::= '=='
neq         ::= '!='
lt          ::= '<'
gt          ::= '>'
lte         ::= '<='
gte         ::= '>='
and_op      ::= '&&'
or_op       ::= '||'
not_op      ::= '!'
```

### Punctuation
```ebnf
lbrace      ::= '{'
rbrace      ::= '}'
lparen      ::= '('
rparen      ::= ')'
lbracket    ::= '['
rbracket    ::= ']'
semi        ::= ';'
comma       ::= ','
colon       ::= ':'
```

### Grammar Rules
```ebnf
program         ::= declaration* statement*

declaration     ::= func_decl | var_decl

func_decl       ::= 'vibe_check' ident '(' params? ')' '{' statement* '}'

params          ::= param (',' param)*
param           ::= ident ':' type

var_decl        ::= 'lowkey' ident ':' type ('=' expr)? ';'

type            ::= 'num' | 'txt' | type '[' ']'   (* arrays *)

statement       ::= var_decl
                  | assignment
                  | print_stmt
                  | if_stmt
                  | while_stmt
                  | func_call
                  | return_stmt
                  | break_stmt
                  | continue_stmt
                  | block

assignment      ::= ident ('[' expr ']')? '=' expr ';'

print_stmt      ::= 'spill_tea' '(' expr (',' expr)* ')' ';'

if_stmt         ::= 'sus' '(' expr ')' block
                    ('deadass' block)?
                  | 'sus' '(' expr ')' statement

while_stmt      ::= 'keep_yapping' '(' expr ')' block

block           ::= '{' statement* '}'

return_stmt     ::= 'slay' expr? ';'

break_stmt      ::= 'bestie' ';'

continue_stmt   ::= 'its_giving' ';'

func_call       ::= ident '(' args? ')' ';'
args            ::= expr (',' expr)*

expr            ::= logic_or

logic_or        ::= logic_and ('||' logic_and)*

logic_and       ::= equality ('&&' equality)*

equality        ::= comparison (('==' | '!=') comparison)*

comparison      ::= term (('<' | '>' | '<=' | '>=') term)*

term            ::= factor (('+' | '-') factor)*

factor          ::= unary (('*' | '/' | '%') unary)*

unary           ::= ('!')? primary

primary         ::= number
                  | string
                  | ident ('(' args? ')' | '[' expr ']')?
                  | 'no_cap'
                  | 'fr_fr'
                  | '(' expr ')'
                  | array_literal

array_literal   ::= '[' expr (',' expr)* ']'
```

---

## Sample GenZ Code

```javascript
// Hello World
lowkey greeting: txt = "no cap this is bussin";
spill_tea(greeting);

// Function declaration
vibe_check add(a: num, b: num) {
    slay a + b;
}

// Recursion - Factorial
vibe_check factorial(n: num) {
    sus (n <= 1) {
        slay 1;
    } deadass {
        slay n * factorial(n - 1);
    }
}

// Arrays
lowkey nums: num[5];
nums[0] = 42;
nums[1] = 1337;

// Loops
lowkey i: num = 0;
keep_yapping (i < 5) {
    spill_tea(i);
    i = i + 1;
}

// Boolean expressions
lowkey is_coding: num = no_cap;
sus (is_coding && fr_fr == fr_fr) {
    spill_tea("this syntax is lowkey valid fr fr");
}
```

---

## Design Decisions

1. **Explicit type annotations**: `lowkey x: num` instead of `lowkey x = 42`
2. **Curly braces for blocks**: Easier to parse than indentation
3. **Semicolons required**: Reduces ambiguity
4. **C-style operator precedence**: Industry standard
5. **Arrays with bracket syntax**: `type[]` for array types, `[]` for literals
6. **Function keyword**: `vibe_check` for function declarations
7. **Return keyword**: `slay` for return statements

---

## Compiler Pipeline

```
Source Code (.genz)
    │
    ▼
[Lexer] ──────► Token Stream
    │
    ▼
[Parser] ──────► AST
    │
    ▼
[Semantic Analyzer] ─────► Validated AST + Symbol Table
    │
    ▼
[Code Generator] ─────► Python / C / LLVM IR
```

---

## Version History

- v0.1: Initial grammar proposal with MVP features
- v0.2: Added functions, arrays, strings, explicit types (per feedback)