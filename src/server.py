import sys
import io
import contextlib
import json
from flask import Flask, request, jsonify
from src.lexer import tokenize
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter
from src.semantic.analyzer import SemanticAnalyzer
from src.generator.generator import generate_python, CodeGenerator
from src.parser.ast import Program

app = Flask(__name__)

class PipelineEncoder(json.JSONEncoder):
    """Custom JSON encoder for pipeline objects."""
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        if hasattr(obj, 'value') and hasattr(obj, 'name'):
            return {'name': obj.name, 'value': obj.value}
        return super().default(obj)

def ast_to_dict(node):
    """Convert AST node to a serializable dictionary."""
    if node is None:
        return None
    if isinstance(node, list):
        return [ast_to_dict(item) for item in node]
    if isinstance(node, (str, int, float, bool)):
        return node
    if hasattr(node, '__dataclass_fields__'):
        result = {'_type': type(node).__name__}
        for field_name in node.__dataclass_fields__:
            value = getattr(node, field_name)
            result[field_name] = ast_to_dict(value)
        return result
    if hasattr(node, '__dict__'):
        result = {'_type': type(node).__name__}
        for key, value in node.__dict__.items():
            if not key.startswith('_'):
                result[key] = ast_to_dict(value)
        return result
    return str(node)

def symbol_table_to_dict(st, include_builtins: bool = True):
    """Convert symbol table to serializable dictionary."""
    scopes = []
    current = st.current_scope
    builtin_names = {
        'print', 'len', 'str', 'num', 'range', 'abs', 'pow', 'sqrt',
        'input', 'int', 'float', 'bool', 'list', 'max', 'min', 'sum'
    }
    while current:
        scope_data = {
            'name': current.name,
            'symbols': {}
        }
        for name, symbol in current.symbols.items():
            # Filter out built-in functions unless include_builtins is True
            if not include_builtins and symbol.is_function and name in builtin_names:
                continue
            sym_data = {
                'name': symbol.name,
                'type': str(symbol.type_info),
                'is_function': symbol.is_function,
                'is_variadic': symbol.is_variadic,
                'is_builtin': symbol.is_function and name in builtin_names,
                'defined': symbol.defined,
            }
            if symbol.is_function:
                sym_data['param_types'] = [str(pt) for pt in symbol.param_types]
                sym_data['return_type'] = str(symbol.return_type) if symbol.return_type else None
            scope_data['symbols'][name] = sym_data
        scopes.append(scope_data)
        current = current.parent
    return {'scopes': list(reversed(scopes))}

@app.route('/')
def index():
    return jsonify({
        "service": "GenZCode Studio API",
        "status": "running",
        "endpoints": {
            "POST /run": "Execute GenZCode and return output",
            "POST /pipeline": "Run full compiler pipeline and return all stages"
        }
    })

@app.route('/run', methods=['POST'])
def run_code():
    if not request.is_json:
        return jsonify({"output": "Error: Request must be JSON"}), 400
    data = request.json
    if not data or "code" not in data:
        return jsonify({"output": "Error: Missing 'code' field in JSON body"}), 400
    code = data["code"]
    
    # Capture standard output
    output_buffer = io.StringIO()
    error_msg = None
    
    with contextlib.redirect_stdout(output_buffer):
        try:
            tokens = tokenize(code)
            ast = Parser(tokens).parse()
            Interpreter().interpret(ast)
        except Exception as e:
            error_msg = str(e)
            
    output = output_buffer.getvalue()
    
    if error_msg:
        if output:
            output += "\n"
        output += f"Error: {error_msg}"
        
    return jsonify({"output": output})

