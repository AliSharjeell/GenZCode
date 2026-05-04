"""Code generator for GenZ/Brainrot language.

Generator Gary's work: translate the AST into Python code.
"""

from typing import Optional
from src.parser.ast import (
    ASTVisitor, Program, VarDecl, FuncDecl, FuncParam,
    Assignment, PrintStmt, IfStmt, WhileStmt, ReturnStmt,
    BreakStmt, ContinueStmt, ExprStmt, Block,
    Binary, Unary, Literal, Variable, ArrayAccess, ArrayLiteral, FuncCall
)


class CodeGenerator(ASTVisitor):
    """Generates Python code from GenZ AST."""

    INDENT = "    "

    def __init__(self):
        self.output: list[str] = []
        self.indent_level = 0
        self.in_loop = False

    def generate(self, ast: Program) -> str:
        """Generate Python code from the AST."""
        self.output = []
        self.indent_level = 0
        self.in_loop = False

        # Visit the program
        self.visit_program(ast)

        return '\n'.join(self.output)

    def _emit(self, code: str) -> None:
        """Add a line of code to the output."""
        indent = self.INDENT * self.indent_level
        self.output.append(f"{indent}{code}")

    def _emit_no_indent(self, code: str) -> None:
        """Add code without indentation."""
        self.output.append(code)

    # -------------------------------------------------------------------------
    # Visitor Methods
    # -------------------------------------------------------------------------

    def visit_program(self, node: Program) -> object:
        # Add Python shebang and imports
        self._emit_no_indent("# Generated Python code from GenZ/Brainrot language")
        self._emit_no_indent("import sys")
        self._emit("")

        # Generate all statements
        for stmt in node.statements:
            self.visit(stmt)
            # Add blank line after function declarations
            if isinstance(stmt, FuncDecl):
                self._emit("")

        return None

    def visit_var_decl(self, node: VarDecl) -> object:
        # Generate: var_name = initial_value
        if node.initializer:
            value = self._generate_expr(node.initializer)
        else:
            # Default values based on type
            if node.type_name == "txt":
                value = '""'
            elif node.type_name.endswith("[]"):
                value = "[]"
            else:
                value = "0"

        self._emit(f"{node.name} = {value}")
        return None

    def visit_func_decl(self, node: FuncDecl) -> object:
        # Generate Python function
        params = ", ".join(p.name for p in node.params)
        self._emit(f"def {node.name}({params}):")

        self.indent_level += 1

        # Generate function body
        if node.body:
            for stmt in node.body.statements:
                self.visit(stmt)
        else:
            self._emit("pass")

        self.indent_level -= 1
        return None

    def visit_assignment(self, node: Assignment) -> object:
        target = self._generate_expr(node.target)
        value = self._generate_expr(node.value)
        self._emit(f"{target} = {value}")
        return None

    def visit_print_stmt(self, node: PrintStmt) -> object:
        # Generate: print(arg1, arg2, ...)
        args = [self._generate_expr(arg) for arg in node.arguments]
        self._emit(f"print({', '.join(args)})")
        return None

    def visit_if_stmt(self, node: IfStmt) -> object:
        condition = self._generate_expr(node.condition)

        self._emit(f"if {condition}:")
        self.indent_level += 1
        self.visit(node.then_branch)
        self.indent_level -= 1

        if node.else_branch:
            self._emit("else:")
            self.indent_level += 1
            self.visit(node.else_branch)
            self.indent_level -= 1

        return None

    def visit_while_stmt(self, node: WhileStmt) -> object:
        condition = self._generate_expr(node.condition)

        self._emit(f"while {condition}:")
        self.indent_level += 1
        old_in_loop = self.in_loop
        self.in_loop = True
        self.visit(node.body)
        self.in_loop = old_in_loop
        self.indent_level -= 1

        return None

    def visit_return_stmt(self, node: ReturnStmt) -> object:
        if node.value:
            value = self._generate_expr(node.value)
            self._emit(f"return {value}")
        else:
            self._emit("return")
        return None

    def visit_break_stmt(self, node: BreakStmt) -> object:
        self._emit("break")
        return None

    def visit_continue_stmt(self, node: ContinueStmt) -> object:
        self._emit("continue")
        return None

    def visit_expr_stmt(self, node: ExprStmt) -> object:
        expr_code = self._generate_expr(node.expression)
        # Only emit if not a function call (function calls as statements)
        if not isinstance(node.expression, FuncCall):
            self._emit(expr_code)
        else:
            self._emit(expr_code)
        return None

    def visit_block(self, node: Block) -> object:
        for stmt in node.statements:
            self.visit(stmt)
        return None

    # -------------------------------------------------------------------------
    # Expression Generation
    # -------------------------------------------------------------------------

    def _generate_expr(self, expr) -> str:
        """Generate Python code for an expression."""
        if isinstance(expr, Literal):
            if isinstance(expr.value, bool):
                return "True" if expr.value else "False"
            elif isinstance(expr.value, str):
                return repr(expr.value)
            else:
                return str(expr.value)

        elif isinstance(expr, Variable):
            return expr.name

        elif isinstance(expr, ArrayAccess):
            array_name = expr.array.name
            index = self._generate_expr(expr.index)
            return f"{array_name}[{index}]"

        elif isinstance(expr, ArrayLiteral):
            elements = [self._generate_expr(e) for e in expr.elements]
            return f"[{', '.join(elements)}]"

        elif isinstance(expr, Binary):
            left = self._generate_expr(expr.left)
            right = self._generate_expr(expr.right)
            return f"({left} {expr.operator} {right})"

        elif isinstance(expr, Unary):
            operand = self._generate_expr(expr.operand)
            if expr.operator == "!":
                return f"(not {operand})"
            else:
                return f"(-{operand})"

        elif isinstance(expr, FuncCall):
            args = [self._generate_expr(arg) for arg in expr.arguments]
            return f"{expr.name}({', '.join(args)})"

        elif isinstance(expr, Assignment):
            target = self._generate_expr(expr.target)
            value = self._generate_expr(expr.value)
            return f"({target} = {value})"

        else:
            return "<unknown_expr>"

    # -------------------------------------------------------------------------
    # Expression visitors (for AST traversal)
    # -------------------------------------------------------------------------

    def visit_binary(self, node: Binary) -> object:
        return self._generate_expr(node)

    def visit_unary(self, node: Unary) -> object:
        return self._generate_expr(node)

    def visit_literal(self, node: Literal) -> object:
        return self._generate_expr(node)

    def visit_variable(self, node: Variable) -> object:
        return self._generate_expr(node)

    def visit_array_access(self, node: ArrayAccess) -> object:
        return self._generate_expr(node)

    def visit_array_literal(self, node: ArrayLiteral) -> object:
        return self._generate_expr(node)

    def visit_func_call(self, node: FuncCall) -> object:
        return self._generate_expr(node)

    def visit(self, node) -> object:
        """Visit a node (dispatch to appropriate method)."""
        return node.accept(self)


def generate_python(ast: Program) -> str:
    """Convenience function to generate Python code."""
    return CodeGenerator().generate(ast)