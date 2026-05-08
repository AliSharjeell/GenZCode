import sys
import io
import contextlib
import json
from flask import Flask, request, jsonify
from src.lexer import tokenize
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter
from src.semantic.analyzer import SemanticAnalyzer
from src.generator.generator import generate_python

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

def symbol_table_to_dict(st):
    """Convert symbol table to serializable dictionary."""
    scopes = []
    current = st.current_scope
    while current:
        scope_data = {
            'name': current.name,
            'symbols': {}
        }
        for name, symbol in current.symbols.items():
            sym_data = {
                'name': symbol.name,
                'type': str(symbol.type_info),
                'is_function': symbol.is_function,
                'is_variadic': symbol.is_variadic,
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

        # Stage 4: Code Generation
        python_code = generate_python(ast)
        stages.append({
            'name': 'generator',
            'title': 'Code Generation',
            'description': 'The code generator traverses the validated AST and emits equivalent Python code. It maps GenZ constructs to Python: lowkey becomes variable assignment, sus becomes if, keep_yapping becomes while, vibe_check becomes def, and brainrot builtins become Python helper functions.',
            'python_code': python_code,
            'status': 'success'
        })

        # Stage 5: Execution / Interpretation
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
