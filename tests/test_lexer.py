"""Tests for the Lexer module."""

import pytest
from src.lexer.lexer import Lexer, LexerError
from src.lexer.tokens import TokenType


class TestLexer:
    """Test cases for the Lexer."""

    def test_numbers(self):
        """Test numeric literal tokenization."""
        lexer = Lexer("42 3.14 100")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].literal == 42
        assert tokens[1].type == TokenType.NUMBER
        assert tokens[1].literal == 3.14
        assert tokens[2].type == TokenType.NUMBER
        assert tokens[2].literal == 100
        assert tokens[3].type == TokenType.EOF

    def test_strings(self):
        """Test string literal tokenization."""
        lexer = Lexer('"hello world"')
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.STRING
        assert tokens[0].literal == "hello world"
        assert tokens[1].type == TokenType.EOF

    def test_keywords(self):
        """Test keyword tokenization."""
        source = "lowkey sus deadass keep_yapping spill_tea vibe_check slay bestie its_giving no_cap fr_fr num txt"
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        expected = [
            TokenType.LOWKEY, TokenType.SUS, TokenType.DEADASS,
            TokenType.KEEP_YAPPING, TokenType.SPILL_TEA, TokenType.VIBE_CHECK,
            TokenType.SLAY, TokenType.BESTIE, TokenType.ITS_GIVING,
            TokenType.NO_CAP, TokenType.FR_FR, TokenType.NUM, TokenType.TXT
        ]

        for i, exp in enumerate(expected):
            assert tokens[i].type == exp

        assert tokens[-1].type == TokenType.EOF

    def test_identifiers(self):
        """Test identifier tokenization."""
        lexer = Lexer("x myVar _private123")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.IDENT
        assert tokens[0].lexeme == "x"
        assert tokens[1].type == TokenType.IDENT
        assert tokens[1].lexeme == "myVar"
        assert tokens[2].type == TokenType.IDENT
        assert tokens[2].lexeme == "_private123"

    def test_operators(self):
        """Test operator tokenization."""
        lexer = Lexer("+ - * / % = == != < > <= >= && || !")
        tokens = lexer.tokenize()

        expected = [
            TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH,
            TokenType.PERCENT, TokenType.ASSIGN, TokenType.EQ, TokenType.NEQ,
            TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE,
            TokenType.AND, TokenType.OR, TokenType.NOT
        ]

        for i, exp in enumerate(expected):
            assert tokens[i].type == exp

    def test_punctuation(self):
        """Test punctuation tokenization."""
        lexer = Lexer("{ } ( ) [ ] ; , :")
        tokens = lexer.tokenize()

        expected = [
            TokenType.LBRACE, TokenType.RBRACE, TokenType.LPAREN, TokenType.RPAREN,
            TokenType.LBRACKET, TokenType.RBRACKET, TokenType.SEMI, TokenType.COMMA,
            TokenType.COLON
        ]

        for i, exp in enumerate(expected):
            assert tokens[i].type == exp

    def test_comments(self):
        """Test that comments are properly skipped."""
        lexer = Lexer("42 // this is a comment\n100")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].literal == 42
        assert tokens[1].type == TokenType.NUMBER
        assert tokens[1].literal == 100
        assert tokens[2].type == TokenType.EOF

    def test_whitespace(self):
        """Test that whitespace is properly handled."""
        lexer = Lexer("   42\t\n100   ")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].literal == 42
        assert tokens[1].type == TokenType.NUMBER
        assert tokens[1].literal == 100

    def test_full_sample(self):
        """Test tokenizing a full sample program."""
        source = '''
            lowkey x: num = 42;
            lowkey name: txt = "bruh";
            spill_tea(x);
            sus (x > 10) {
                spill_tea("big number fr fr");
            }
        '''
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # Check some key tokens
        assert tokens[0].type == TokenType.LOWKEY
        assert tokens[1].type == TokenType.IDENT
        assert tokens[2].type == TokenType.COLON
        assert tokens[3].type == TokenType.NUM
        assert tokens[4].type == TokenType.ASSIGN
        assert tokens[5].type == TokenType.NUMBER

    def test_unterminated_string(self):
        """Test that unterminated strings raise an error."""
        lexer = Lexer('"hello world')
        with pytest.raises(LexerError) as exc_info:
            lexer.tokenize()
        assert "Unterminated string" in str(exc_info.value)

    def test_invalid_character(self):
        """Test that invalid characters raise an error."""
        lexer = Lexer("@#$")
        with pytest.raises(LexerError) as exc_info:
            lexer.tokenize()
        assert "Unexpected character" in str(exc_info.value)

    def test_string_escape_newline(self):
        """Test \\n escape sequence in strings."""
        lexer = Lexer('"hello\\nworld"')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].literal == "hello\nworld"

    def test_string_escape_tab(self):
        """Test \\t escape sequence in strings."""
        lexer = Lexer('"hello\\tworld"')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].literal == "hello\tworld"

    def test_string_escape_backslash(self):
        """Test \\\\ escape sequence in strings."""
        lexer = Lexer('"hello\\\\world"')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].literal == "hello\\world"

    def test_string_escape_quote(self):
        """Test \\\" escape sequence in strings."""
        lexer = Lexer('"hello\\"world\\""')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].literal == 'hello"world"'

    def test_string_escape_carriage_return(self):
        """Test \\r escape sequence in strings."""
        lexer = Lexer('"hello\\rworld"')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].literal == "hello\rworld"

    def test_string_mixed_escapes(self):
        """Test multiple escape sequences in one string."""
        lexer = Lexer('"a\\nb\\tc\\\\d"')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].literal == "a\nb\tc\\d"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])