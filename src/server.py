import sys
import io
import contextlib
from flask import Flask, request, jsonify
from src.lexer import tokenize
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "service": "GenZCode Studio API",
        "status": "running",
        "endpoints": {
            "POST /run": "Execute GenZCode and return output"
        }
    })

@app.route('/run', methods=['POST'])
def run_code():
    data = request.json
    code = data.get("code", "")
    
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