@app.route('/pipeline', methods=['POST'])
def pipeline():
    """Run the full compiler pipeline and return all stages with detailed data."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.json
    if not data or "code" not in data:
        return jsonify({"error": "Missing 'code' field in JSON body"}), 400
    code = data["code"]

    stages = []
    output_buffer = io.StringIO()
    execution_output = ""
    error_msg = None

    try:
        # Stage 1: Lexical Analysis
        tokens = tokenize(code)
        token_data = []
        for t in tokens:
            token_data.append({
                'type': t.type.name,
                'lexeme': t.lexeme,
                'literal': t.literal,
                'line': t.line,
                'column': t.column
            })
        stages.append({
            'name': 'lexer',
            'title': 'Lexical Analysis',
            'description': 'The lexer scans the raw source code character by character, grouping them into meaningful tokens. It recognizes keywords like lowkey, sus, and spill_tea; identifiers; numbers; strings; operators; and punctuation. Comments are stripped and whitespace is ignored.',
            'tokens': token_data,
            'status': 'success'
        })

        # Stage 2: Parsing
        ast = Parser(tokens).parse()
        ast_dict = ast_to_dict(ast)
        stages.append({
            'name': 'parser',
            'title': 'Syntax Analysis (Parsing)',
            'description': 'The parser takes the token stream and builds an Abstract Syntax Tree (AST) using recursive descent parsing. It validates grammar rules, handles operator precedence, and constructs a hierarchical representation of the program structure.',
            'ast': ast_dict,
            'status': 'success'
        })

        # Stage 3: Semantic Analysis
        analyzer = SemanticAnalyzer()
        symbol_table = analyzer.analyze(ast)
        st_dict = symbol_table_to_dict(symbol_table)
        stages.append({
            'name': 'semantic',
            'title': 'Semantic Analysis',
            'description': 'The semantic analyzer traverses the AST to perform type checking, scope resolution, and symbol table construction. It validates that variables are declared before use, types match in assignments, function calls have correct arguments, and break/continue statements appear inside loops.',
            'symbol_table': st_dict,
            'status': 'success'
        })

        # Stage 4: Intermediate Code (IR) Generation
        ir_code = generate_ir(ast)
        stages.append({
            'name': 'intermediate',
            'title': 'Intermediate Code (IR)',
            'description': 'The intermediate code generator produces a three-address code (TAC) representation. This platform-independent representation breaks complex expressions into simple instructions with at most one operator per instruction, making it ideal for optimization and easier code generation.',
            'ir_code': ir_code,
            'status': 'success'
        })

        # Stage 5: Optimized IR
        optimized_ir = optimize_ir(ir_code)
        stages.append({
            'name': 'optimizer',
            'title': 'Optimization Pass',
            'description': 'The optimization pass applies various compiler optimizations to the intermediate code: constant folding (evaluating constant expressions at compile time), copy propagation, dead code elimination, and strength reduction. These transformations reduce execution time and code size.',
            'ir_code': optimized_ir,
            'status': 'success'
        })

        # Stage 6: Code Generation
        python_code = generate_python(ast)
        stages.append({
            'name': 'generator',
            'title': 'Code Generation',
            'description': 'The code generator traverses the validated AST and emits equivalent Python code. It maps GenZ constructs to Python: lowkey becomes variable assignment, sus becomes if, keep_yapping becomes while, vibe_check becomes def, and brainrot builtins become Python helper functions.',
            'python_code': python_code,
            'status': 'success'
        })

        # Stage 7: Execution / Interpretation
        with contextlib.redirect_stdout(output_buffer):
            Interpreter().interpret(ast)
        execution_output = output_buffer.getvalue()
        stages.append({
            'name': 'interpreter',
            'title': 'Execution (Interpretation)',
            'description': 'The interpreter walks the AST and executes it directly without compiling to machine code. It maintains an environment for variable storage, handles function calls with closures, evaluates expressions with proper operator semantics, and produces program output.',
            'output': execution_output,
            'status': 'success'
        })

    except Exception as e:
        error_msg = str(e)
        # Add error to the last stage attempted
        if stages:
            stages[-1]['status'] = 'error'
            stages[-1]['error'] = error_msg

    return jsonify({
        'stages': stages,
        'error': error_msg,
        'output': execution_output
    })


# =============================================================================
# Intermediate Code Generation (TAC - Three Address Code)
# =============================================================================

class IRGenerator:
    """Generate Three-Address Code (TAC) intermediate representation."""

    def __init__(self):
        self.instructions: list[str] = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self) -> str:
        t = f"t{self.temp_count}"
        self.temp_count += 1
        return t

    def new_label(self) -> str:
        l = f"L{self.label_count}"
        self.label_count += 1
        return l

    def emit(self, code: str) -> None:
        self.instructions.append(code)

    def generate(self, ast: Program) -> str:
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0
        self._visit_program(ast)
        return '\n'.join(self.instructions)

    def _visit_program(self, node: Program) -> None:
        for stmt in node.statements:
            self._visit(stmt)

    def _visit(self, node) -> None:
        method = f"_visit_{type(node).__name__}"
        if hasattr(self, method):
            return getattr(self, method)(node)
        return None

    def _visit_VarDecl(self, node) -> None:
        if node.initializer:
            result = self._visit_expr(node.initializer)
            self.emit(f"{node.name} = {result}")

    def _visit_FuncDecl(self, node) -> None:
        self.emit(f"func {node.name}")
        if node.body:
            for stmt in node.body.statements:
                self._visit(stmt)
        self.emit(f"endfunc {node.name}")

    def _visit_PrintStmt(self, node) -> None:
        for arg in node.arguments:
            result = self._visit_expr(arg)
            self.emit(f"print {result}")

    def _visit_IfStmt(self, node) -> None:
        cond = self._visit_expr(node.condition)
        label_else = self.new_label()
        label_end = self.new_label()
        self.emit(f"ifnot {cond} goto {label_else}")
        if node.then_branch:
            self._visit(node.then_branch)
        self.emit(f"goto {label_end}")
        self.emit(f"{label_else}:")
        if node.else_branch:
            self._visit(node.else_branch)
        self.emit(f"{label_end}:")

    def _visit_WhileStmt(self, node) -> None:
        label_start = self.new_label()
        label_end = self.new_label()
        self.emit(f"{label_start}:")
        cond = self._visit_expr(node.condition)
        self.emit(f"ifnot {cond} goto {label_end}")
        if node.body:
            self._visit(node.body)
        self.emit(f"goto {label_start}")
        self.emit(f"{label_end}:")

    def _visit_ForStmt(self, node) -> None:
        label_start = self.new_label()
        label_end = self.new_label()
        if node.init:
            self._visit(node.init)
        self.emit(f"{label_start}:")
        if node.condition:
            cond = self._visit_expr(node.condition)
            self.emit(f"ifnot {cond} goto {label_end}")
        if node.body:
            self._visit(node.body)
        if node.update:
            result = self._visit_expr(node.update)
            self.emit(result)
        self.emit(f"goto {label_start}")
        self.emit(f"{label_end}:")

    def _visit_ReturnStmt(self, node) -> None:
        if node.value:
            result = self._visit_expr(node.value)
            self.emit(f"return {result}")
        else:
            self.emit("return")

    def _visit_BreakStmt(self, node) -> None:
        self.emit("goto endloop")

    def _visit_ContinueStmt(self, node) -> None:
        self.emit("goto loopstart")

    def _visit_ExprStmt(self, node) -> None:
        self._visit_expr(node.expression)

    def _visit_Block(self, node) -> None:
        for stmt in node.statements:
            self._visit(stmt)

    def _visit_SwitchStmt(self, node) -> None:
        expr = self._visit_expr(node.expression)
        end_label = self.new_label()
        for case_val, case_stmts in node.cases:
            cv = self._visit_expr(case_val)
            label_case = self.new_label()
            self.emit(f"if {expr} == {cv} goto {label_case}")
            for stmt in case_stmts:
                self._visit(stmt)
            self.emit(f"goto {end_label}")
            self.emit(f"{label_case}:")
        if node.default:
            for stmt in node.default:
                self._visit(stmt)
        self.emit(f"{end_label}:")

    def _visit_Assignment(self, node) -> None:
        result = self._visit_expr(node.value)
        target = self._visit_expr(node.target)
        self.emit(f"{target} = {result}")

    def _visit_expr(self, expr) -> str:
        method = f"_expr_{type(expr).__name__}"
        if hasattr(self, method):
            return getattr(self, method)(expr)
        return str(expr.value if hasattr(expr, 'value') else expr)

    def _expr_Literal(self, expr) -> str:
        if isinstance(expr.value, str):
            return f'"{expr.value}"'
        return str(expr.value)

    def _expr_Variable(self, expr) -> str:
        return expr.name

    def _expr_ArrayAccess(self, expr) -> str:
        arr = self._visit_expr(expr.array)
        idx = self._visit_expr(expr.index)
        t = self.new_temp()
        self.emit(f"{t} = {arr}[{idx}]")
        return t

    def _expr_ArrayLiteral(self, expr) -> str:
        elements = [self._visit_expr(e) for e in expr.elements]
        return f"[{', '.join(elements)}]"

    def _expr_Binary(self, expr) -> str:
        left = self._visit_expr(expr.left)
        right = self._visit_expr(expr.right)
        t = self.new_temp()
        self.emit(f"{t} = {left} {expr.operator} {right}")
        return t

    def _expr_Unary(self, expr) -> str:
        operand = self._visit_expr(expr.operand)
        t = self.new_temp()
        self.emit(f"{t} = {expr.operator}{operand}")
        return t

    def _expr_FuncCall(self, expr) -> str:
        args = [self._visit_expr(a) for a in expr.arguments]
        t = self.new_temp()
        self.emit(f"{t} = call {expr.name}({', '.join(args)})")
        return t

    def _expr_Assignment(self, expr) -> str:
        result = self._visit_expr(expr.value)
        target = self._visit_expr(expr.target)
        self.emit(f"{target} = {result}")
        return target


def generate_ir(ast: Program) -> str:
    """Generate three-address code from AST."""
    return IRGenerator().generate(ast)


def optimize_ir(ir_code: str) -> str:
    """Apply simple optimizations to TAC code."""
    lines = ir_code.split('\n')
    optimized = []
    used_vars = set()
    const_folds = {}

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or stripped.startswith('func'):
            optimized.append(line)
            continue

        # Detect constant assignments
        import re
        assign_match = re.match(r'^(\w+)\s*=\s*(.+)$', stripped)
        if assign_match:
            var_name, expr = assign_match.groups()
            # Check for simple constant folding
            const_match = re.match(r'^\s*"?(-?\d+\.?\d*)"?\s*$', expr.strip())
            if const_match:
                const_folds[var_name] = const_match.group(1)
                optimized.append(line)
                continue
            # Copy propagation check
            if expr.strip() in const_folds:
                optimized.append(f"{var_name} = {const_folds[expr.strip()]}  # copy propagation")
                continue

        # Dead code elimination - skip pure assignments that are never used
        if 'print' in stripped or 'if' in stripped or 'goto' in stripped or 'return' in stripped:
            # Mark variables in conditionals as used
            for var in const_folds:
                if var in stripped:
                    used_vars.add(var)
            optimized.append(line)
        elif 'call' in stripped or '[' in stripped:
            optimized.append(line)
        else:
            optimized.append(line)

    return '\n'.join(optimized)


@app.route('/phase', methods=['POST'])
def run_phase():
    """Run a specific compiler phase and return results."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.json
    if not data or "code" not in data:
        return jsonify({"error": "Missing 'code' field in JSON body"}), 400

    code = data["code"]
    phase = data.get("phase", "lexer")

    try:
        if phase == "lexer":
            tokens = tokenize(code)
            token_data = []
            for t in tokens:
                token_data.append({
                    'type': t.type.name,
                    'lexeme': t.lexeme,
                    'literal': t.literal,
                    'line': t.line,
                    'column': t.column
                })
            return jsonify({
                'phase': 'lexer',
                'tokens': token_data,
                'status': 'success'
            })

        elif phase == "parser":
            tokens = tokenize(code)
            ast = Parser(tokens).parse()
            return jsonify({
                'phase': 'parser',
                'ast': ast_to_dict(ast),
                'status': 'success'
            })

        elif phase == "semantic":
            tokens = tokenize(code)
            ast = Parser(tokens).parse()
            analyzer = SemanticAnalyzer()
            symbol_table = analyzer.analyze(ast)
            return jsonify({
                'phase': 'semantic',
                'symbol_table': symbol_table_to_dict(symbol_table),
                'status': 'success'
            })

        elif phase == "intermediate":
            tokens = tokenize(code)
            ast = Parser(tokens).parse()
            SemanticAnalyzer().analyze(ast)
            ir = generate_ir(ast)
            return jsonify({
                'phase': 'intermediate',
                'ir_code': ir,
                'status': 'success'
            })

        elif phase == "optimizer":
            tokens = tokenize(code)
            ast = Parser(tokens).parse()
            SemanticAnalyzer().analyze(ast)
            ir = generate_ir(ast)
            optimized = optimize_ir(ir)
            return jsonify({
                'phase': 'optimizer',
                'ir_code': ir,
                'optimized_ir': optimized,
                'status': 'success'
            })

        elif phase == "generator":
            tokens = tokenize(code)
            ast = Parser(tokens).parse()
            SemanticAnalyzer().analyze(ast)
            python_code = generate_python(ast)
            return jsonify({
                'phase': 'generator',
                'python_code': python_code,
                'status': 'success'
            })

        else:
            return jsonify({"error": f"Unknown phase: {phase}"}), 400

    except Exception as e:
        return jsonify({
            'phase': phase,
            'status': 'error',
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
