"""Tests for the Interpreter module."""

import pytest
from src.interpreter.interpreter import Interpreter, interpret, InterpreterError


class TestInterpreter:
    """Test cases for the interpreter."""

    def _run(self, source: str):
        """Helper to run GenZ source code."""
        return interpret(source, skip_semantic=True)

    def test_hello_world(self, capsys):
        """Test hello world."""
        self._run('spill_tea("hello world");')
        captured = capsys.readouterr()
        assert "hello world" in captured.out

    def test_variable_num(self):
        """Test numeric variable."""
        result = self._run("lowkey x: num = 42;")
        assert result is None

    def test_variable_txt(self):
        """Test string variable."""
        result = self._run('lowkey name: txt = "bruh";')
        assert result is None

    def test_print_variable(self, capsys):
        """Test printing variable."""
        self._run("lowkey x: num = 42; spill_tea(x);")
        captured = capsys.readouterr()
        assert "42" in captured.out

    def test_boolean_true(self):
        """Test no_cap (true)."""
        self._run("lowkey x: num = no_cap;")
        # Check no error

    def test_boolean_false(self):
        """Test fr_fr (false)."""
        self._run("lowkey x: num = fr_fr;")

    def test_arithmetic_add(self):
        """Test addition."""
        self._run("lowkey x: num = 1 + 2;")
        self._run("lowkey x: num = 1 + 2; spill_tea(x);")

    def test_arithmetic_subtract(self):
        """Test subtraction."""
        self._run("lowkey x: num = 5 - 3;")

    def test_arithmetic_multiply(self):
        """Test multiplication."""
        self._run("lowkey x: num = 3 * 4;")

    def test_arithmetic_divide(self):
        """Test division."""
        self._run("lowkey x: num = 10 / 2;")

    def test_arithmetic_modulo(self):
        """Test modulo."""
        self._run("lowkey x: num = 10 % 3;")

    def test_comparison(self):
        """Test comparison."""
        self._run("lowkey x: num = 1 < 2;")

    def test_logical_and(self):
        """Test logical AND."""
        self._run("lowkey x: num = no_cap && fr_fr;")

    def test_logical_or(self):
        """Test logical OR."""
        self._run("lowkey x: num = no_cap || fr_fr;")

    def test_logical_not(self):
        """Test logical NOT."""
        self._run("lowkey x: num = !no_cap;")

    def test_unary_negation(self):
        """Test unary negation."""
        self._run("lowkey x: num = -42;")

    def test_assignment(self):
        """Test variable assignment."""
        self._run("lowkey x: num = 0; x = 42;")

    def test_if_true(self, capsys):
        """Test if statement with true condition."""
        self._run("sus (no_cap) { spill_tea(1); }")
        captured = capsys.readouterr()
        assert "1" in captured.out

    def test_if_false(self, capsys):
        """Test if statement with false condition."""
        self._run("sus (fr_fr) { spill_tea(1); } deadass { spill_tea(0); }")
        captured = capsys.readouterr()
        assert "0" in captured.out
        assert "1" not in captured.out

    def test_while_loop(self, capsys):
        """Test while loop."""
        self._run("lowkey i: num = 3; keep_yapping (i > 0) { spill_tea(i); i = i - 1; }")
        captured = capsys.readouterr()
        assert "3" in captured.out
        assert "2" in captured.out
        assert "1" in captured.out

    def test_break(self, capsys):
        """Test break statement."""
        self._run("keep_yapping (no_cap) { spill_tea(1); bestie; spill_tea(2); }")
        captured = capsys.readouterr()
        assert "1" in captured.out
        assert "2" not in captured.out

    def test_continue(self, capsys):
        """Test continue statement."""
        # continue skips the rest of the loop body, so nothing should print
        self._run("lowkey i: num = 0; keep_yapping (i < 3) { i = i + 1; its_giving; spill_tea(i); }")
        captured = capsys.readouterr()
        # With i = i + 1 before continue, all iterations hit continue before print
        assert "1" not in captured.out
        assert "2" not in captured.out
        assert "3" not in captured.out

    def test_continue_with_print_after(self, capsys):
        """Test continue statement with print after continue."""
        # print is after continue, so nothing prints
        self._run("lowkey i: num = 0; keep_yapping (i < 3) { i = i + 1; its_giving; spill_tea(i); }")
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_continue_allows_next_iteration(self, capsys):
        """Test that continue allows the next iteration to proceed."""
        # i is incremented BEFORE continue, so when i reaches 3, loop exits
        # Nothing should print because continue is before spill_tea
        self._run("lowkey i: num = 0; keep_yapping (i < 3) { i = i + 1; its_giving; } spill_tea(i);")
        captured = capsys.readouterr()
        assert "3" in captured.out

    def test_function_declaration(self):
        """Test function declaration."""
        self._run("vibe_check add(a: num, b: num) { slay a + b; }")

    def test_function_call(self, capsys):
        """Test function call."""
        self._run("vibe_check greet() { spill_tea(\"hello\"); } greet();")
        captured = capsys.readouterr()
        assert "hello" in captured.out

    def test_function_with_args(self, capsys):
        """Test function with arguments."""
        self._run("vibe_check add(a: num, b: num) { slay a + b; } spill_tea(add(2, 3));")
        captured = capsys.readouterr()
        assert "5" in captured.out

    def test_recursive_function(self, capsys):
        """Test recursive function."""
        self._run("vibe_check factorial(n: num) { sus (n <= 1) { slay 1; } deadass { slay n * factorial(n - 1); } } spill_tea(factorial(5));")
        captured = capsys.readouterr()
        assert "120" in captured.out

    def test_array_literal(self):
        """Test array literal."""
        self._run("lowkey nums: num[] = [1, 2, 3];")

    def test_array_access(self, capsys):
        """Test array access."""
        self._run("lowkey nums: num[] = [10, 20, 30]; spill_tea(nums[0]);")
        captured = capsys.readouterr()
        assert "10" in captured.out

    def test_array_assignment(self, capsys):
        """Test array element assignment."""
        self._run("lowkey arr: num[] = [0]; arr[0] = 42; spill_tea(arr[0]);")
        captured = capsys.readouterr()
        assert "42" in captured.out

    def test_string_concatenation(self, capsys):
        """Test string concatenation."""
        self._run('lowkey a: txt = "hello"; lowkey b: txt = " world"; spill_tea(a + b);')
        captured = capsys.readouterr()
        assert "hello world" in captured.out

    def test_nested_expressions(self):
        """Test nested expressions."""
        self._run("lowkey x: num = (1 + 2) * (3 - 4);")

    def test_scope_isolation(self, capsys):
        """Test variable scope in if block."""
        self._run("lowkey x: num = 1; sus (no_cap) { lowkey x: num = 2; spill_tea(x); } spill_tea(x);")
        captured = capsys.readouterr()
        assert "2" in captured.out
        assert "1" in captured.out

    def test_string_comparison(self):
        """Test string comparison."""
        self._run('lowkey a: txt = "hello"; lowkey b: txt = "hello"; lowkey eq: num = a == b;')

    def test_multiple_statements(self, capsys):
        """Test multiple statements."""
        self._run("lowkey x: num = 1; x = 2; x = 3; spill_tea(x);")
        captured = capsys.readouterr()
        assert "3" in captured.out

    def test_divide_by_zero(self):
        """Test division by zero error."""
        with pytest.raises(InterpreterError) as exc_info:
            self._run("lowkey x: num = 1 / 0;")
        assert "Division by zero" in str(exc_info.value)

    def test_undefined_variable(self):
        """Test undefined variable error."""
        with pytest.raises(InterpreterError) as exc_info:
            self._run("spill_tea(x);")
        assert "Undefined variable" in str(exc_info.value)

    def test_undefined_function(self):
        """Test undefined function error."""
        with pytest.raises(InterpreterError) as exc_info:
            self._run("vibe_check main() { unknown(); }")
        assert "Undefined function" in str(exc_info.value)

    def test_main_function_auto_call(self, capsys):
        """Test that main() is auto-called."""
        self._run("vibe_check main() { spill_tea(\"in main\"); }")
        captured = capsys.readouterr()
        assert "in main" in captured.out

    def test_return_inside_function(self, capsys):
        """Test return statement inside function."""
        self._run("vibe_check get_value() { slay 42; } lowkey x: num = get_value(); spill_tea(x);")
        captured = capsys.readouterr()
        assert "42" in captured.out

    def test_return_no_value(self):
        """Test return without value."""
        self._run("vibe_check foo() { slay; }")

    def test_builtin_len(self, capsys):
        """Test len() builtin function."""
        self._run("lowkey arr: num[] = [1, 2, 3]; spill_tea(len(arr));")
        captured = capsys.readouterr()
        assert "3" in captured.out

    def test_builtin_range(self):
        """Test range() builtin function."""
        self._run("lowkey r: num[] = range(5);")

    def test_builtin_abs(self):
        """Test abs() builtin function."""
        self._run("lowkey x: num = abs(-5);")

    def test_builtin_pow(self):
        """Test pow() builtin function."""
        self._run("lowkey x: num = pow(2, 3);")

    def test_else_if_chain(self, capsys):
        """Test else-if chain: sus ... deadass sus ... deadass."""
        self._run("""
            lowkey x: num = 5;
            sus (x > 10) {
                spill_tea("big");
            } deadass sus (x > 3) {
                spill_tea("medium");
            } deadass {
                spill_tea("small");
            }
        """)
        captured = capsys.readouterr()
        assert "medium" in captured.out
        assert "big" not in captured.out
        assert "small" not in captured.out

    def test_else_if_falls_to_else(self, capsys):
        """Test that else-if falls through to else when no condition matches."""
        self._run("""
            lowkey x: num = 1;
            sus (x > 10) {
                spill_tea("big");
            } deadass sus (x > 5) {
                spill_tea("medium");
            } deadass {
                spill_tea("small");
            }
        """)
        captured = capsys.readouterr()
        assert "small" in captured.out
        assert "big" not in captured.out
        assert "medium" not in captured.out

    def test_for_loop(self, capsys):
        """Test yapping_through for-loop."""
        self._run("yapping_through (lowkey i: num = 0; i < 3; i = i + 1) { spill_tea(i); }")
        captured = capsys.readouterr()
        assert "0" in captured.out
        assert "1" in captured.out
        assert "2" in captured.out

    def test_for_loop_with_break(self, capsys):
        """Test for-loop with bounce (break)."""
        self._run("yapping_through (lowkey i: num = 0; i < 10; i = i + 1) { sus (i == 3) { bounce; } spill_tea(i); }")
        captured = capsys.readouterr()
        assert "0" in captured.out

    def test_for_loop_with_continue(self, capsys):
        """Test for-loop with next_up (continue)."""
        self._run("yapping_through (lowkey i: num = 0; i < 5; i = i + 1) { sus (i == 2) { next_up; } spill_tea(i); }")
        captured = capsys.readouterr()
        assert "0" in captured.out
        assert "1" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])