
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.errors = []

    def analyze(self, ast):
        for statement in ast[1]:
            self.check_statement(statement)

        return self.symbol_table, self.errors

    def check_statement(self, statement):
        kind = statement[0]

        if kind == "DECLARE":
            data_type, name, value = statement[1:]

            if name in self.symbol_table:
                self.errors.append(
                    f"Variable '{name}' already declared"
                )
                return

            value_type = self.check_expression(value)

            if value_type and value_type != data_type:
                self.errors.append(
                    f"Type mismatch in declaration of '{name}'"
                )
                return

            self.symbol_table[name] = data_type

        elif kind == "ASSIGN":
            name, value = statement[1:]

            if name not in self.symbol_table:
                self.errors.append(
                    f"Variable '{name}' not declared"
                )
                return

            value_type = self.check_expression(value)

            if value_type and value_type != self.symbol_table[name]:
                self.errors.append(
                    f"Type mismatch in assignment to '{name}'"
                )

        elif kind == "PRINT":
            self.check_expression(statement[1])

    def check_expression(self, expression):
        kind = expression[0]

        if kind == "NUMBER":
            return "int"

        if kind == "VARIABLE":
            name = expression[1]

            if name not in self.symbol_table:
                self.errors.append(
                    f"Variable '{name}' not declared"
                )
                return None

            return self.symbol_table[name]

        if kind == "BINOP":
            left_type = self.check_expression(expression[2])
            right_type = self.check_expression(expression[3])

            if left_type != right_type:
                self.errors.append(
                    "Type mismatch in expression"
                )
                return None

            return left_type

        return None
