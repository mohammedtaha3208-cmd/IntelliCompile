
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def consume(self, expected=None):
        token = self.current()

        if token is None:
            raise SyntaxError("Unexpected end of input")

        if expected and token[1] != expected:
            raise SyntaxError(
                f"Expected '{expected}', found '{token[1]}'"
            )

        self.position += 1
        return token

    def parse(self):
        statements = []

        while self.current() is not None:
            statements.append(self.statement())

        return ("PROGRAM", statements)

    def statement(self):
        token = self.current()

        if token[1] in ("int", "float"):
            return self.declaration()

        if token[0] == "IDENTIFIER":
            return self.assignment()

        if token[1] == "print":
            return self.print_statement()

        raise SyntaxError(f"Invalid statement: {token[1]}")

    def declaration(self):
        data_type = self.consume()[1]
        name = self.consume()

        if name[0] != "IDENTIFIER":
            raise SyntaxError("Expected variable name")

        self.consume("=")
        value = self.expression()
        self.consume(";")

        return ("DECLARE", data_type, name[1], value)

    def assignment(self):
        name = self.consume()[1]
        self.consume("=")
        value = self.expression()
        self.consume(";")

        return ("ASSIGN", name, value)

    def print_statement(self):
        self.consume("print")
        self.consume("(")
        value = self.expression()
        self.consume(")")
        self.consume(";")

        return ("PRINT", value)

    def expression(self):
        node = self.term()

        while self.current() and self.current()[1] in ("+", "-"):
            operator = self.consume()[1]
            right = self.term()
            node = ("BINOP", operator, node, right)

        return node

    def term(self):
        node = self.factor()

        while self.current() and self.current()[1] in ("*", "/"):
            operator = self.consume()[1]
            right = self.factor()
            node = ("BINOP", operator, node, right)

        return node

    def factor(self):
        token = self.current()

        if token is None:
            raise SyntaxError("Expected an expression")

        if token[0] == "NUMBER":
            self.consume()
            return ("NUMBER", int(token[1]))

        if token[0] == "IDENTIFIER":
            self.consume()
            return ("VARIABLE", token[1])

        if token[1] == "(":
            self.consume("(")
            node = self.expression()
            self.consume(")")
            return node

        raise SyntaxError(f"Invalid expression: {token[1]}")


def parse(tokens):
    parser = Parser(tokens)
    return parser.parse()
