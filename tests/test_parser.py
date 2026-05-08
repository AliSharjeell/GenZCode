"""Tests for the Parser module."""

import pytest
from src.lexer import tokenize
from src.parser.parser import Parser, ParserError
from src.parser.ast import (
    Program, VarDecl, FuncDecl, FuncParam, Literal, Variable, Binary, Unary, PrintStmt, IfStmt,
    WhileStmt, ForStmt, ReturnStmt, BreakStmt, ContinueStmt, Assignment, ArrayAccess,
    ArrayLiteral, Block, ExprStmt, FuncCall
)


class TestParser:
    """Test cases for the Parser."""

    def _parse(self, source: str) -> Program:
        """Helper to parse source code."""
        tokens = tokenize(source)
        return Parser(tokens).parse()

    def test_variable_declaration_num(self):
        """Test parsing: lowkey x: num = 42;"""
        ast = self._parse("lowkey x: num = 42;")

        assert len(ast.statements) == 1
        var_decl = ast.statements[0]
        assert isinstance(var_decl, VarDecl)
        assert var_decl.name == "x"
        assert var_decl.type_name == "num"
        assert isinstance(var_decl.initializer, Literal)
        assert var_decl.initializer.value == 42

    def test_variable_declaration_txt(self):
        """Test parsing: lowkey name: txt = "hello";"""
        ast = self._parse('lowkey name: txt = "hello";')

        var_decl = ast.statements[0]
        assert isinstance(var_decl, VarDecl)
        assert var_decl.name == "name"
        assert var_decl.type_name == "txt"
        assert isinstance(var_decl.initializer, Literal)
        assert var_decl.initializer.value == "hello"

    def test_variable_declaration_no_initializer(self):
        """Test parsing: lowkey x: num;"""
        ast = self._parse("lowkey x: num;")

        var_decl = ast.statements[0]
        assert isinstance(var_decl, VarDecl)
        assert var_decl.name == "x"
        assert var_decl.type_name == "num"
        assert var_decl.initializer is None

    def test_assignment(self):
        """Test parsing: x = 42;"""
        ast = self._parse("lowkey x: num = 0; x = 42;")

        assert len(ast.statements) == 2
        # Assignment is wrapped in ExprStmt
        expr_stmt = ast.statements[1]
        assert isinstance(expr_stmt, ExprStmt)
        assign = expr_stmt.expression
        assert isinstance(assign, Assignment)
        assert isinstance(assign.target, Variable)
        assert assign.target.name == "x"
        assert isinstance(assign.value, Literal)
        assert assign.value.value == 42

    def test_array_access_assignment(self):
        """Test parsing: arr[0] = 42;"""
        ast = self._parse("lowkey arr: num[]; arr[0] = 42;")

        expr_stmt = ast.statements[1]
        assign = expr_stmt.expression
        assert isinstance(assign, Assignment)
        assert isinstance(assign.target, ArrayAccess)
        assert assign.target.array.name == "arr"
        assert isinstance(assign.target.index, Literal)
        assert assign.target.index.value == 0

    def test_print_statement(self):
        """Test parsing: spill_tea(x);"""
        ast = self._parse("lowkey x: num = 42; spill_tea(x);")

        print_stmt = ast.statements[1]
        assert isinstance(print_stmt, PrintStmt)
        assert len(print_stmt.arguments) == 1
        assert isinstance(print_stmt.arguments[0], Variable)
        assert print_stmt.arguments[0].name == "x"

    def test_print_multiple_args(self):
        """Test parsing: spill_tea(a, b, c);"""
        ast = self._parse("lowkey a: num = 1; spill_tea(1, 2, 3);")

        print_stmt = ast.statements[1]
        assert isinstance(print_stmt, PrintStmt)
        assert len(print_stmt.arguments) == 3

    def test_if_statement(self):
        """Test parsing: sus (x > 10) { ... }"""
        ast = self._parse("""
            lowkey x: num = 42;
            sus (x > 10) {
                spill_tea(1);
            }
        """)

        if_stmt = ast.statements[1]
        assert isinstance(if_stmt, IfStmt)
        assert isinstance(if_stmt.condition, Binary)
        assert if_stmt.condition.operator == ">"
        assert if_stmt.then_branch is not None

    def test_if_else_statement(self):
        """Test parsing: sus (x > 10) { ... } deadass { ... }"""
        ast = self._parse("""
            sus (no_cap) {
                spill_tea(1);
            } deadass {
                spill_tea(0);
            }
        """)

        if_stmt = ast.statements[0]
        assert isinstance(if_stmt, IfStmt)
        assert if_stmt.else_branch is not None

    def test_while_statement(self):
        """Test parsing: keep_yapping (x > 0) { ... }"""
        ast = self._parse("""
            lowkey x: num = 5;
            keep_yapping (x > 0) {
                x = x - 1;
            }
        """)

        while_stmt = ast.statements[1]
        assert isinstance(while_stmt, WhileStmt)
        assert isinstance(while_stmt.condition, Binary)
        assert while_stmt.condition.operator == ">"

    def test_for_statement(self):
        """Test parsing: yapping_through (init; cond; update) { ... }"""
        ast = self._parse("""
            yapping_through (lowkey i: num = 0; i < 5; i = i + 1) {
                spill_tea(i);
            }
        """)

        for_stmt = ast.statements[0]
        assert isinstance(for_stmt, ForStmt)
        assert for_stmt.init is not None
        assert for_stmt.condition is not None
        assert for_stmt.update is not None
        assert isinstance(for_stmt.condition, Binary)

    def test_for_statement_no_init(self):
        """Test for-loop with empty init."""
        ast = self._parse("""
            yapping_through (; i < 5; i = i + 1) {
                spill_tea(i);
            }
        """)
        for_stmt = ast.statements[0]
        assert isinstance(for_stmt, ForStmt)
        assert for_stmt.init is None
        assert for_stmt.condition is not None

    def test_return_statement(self):
        """Test parsing: slay x + y;"""
        ast = self._parse("vibe_check add(a: num, b: num) { slay a + b; }")

        func = ast.statements[0]
        assert isinstance(func, FuncDecl)
        assert isinstance(func.body.statements[0], ReturnStmt)
        return_stmt = func.body.statements[0]
        assert isinstance(return_stmt.value, Binary)
        assert return_stmt.value.operator == "+"

    def test_return_no_value(self):
        """Test parsing: slay;"""
        ast = self._parse("vibe_check void_func() { slay; }")

        func = ast.statements[0]
        return_stmt = func.body.statements[0]
        assert isinstance(return_stmt, ReturnStmt)
        assert return_stmt.value is None

    def test_break_statement(self):
        """Test parsing: bestie;"""
        ast = self._parse("keep_yapping (no_cap) { bestie; }")

        while_stmt = ast.statements[0]
        break_stmt = while_stmt.body.statements[0]
        assert isinstance(break_stmt, BreakStmt)

    def test_continue_statement(self):
        """Test parsing: its_giving;"""
        ast = self._parse("keep_yapping (no_cap) { its_giving; }")

        while_stmt = ast.statements[0]
        continue_stmt = while_stmt.body.statements[0]
        assert isinstance(continue_stmt, ContinueStmt)

    def test_function_declaration(self):
        """Test parsing function declarations."""
        ast = self._parse("vibe_check add(a: num, b: num) { slay a + b; }")

        assert len(ast.statements) == 1
        func = ast.statements[0]
        assert isinstance(func, FuncDecl)
        assert func.name == "add"
        assert len(func.params) == 2
        assert func.params[0].name == "a"
        assert func.params[0].type_name == "num"

    def test_binary_operators(self):
        """Test binary operator parsing."""
        source = """
            lowkey a: num = 1 + 2;
            lowkey b: num = 3 - 4;
            lowkey c: num = 5 * 6;
            lowkey d: num = 7 / 8;
            lowkey e: num = 10 % 3;
        """
        ast = self._parse(source)

        ops = ['+', '-', '*', '/', '%']
        for i, op in enumerate(ops):
            var_decl = ast.statements[i]
            binary = var_decl.initializer
            assert isinstance(binary, Binary)
            assert binary.operator == op

    def test_comparison_operators(self):
        """Test comparison operator parsing."""
        ast = self._parse("sus (1 < 2 && 3 > 4 && 5 <= 6 && 7 >= 8) { }")

        condition = ast.statements[0].condition
        # The condition is a tree of Binary nodes connected by AND
        assert isinstance(condition, Binary)
        assert condition.operator == "&&"

    def test_boolean_literals(self):
        """Test parsing no_cap (true) and fr_fr (false)."""
        ast = self._parse("lowkey t: num = no_cap; lowkey f: num = fr_fr;")

        true_lit = ast.statements[0].initializer
        false_lit = ast.statements[1].initializer

        assert isinstance(true_lit, Literal)
        assert true_lit.value is True
        assert isinstance(false_lit, Literal)
        assert false_lit.value is False

    def test_array_literal(self):
        """Test parsing array literals."""
        ast = self._parse("lowkey nums: num[] = [1, 2, 3];")

        var_decl = ast.statements[0]
        assert isinstance(var_decl.initializer, ArrayLiteral)
        assert len(var_decl.initializer.elements) == 3

    def test_array_access(self):
        """Test parsing array access."""
        ast = self._parse("lowkey arr: num[]; lowkey x: num = arr[0];")

        access = ast.statements[1].initializer
        assert isinstance(access, ArrayAccess)
        assert access.array.name == "arr"
        assert isinstance(access.index, Literal)
        assert access.index.value == 0

    def test_unary_operators(self):
        """Test unary operator parsing."""
        ast = self._parse("lowkey x: num = !no_cap; lowkey y: num = -42;")

        not_expr = ast.statements[0].initializer
        assert isinstance(not_expr, Unary)
        assert not_expr.operator == "!"

        neg_expr = ast.statements[1].initializer
        assert isinstance(neg_expr, Unary)
        assert neg_expr.operator == "-"

    def test_nested_expressions(self):
        """Test parsing nested expressions."""
        ast = self._parse("lowkey x: num = (1 + 2) * (3 - 4);")

        expr = ast.statements[0].initializer
        assert isinstance(expr, Binary)
        assert expr.operator == "*"

    def test_function_call_as_statement(self):
        """Test parsing function calls as statements."""
        ast = self._parse("vibe_check greet(name: txt) { } greet(\"world\");")

        # First statement is function declaration, second is function call
        assert isinstance(ast.statements[0], FuncDecl)
        assert isinstance(ast.statements[1], ExprStmt)
        func_call = ast.statements[1].expression
        assert isinstance(func_call, FuncCall)
        assert func_call.name == "greet"
        assert len(func_call.arguments) == 1

    def test_else_if_chain(self):
        """Test parsing: sus (...) { } deadass sus (...) { } deadass { }"""
        ast = self._parse("""
            lowkey x: num = 5;
            sus (x > 10) {
                spill_tea(1);
            } deadass sus (x > 3) {
                spill_tea(2);
            } deadass {
                spill_tea(3);
            }
        """)

        if_stmt = ast.statements[1]
        assert isinstance(if_stmt, IfStmt)
        assert isinstance(if_stmt.else_branch, IfStmt)
        assert isinstance(if_stmt.else_branch.then_branch, Block)
        assert isinstance(if_stmt.else_branch.else_branch, Block)

    def test_comments_ignored(self):
        """Test that comments don't interfere with parsing."""
        ast = self._parse("""
            // this is a comment
            lowkey x: num = 42; // inline comment
            spill_tea(x);
        """)

        assert len(ast.statements) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])