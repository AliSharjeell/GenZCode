"""Interpreter for GenZ/Brainrot language.

Actually executes GenZ code directly instead of generating Python.
"""

from typing import Any, Optional
from src.parser.ast import (
    ASTVisitor, Program, VarDecl, FuncDecl, FuncParam,
    Assignment, PrintStmt, IfStmt, SwitchStmt, WhileStmt, ForStmt, ReturnStmt,
    BreakStmt, ContinueStmt, ExprStmt, Block,
    Binary, Unary, Literal, Variable, ArrayAccess, ArrayLiteral, FuncCall, Expr
)
from .environment import (
    Environment, RuntimeValue, UserFunction, BuiltinFunction,
    ReturnValue, BreakException, ContinueException, Builtins,
    InterpreterError
)


class Interpreter(ASTVisitor):
    """Interprets GenZ code directly."""

    def __init__(self):
        self.environment = Environment()
        self.functions: dict[str, UserFunction] = {}
        self.in_loop = False

        # Register built-in functions
        self._register_builtins()

    def _register_builtins(self) -> None:
        """Register built-in functions."""
        for name, builtin in Builtins.FUNCTIONS.items():
            self.environment.define(
                name,
                RuntimeValue(builtin, 'function')
            )

    def interpret(self, ast: Program) -> Any:
        """Execute a GenZ program."""
        # Register all function declarations
        for stmt in ast.statements:
            if isinstance(stmt, FuncDecl):
                self._register_function(stmt)

        # Check if main function exists
        has_main = 'main' in self.functions

        # Execute all statements (except function definitions)
        result = None
        for stmt in ast.statements:
            if isinstance(stmt, FuncDecl):
                continue  # Already registered
            result = self.execute_statement(stmt)

        # Auto-call main() if defined with no parameters
        if has_main:
            main_func = self.functions['main']
            if len(main_func.params) == 0:
                result = main_func.call([], self)

        return result

    def _register_function(self, func_decl: FuncDecl) -> None:
        """Register a user-defined function."""
        user_func = UserFunction(
            name=func_decl.name,
            params=[p.name for p in func_decl.params],
            body=func_decl.body,
            closure=self.environment
        )
        self.functions[func_decl.name] = user_func
        self.environment.define(
            func_decl.name,
            RuntimeValue(user_func, 'function')
        )

    def execute_statement(self, stmt) -> Any:
        """Execute a single statement."""
        return self.visit(stmt)

    # -------------------------------------------------------------------------
    # Visitor Methods - Statements
    # -------------------------------------------------------------------------

    def visit_program(self, node: Program) -> object:
        for stmt in node.statements:
            self.visit(stmt)
        return None

    def visit_var_decl(self, node: VarDecl) -> object:
        value = self._evaluate_expr(node.initializer) if node.initializer else self._default_value(node.type_name)
        runtime_value = RuntimeValue(value, self._infer_runtime_type(node.type_name, value))
        self.environment.define(node.name, runtime_value)
        return None

    def visit_func_decl(self, node: FuncDecl) -> object:
        self._register_function(node)
        return None

    def visit_assignment(self, node: Assignment) -> object:
        value = self._evaluate_expr(node.value)
        self._assign_target(node.target, value)
        return value

    def visit_print_stmt(self, node: PrintStmt) -> object:
        values = [self._evaluate_expr(arg) for arg in node.arguments]
        print(' '.join(str(v) for v in values))
        return None

    def visit_if_stmt(self, node: IfStmt) -> object:
        condition = self._evaluate_expr(node.condition)
        if self._is_truthy(condition):
            return self.visit(node.then_branch)
        elif node.else_branch:
            return self.visit(node.else_branch)
        return None

    def visit_while_stmt(self, node: WhileStmt) -> object:
        self.in_loop = True
        try:
            while self._is_truthy(self._evaluate_expr(node.condition)):
                try:
                    self.visit(node.body)
                except BreakException:
                    break
                except ContinueException:
                    pass  # Continue to next iteration
        finally:
            self.in_loop = False
        return None

    def visit_for_stmt(self, node: ForStmt) -> object:
        # Execute init in a new scope
        old_env = self.environment
        self.environment = Environment(parent=old_env)
        try:
            if node.init:
                self.visit(node.init)

            self.in_loop = True
            try:
                while node.condition is None or self._is_truthy(self._evaluate_expr(node.condition)):
                    try:
                        self.visit(node.body)
                    except BreakException:
                        break
                    except ContinueException:
                        pass  # Continue to next iteration
                    finally:
                        pass

                    if node.update:
                        self._evaluate_expr(node.update)
            finally:
                self.in_loop = False
        finally:
            self.environment = old_env
        return None

    def visit_block(self, node: Block) -> object:
        old_env = self.environment
        self.environment = Environment(parent=old_env)
        result = None
        try:
            for stmt in node.statements:
                result = self.visit(stmt)
        finally:
            self.environment = old_env
        return result

    def visit_return_stmt(self, node: ReturnStmt) -> object:
        value = self._evaluate_expr(node.value) if node.value else None
        raise ReturnValue(value)

    def visit_break_stmt(self, node: BreakStmt) -> object:
        if not self.in_loop:
            raise InterpreterError("'bounce' must be inside a loop")
        raise BreakException()

    def visit_continue_stmt(self, node: ContinueStmt) -> object:
        if not self.in_loop:
            raise InterpreterError("'next_up' must be inside a loop")
        raise ContinueException()

    def visit_switch_stmt(self, node: SwitchStmt) -> object:
        switch_value = self._evaluate_expr(node.expression)

        # Execute matching case
        for case_value, case_stmts in node.cases:
            if self._evaluate_expr(case_value) == switch_value:
                for stmt in case_stmts:
                    self.visit(stmt)
                return None

        # Execute default case if no match
        if node.default:
            for stmt in node.default:
                self.visit(stmt)

        return None

    def visit_expr_stmt(self, node: ExprStmt) -> object:
        return self._evaluate_expr(node.expression)

    # -------------------------------------------------------------------------
    # Visitor Methods - Expressions
    # -------------------------------------------------------------------------

    def visit_binary(self, node: Binary) -> object:
        return self._evaluate_binary(node)

    def visit_unary(self, node: Unary) -> object:
        operand = self._evaluate_expr(node.operand)

        if node.operator == '!':
            return not self._is_truthy(operand)
        elif node.operator == '-':
            return -self._to_number(operand)

        raise InterpreterError(f"Unknown unary operator: {node.operator}")

    def visit_literal(self, node: Literal) -> object:
        return node.value

    def visit_variable(self, node: Variable) -> object:
        runtime_value = self.environment.get(node.name)
        return runtime_value.value

    def visit_array_access(self, node: ArrayAccess) -> object:
        array_value = self._evaluate_expr(node.array)
        index = self._to_number(self._evaluate_expr(node.index))

        if not isinstance(array_value, list):
            raise InterpreterError(f"'{node.array.name}' is not an array")

        try:
            return array_value[int(index)]
        except IndexError:
            raise InterpreterError(f"Array index out of bounds: {index}")

    def visit_array_literal(self, node: ArrayLiteral) -> object:
        return [self._evaluate_expr(elem) for elem in node.elements]

    def visit_func_call(self, node: FuncCall) -> object:
        return self._call_function(node.name, node.arguments)

    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------

    def _evaluate_expr(self, expr) -> Any:
        """Evaluate an expression."""
        return self.visit(expr)

    def _evaluate_binary(self, node: Binary) -> Any:
        """Evaluate a binary expression."""
        left = self._evaluate_expr(node.left)
        right = self._evaluate_expr(node.right)

        op = node.operator

        # Arithmetic
        if op == '+':
            # String concatenation
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return self._to_number(left) + self._to_number(right)
        elif op == '-':
            return self._to_number(left) - self._to_number(right)
        elif op == '*':
            return self._to_number(left) * self._to_number(right)
        elif op == '/':
            left_num = self._to_number(left)
            right_num = self._to_number(right)
            if right_num == 0:
                raise InterpreterError("Division by zero")
            return left_num / right_num
        elif op == '%':
            return self._to_number(left) % self._to_number(right)

        # Comparisons
        elif op == '<':
            return self._to_number(left) < self._to_number(right)
        elif op == '>':
            return self._to_number(left) > self._to_number(right)
        elif op == '<=':
            return self._to_number(left) <= self._to_number(right)
        elif op == '>=':
            return self._to_number(left) >= self._to_number(right)
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right

        # Logical
        elif op == '&&':
            return self._is_truthy(left) and self._is_truthy(right)
        elif op == '||':
            return self._is_truthy(left) or self._is_truthy(right)

        raise InterpreterError(f"Unknown operator: {op}")

    def _call_function(self, name: str, arguments: list[Expr]) -> Any:
        """Call a function."""
        # Check built-ins first
        builtin = Builtins.get_function(name)
        if builtin:
            if name == 'fanum_tax' and arguments and isinstance(arguments[0], Variable):
                var_name = arguments[0].name
                val = self._evaluate_expr(arguments[0])
                taxed_val = float(val) * 0.8
                self.environment.set(var_name, RuntimeValue(taxed_val, "num"))
                return taxed_val
            elif name == 'rizz' and arguments and isinstance(arguments[0], Variable):
                var_name = arguments[0].name
                val = self._evaluate_expr(arguments[0])
                rizzed_val = float(val) + 10.0
                self.environment.set(var_name, RuntimeValue(rizzed_val, "num"))
                return rizzed_val

            # Evaluate arguments normally
            args = [self._evaluate_expr(arg) for arg in arguments]
            return builtin.call(args, self)

        # Check user functions
        if name in self.functions:
            user_func = self.functions[name]
            args = [self._evaluate_expr(arg) for arg in arguments]
            return user_func.call(args, self)

        raise InterpreterError(f"Undefined function: '{name}'")

    def _assign_target(self, target: Expr, value: Any) -> None:
        """Assign to a variable or array element."""
        if isinstance(target, Variable):
            self.environment.set(target.name, RuntimeValue(value, self._infer_type(value)))
        elif isinstance(target, ArrayAccess):
            array = self._evaluate_expr(target.array)
            index = int(self._to_number(self._evaluate_expr(target.index)))
            if isinstance(array, list):
                array[index] = value
            else:
                raise InterpreterError(f"'{target.array.name}' is not an array")
        else:
            raise InterpreterError("Invalid assignment target")

    def _is_truthy(self, value: Any) -> bool:
        """Check if value is truthy."""
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        if isinstance(value, list):
            return len(value) > 0
        return True

    def _to_number(self, value: Any) -> float:
        """Convert value to a number."""
        if isinstance(value, bool):
            return 1.0 if value else 0.0
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                return 0.0
        return 0.0

    def _infer_type(self, value: Any) -> str:
        """Infer runtime type."""
        if isinstance(value, bool):
            return "num"
        if isinstance(value, (int, float)):
            return "num"
        if isinstance(value, str):
            return "txt"
        if isinstance(value, list):
            return "array"
        return "num"

    def _infer_runtime_type(self, type_name: str, value: Any) -> str:
        """Infer type from declaration and value."""
        if type_name == "num":
            return "num"
        if type_name == "txt":
            return "txt"
        if type_name.endswith("[]"):
            return "array"
        return "num"

    def _default_value(self, type_name: str) -> Any:
        """Get default value for type."""
        if type_name == "num":
            return 0
        if type_name == "txt":
            return ""
        if type_name.endswith("[]"):
            return []
        return 0

    def visit(self, node) -> object:
        """Visit a node (dispatch to appropriate method)."""
        return node.accept(self)


def interpret(source: str, skip_semantic: bool = False) -> Any:
    """Convenience function to interpret GenZ source code."""
    from src.lexer import tokenize
    from src.parser.parser import Parser

    tokens = tokenize(source)
    ast = Parser(tokens).parse()

    if not skip_semantic:
        from src.semantic.analyzer import SemanticAnalyzer
        SemanticAnalyzer().analyze(ast)

    return Interpreter().interpret(ast)