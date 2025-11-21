INTEGER = "INTEGER"
PLUS    = "PLUS"
MINUS   = "MINUS"
MUL     = "MUL"
DIV     = "DIV"
LPAREN  = "LPAREN"
RPAREN  = "RPAREN"
EOF     = "EOF"


class Tokens:
    def __init__(self, type_, token):
        self.type = type_
        self.token = token

    def __repr__(self):
        return f"{self.type} {self.token}"



class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        """Move to the next character"""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None  # End of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Collect multi-digit integers"""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Tokens("INTEGER", int(result))

    def get_next_token(self):
        """Return the next token"""
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.integer()

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



class LexerError(Exception): pass
class ParserError(Exception): pass