from src.lexer import Lexer
from src.parser import Parser



INTEGER = "INTEGER"
PLUS = "PLUS"
MINUS = "MINUS"
MULTIPLY = "MULTIPLY"
DIVIDE = "DIVIDE"
LPAREN = "LPAREN"
RPAREN = "RPAREN"
FUNC = "FUNC"     
EOF = "EOF"


class Tokens:
    def __init__(self, type_, token):
        self.type = type_
        self.token = token

    def __repr__(self):
        return f"{self.type} {self.token}"

import string

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Tokens("INTEGER", int(result))

    def identifier(self):
        """Collect function names like sin, cos, tan, factorial"""
        result = ""
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return Tokens("FUNC", result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return self.integer()
            if self.current_char.isalpha():
                return self.identifier()
            if self.current_char == '+':
                self.advance()
                return Tokens("PLUS", '+')
            if self.current_char == '-':
                self.advance()
                return Tokens("MINUS", '-')
            if self.current_char == '*':
                self.advance()
                return Tokens("MULTIPLY", '*')
            if self.current_char == '/':
                self.advance()
                return Tokens("DIVIDE", '/')
            if self.current_char == '(':
                self.advance()
                return Tokens("LPAREN", '(')
            if self.current_char == ')':
                self.advance()
                return Tokens("RPAREN", ')')
            raise Exception(f"Invalid character: {self.current_char}")
        return Tokens("EOF", None)


import math

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Unexpected token: {self.current_token}")

    def factor(self):
        token = self.current_token
        if token.type == "INTEGER":
            self.eat("INTEGER")
            return token.token
        elif token.type == "FUNC":
            func_name = token.token
            self.eat("FUNC")
            self.eat("LPAREN")
            arg = self.expr()
            self.eat("RPAREN")
            return self.apply_function(func_name, arg)
        elif token.type == "LPAREN":
            self.eat("LPAREN")
            result = self.expr()
            self.eat("RPAREN")
            return result

    def apply_function(self, name, arg):
        if name == "sin":
            return math.sin(arg)
        elif name == "cos":
            return math.cos(arg)
        elif name == "tan":
            return math.tan(arg)
        elif name == "factorial":
            return math.factorial(int(arg))
        elif name == "pow":
            return arg ** 2 
        else:
            raise Exception(f"Unknown function: {name}")

    def term(self):
        result = self.factor()
        while self.current_token.type in ("MULTIPLY", "DIVIDE"):
            token = self.current_token
            if token.type == "MULTIPLY":
                self.eat("MULTIPLY")
                result *= self.factor()
            elif token.type == "DIVIDE":
                self.eat("DIVIDE")
                result /= self.factor()
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type in ("PLUS", "MINUS"):
            token = self.current_token
            if token.type == "PLUS":
                self.eat("PLUS")
                result += self.term()
            elif token.type == "MINUS":
                self.eat("MINUS")
                result -= self.term()
        return result

if __name__ == "__main__":
    while True:
        try:
            text = input("calc> ")
            if not text:
                continue
            lexer = Lexer(text)
            parser = Parser(lexer)
            result = parser.expr()
            print(result)
        except Exception as e:
            print("Error:", e)
