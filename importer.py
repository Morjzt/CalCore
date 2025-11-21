from src.lexer import Lexer
from src.parser import Parser


def evaluate(expression):
    lexer = Lexer(expression)
    parser = Parser(lexer)
    return parser.expr()
