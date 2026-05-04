"""Tests for the Code Generator module."""

import pytest
from src.lexer import tokenize
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.generator.generator import CodeGenerator


class TestCodeGenerator:
    """Test cases for code generation."""

    def _generate(self, source: str) -> str:
        """Helper to parse, analyze, and generate code."""
        tokens = tokenize(source)
        ast = Parser(tokens).parse()
        SemanticAnalyzer().analyze(ast)  # Validate before generating
        return CodeGenerator().generate(ast)

    def test_hello_world(self):
        """Test generating a simple hello world."""
        source = 'spill_tea("hello world");'
        code = self._generate(source)
        assert 'print("hello world")' in code

    def test_variable_declaration_num(self):
        """Test generating numeric variable declaration."""
        source = "lowkey x: num = 42;"
        code = self._generate(source)
        assert "x = 42" in code

    def test_variable_declaration_txt(self):
        """Test generating string variable declaration."""
        source = 'lowkey name: txt = "bruh";'
        code = self._generate(source)
        assert 'name = "bruh"' in code

    def test_variable_declaration_no_init(self):
        """Test generating variable without initializer."""
        source = "lowkey x: num;"
        code = self._generate(source)
        assert "x = 0" in code

    def test_string_variable_no_init(self):
        """Test generating string variable without initializer."""
        source = "lowkey name: txt;"
        code = self._generate(source)
        assert 'name = ""' in code

    def test_boolean_true(self):
        """Test generating true (no_cap)."""
        source = "lowkey x: num = no_cap;"
        code = self._generate(source)
        assert "x = True" in code

    def test_boolean_false(self):
        """Test generating false (fr_fr)."""
        source = "lowkey x: num = fr_fr;"
        code = self._generate(source)
        assert "x = False" in code

    def test_binary_arithmetic(self):
        """Test generating binary arithmetic."""
        source = "lowkey x: num = 1 + 2;"
        code = self._generate(source)
        assert "x = (1 + 2)" in code

    def test_binary_subtraction(self):
        """Test generating subtraction."""
        source = "lowkey x: num = 5 - 3;"
        code = self._generate(source)
        assert "x = (5 - 3)" in code

    def test_binary_multiplication(self):
        """Test generating multiplication."""
        source = "lowkey x: num = 3 * 4;"
        code = self._generate(source)
        assert "x = (3 * 4)" in code

    def test_binary_division(self):
        """Test generating division."""
        source = "lowkey x: num = 10 / 2;"
        code = self._generate(source)
        assert "x = (10 / 2)" in code

    def test_comparison_operators(self):
        """Test generating comparison operators."""
        source = "lowkey x: num = 1 < 2;"
        code = self._generate(source)
        assert "x = (1 < 2)" in code

    def test_logical_operators(self):
        """Test generating logical operators."""
        source = "lowkey x: num = no_cap && fr_fr;"
        code = self._generate(source)
        assert "True and False" in code

    def test_unary_not(self):
        """Test generating unary NOT."""
        source = "lowkey x: num = !no_cap;"
        code = self._generate(source)
        assert "not True" in code

    def test_unary_negation(self):
        """Test generating unary negation."""
        source = "lowkey x: num = -42;"
        code = self._generate(source)
        assert "x = (-42)" in code

    def test_assignment(self):
        """Test generating variable assignment."""
        source = "lowkey x: num = 0; x = 42;"
        code = self._generate(source)
        assert "x = 42" in code

    def test_print_statement(self):
        """Test generating print statement."""
        source = "lowkey x: num = 42; spill_tea(x);"
        code = self._generate(source)
        assert "print(x)" in code

    def test_print_multiple_args(self):
        """Test generating print with multiple arguments."""
        source = "spill_tea(1, 2, 3);"
        code = self._generate(source)
        assert "print(1, 2, 3)" in code

    def test_if_statement(self):
        """Test generating if statement."""
        source = "sus (no_cap) { spill_tea(1); }"
        code = self._generate(source)
        assert "if True:" in code
        assert "print(1)" in code

    def test_if_else_statement(self):
        """Test generating if-else statement."""
        source = "sus (no_cap) { spill_tea(1); } deadass { spill_tea(0); }"
        code = self._generate(source)
        assert "if True:" in code
        assert "else:" in code

    def test_while_statement(self):
        """Test generating while loop."""
        source = "lowkey x: num = 0; keep_yapping (x < 10) { spill_tea(x); }"
        code = self._generate(source)
        assert "while x < 10:" in code
        assert "print(x)" in code

    def test_break_statement(self):
        """Test generating break statement."""
        source = "keep_yapping (no_cap) { bestie; }"
        code = self._generate(source)
        assert "break" in code

    def test_continue_statement(self):
        """Test generating continue statement."""
        source = "keep_yapping (no_cap) { its_giving; }"
        code = self._generate(source)
        assert "continue" in code

    def test_return_statement(self):
        """Test generating return statement."""
        source = "vibe_check add(a: num, b: num) { slay a + b; }"
        code = self._generate(source)
        assert "def add(a, b):" in code
        assert "return (a + b)" in code

    def test_return_no_value(self):
        """Test generating return without value."""
        source = "vibe_check foo() { slay; }"
        code = self._generate(source)
        assert "def foo():" in code
        assert "return" in code

    def test_function_call(self):
        """Test generating function call."""
        source = "vibe_check greet() { } greet();"
        code = self._generate(source)
        assert "def greet():" in code
        assert "greet()" in code

    def test_function_with_args(self):
        """Test generating function with arguments."""
        source = "vibe_check add(a: num, b: num) { slay a + b; }"
        code = self._generate(source)
        assert "def add(a, b):" in code

    def test_array_literal(self):
        """Test generating array literal."""
        source = "lowkey nums: num[] = [1, 2, 3];"
        code = self._generate(source)
        assert "nums = [1, 2, 3]" in code

    def test_array_access(self):
        """Test generating array access."""
        source = "lowkey arr: num[]; lowkey x: num = arr[0];"
        code = self._generate(source)
        assert "arr = []" in code
        assert "x = arr[0]" in code

    def test_array_assignment(self):
        """Test generating array element assignment."""
        source = "lowkey arr: num[]; arr[0] = 42;"
        code = self._generate(source)
        assert "arr[0] = 42" in code

    def test_nested_expressions(self):
        """Test generating nested expressions."""
        source = "lowkey x: num = (1 + 2) * (3 - 4);"
        code = self._generate(source)
        assert "x = ((1 + 2) * (3 - 4))" in code

    def test_complex_program(self):
        """Test generating a complete program."""
        source = '''
            vibe_check factorial(n: num) {
                sus (n <= 1) {
                    slay 1;
                } deadass {
                    slay n * factorial(n - 1);
                }
            }

            vibe_check main() {
                lowkey x: num = 5;
                keep_yapping (x > 0) {
                    spill_tea(x);
                    x = x - 1;
                }
            }
        '''
        code = self._generate(source)
        assert "def factorial(n):" in code
        assert "def main():" in code
        assert "while x > 0:" in code
        assert "print(x)" in code


if __name__ == "__main__":
    pytest.main([__file__, "-v"])