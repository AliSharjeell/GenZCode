"""Parser module for GenZ/Brainrot language."""

from .parser import Parser, ParserError, parse
from .ast import *

__all__ = ['Parser', 'ParserError', 'parse']