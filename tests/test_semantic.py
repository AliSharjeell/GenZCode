"""Tests for the Semantic Analyzer module."""

import pytest
from src.lexer import tokenize
from src.parser.parser import Parser
from src.semantic.analyzer import SemanticAnalyzer
from src.semantic.symbol_table import SemanticError


class TestSemanticAnalyzer:
    """Test cases for semantic analysis."""

    def _analyze(self, source: str):
        """Helper to parse and analyze source code."""
        tokens = tokenize(source)
        ast = Parser(tokens).parse()
        analyzer = SemanticAnalyzer()
        return analyzer.analyze(ast), analyzer

    def test_variable_declaration(self):
        """Test variable declaration adds to symbol table."""
        _, analyzer = self._analyze("lowkey x: num = 42;")

        symbol = analyzer.symbol_table.lookup("x")
        assert symbol is not None
        assert symbol.type_info.base_type == "num"
        assert not symbol.type_info.is_array

    def test_string_variable(self):
        """Test string variable declaration."""
        _, analyzer = self._analyze('lowkey name: txt = "hello";')

        symbol = analyzer.symbol_table.lookup("name")
        assert symbol is not None
        assert symbol.type_info.base_type == "txt"

    def test_array_variable(self):
        """Test array variable declaration."""
        _, analyzer = self._analyze("lowkey nums: num[];")

        symbol = analyzer.symbol_table.lookup("nums")
        assert symbol is not None
        assert symbol.type_info.is_array
        assert symbol.type_info.base_type == "num"

    def test_function_declaration(self):
        """Test function declaration adds to global scope."""
        _, analyzer = self._analyze("vibe_check add(a: num, b: num) { slay a + b; }")

        symbol = analyzer.symbol_table.lookup_function("add")
        assert symbol is not None
        assert symbol.is_function
        assert len(symbol.param_types) == 2

    def test_undefined_variable(self):
        """Test that undefined variables raise an error."""
        with pytest.raises(SemanticError) as exc_info:
            self._analyze("lowkey x: num = y;")
        assert "Undefined variable" in str(exc_info.value)

    def test_redefined_variable(self):
        """Test that redefining a variable in same scope raises an error."""
        with pytest.raises(SemanticError) as exc_info:
            self._analyze("lowkey x: num = 1; lowkey x: num = 2;")
        assert "already defined" in str(exc_info.value)

    def test_scope_isolation(self):
        """Test that variables in different scopes don't conflict."""
        source = '''
            lowkey x: num = 1;
            sus (no_cap) {
                lowkey x: num = 2;
            }
        '''
        _, analyzer = self._analyze(source)

        # Both should exist
        assert analyzer.symbol_table.lookup("x") is not None

    def test_function_parameters_in_scope(self):
        """Test that function parameters are in scope inside the function."""
        source = "vibe_check add(a: num, b: num) { lowkey c: num = a + b; slay c; }"
        _, analyzer = self._analyze(source)

        # Function should be defined
        assert analyzer.symbol_table.lookup_function("add") is not None

    def test_type_mismatch_number_to_string(self):
        """Test that assigning number to string raises an error."""
        with pytest.raises(SemanticError) as exc_info:
            self._analyze('lowkey x: txt = 42;')
        assert "Type mismatch" in str(exc_info.value)

    def test_type_mismatch_string_to_number(self):
        """Test that assigning string to number raises an error."""
        with pytest.raises(SemanticError) as exc_info:
            self._analyze('lowkey x: num = "hello";')
        assert "Type mismatch" in str(exc_info.value)

    def test_break_outside_loop(self):
        """Test that break outside loop raises an error."""
        with pytest.raises(SemanticError) as exc_info:
            self._analyze("bestie;")
        assert "must be inside a loop" in str(exc_info.value)

    def test_continue_outside_loop(self):
        """Test that continue outside loop raises an error."""
        with pytest.raises(SemanticError) as exc_info:
            self._analyze("its_giving;")
        assert "must be inside a loop" in str(exc_info.value)

    def test_return_outside_function(self):
        """Test that return outside function raises an error."""
        with pytest.raises(SemanticError) as exc_info:
            self._analyze("slay 42;")
        assert "outside of function" in str(exc_info.value)

    def test_undefined_function(self):
        """Test that calling undefined function raises an error."""
        source = "vibe_check main() { greet(); }"
        with pytest.raises(SemanticError) as exc_info:
            self._analyze(source)
        assert "Undefined function" in str(exc_info.value)

    def test_function_wrong_argument_count(self):
        """Test that wrong argument count raises an error."""
        source = '''
            vibe_check add(a: num, b: num) { slay a + b; }
            vibe_check main() { add(1); }
        '''
        with pytest.raises(SemanticError) as exc_info:
            self._analyze(source)
        assert "expects 2 arguments" in str(exc_info.value)

    def test_function_wrong_argument_type(self):
        """Test that wrong argument type raises an error."""
        source = '''
            vibe_check greet(name: txt) { }
            vibe_check main() { greet(42); }
        '''
        with pytest.raises(SemanticError) as exc_info:
            self._analyze(source)
        assert "expected txt" in str(exc_info.value)

    def test_array_index_must_be_numeric(self):
        """Test that non-numeric array index raises an error."""
        source = "lowkey arr: num[]; lowkey x: num = arr[\"hello\"];"
        with pytest.raises(SemanticError) as exc_info:
            self._analyze(source)
        assert "Array index must be numeric" in str(exc_info.value)

    def test_arithmetic_on_strings(self):
        """Test that arithmetic on strings raises an error."""
        source = 'lowkey a: txt = "hello"; lowkey b: txt = a * 2;'
        with pytest.raises(SemanticError) as exc_info:
            self._analyze(source)
        assert "Cannot perform" in str(exc_info.value)

    def test_negate_string(self):
        """Test that negating a string raises an error."""
        source = 'lowkey x: txt = "hello"; lowkey y: num = -x;'
        with pytest.raises(SemanticError) as exc_info:
            self._analyze(source)
        assert "Cannot negate" in str(exc_info.value)

    def test_valid_program(self):
        """Test a valid complete program."""
        source = '''
            vibe_check factorial(n: num) {
                sus (n <= 1) {
                    slay 1;
                } deadass {
                    lowkey result: num = n * 2;
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
        _, analyzer = self._analyze(source)

        # Check functions are defined
        assert analyzer.symbol_table.lookup_function("factorial") is not None
        assert analyzer.symbol_table.lookup_function("main") is not None

    def test_string_concatenation(self):
        """Test that string concatenation is allowed."""
        source = 'lowkey a: txt = "hello"; lowkey b: txt = " " + "world";'
        _, analyzer = self._analyze(source)

        assert analyzer.symbol_table.lookup("a") is not None
        assert analyzer.symbol_table.lookup("b") is not None

    def test_boolean_operations(self):
        """Test boolean operations work."""
        source = "lowkey x: num = no_cap && fr_fr;"
        _, analyzer = self._analyze(source)

        assert analyzer.symbol_table.lookup("x") is not None

    def test_comparison_operations(self):
        """Test comparison operations work."""
        source = "lowkey x: num = 1 < 2;"
        _, analyzer = self._analyze(source)

        assert analyzer.symbol_table.lookup("x") is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])