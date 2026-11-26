
class IntermediateCodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, ast):
        for statement in ast[1]:
            self.generate_statement(statement)

        return self.code

    def generate_statement(self, statement):
        kind = statement[0]

        if kind == "DECLARE":
            name = statement[2]
            value = self.generate_expression(statement[3])
            self.code.append(f"{name} = {value}")

        elif kind == "ASSIGN":
            name = statement[1]
            value = self.generate_expression(statement[2])
            self.code.append(f"{name} = {value}")

        elif kind == "PRINT":
            value = self.generate_expression(statement[1])
            self.code.append(f"PRINT {value}")

    def generate_expression(self, expression):
        kind = expression[0]

        if kind == "NUMBER":
            return str(expression[1])

        if kind == "VARIABLE":
            return expression[1]

        if kind == "BINOP":
            operator = expression[1]
            left = self.generate_expression(expression[2])
            right = self.generate_expression(expression[3])

            temp = self.new_temp()
            self.code.append(
                f"{temp} = {left} {operator} {right}"
            )
            return temp
