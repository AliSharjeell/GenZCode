"""Token types for GenZ/Brainrot language."""

from enum import Enum, auto
from typing import Optional


class TokenType(Enum):
    """All token types for the GenZ language."""

    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENT = auto()

    # Keywords
    LOWKEY = auto()      # variable declaration
    NUM = auto()         # numeric type
    TXT = auto()         # string type
    SUS = auto()         # if
    DEADASS = auto()     # else
    KEEP_YAPPING = auto()  # while
    SPILL_TEA = auto()   # print
    VIBE_CHECK = auto()  # function
    SLAY = auto()        # return
    BESTIE = auto()      # break
    ITS_GIVING = auto()  # continue
    NO_CAP = auto()      # true
    FR_FR = auto()       # false

    # Operators
    PLUS = auto()        # +
    MINUS = auto()       # -
    STAR = auto()        # *
    SLASH = auto()       # /
    PERCENT = auto()     # %
    ASSIGN = auto()      # =
    EQ = auto()          # ==
    NEQ = auto()         # !=
    LT = auto()          # <
    GT = auto()          # >
    LTE = auto()         # <=
    GTE = auto()         # >=
    AND = auto()         # &&
    OR = auto()          # ||
    NOT = auto()         # !

    # Punctuation
    LBRACE = auto()      # {
    RBRACE = auto()       # }
    LPAREN = auto()      # (
    RPAREN = auto()       # )
    LBRACKET = auto()     # [
    RBRACKET = auto()     # ]
    SEMI = auto()         # ;
    COMMA = auto()        # ,
    COLON = auto()        # :

    # Special
    EOF = auto()
    COMMENT = auto()     # // ... (ignored)


KEYWORDS = {
    'lowkey': TokenType.LOWKEY,
    'num': TokenType.NUM,
    'txt': TokenType.TXT,
    'sus': TokenType.SUS,
    'deadass': TokenType.DEADASS,
    'keep_yapping': TokenType.KEEP_YAPPING,
    'spill_tea': TokenType.SPILL_TEA,
    'vibe_check': TokenType.VIBE_CHECK,
    'slay': TokenType.SLAY,
    'bestie': TokenType.BESTIE,
    'its_giving': TokenType.ITS_GIVING,
    'no_cap': TokenType.NO_CAP,
    'fr_fr': TokenType.FR_FR,
}


class Token:
    """Represents a single token in the source code."""

    def __init__(
        self,
        type: TokenType,
        lexeme: str,
        literal: Optional[object] = None,
        line: int = 0,
        column: int = 0,
    ):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.column = column

    def __repr__(self) -> str:
        return f"Token({self.type.name}, '{self.lexeme}', {self.literal})"