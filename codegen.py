
class CodeGenerator:
    def generate(self, intermediate_code):
        bytecode = []

        for instruction in intermediate_code:
            parts = instruction.split()

            if parts[0] == "PRINT":
                value = parts[1]

                if value.isdigit():
                    bytecode.append(f"PUSH {value}")
                else:
                    bytecode.append(f"LOAD {value}")

                bytecode.append("PRINT")

            elif len(parts) == 3 and parts[1] == "=":
                target, _, value = parts

                if value.isdigit():
                    bytecode.append(f"PUSH {value}")
                else:
                    bytecode.append(f"LOAD {value}")

                bytecode.append(f"STORE {target}")

            elif len(parts) == 5 and parts[1] == "=":
                target, _, left, operator, right = parts

                for operand in (left, right):
                    if operand.isdigit():
                        bytecode.append(f"PUSH {operand}")
                    else:
                        bytecode.append(f"LOAD {operand}")

                operations = {
                    "+": "ADD",
                    "-": "SUB",
                    "*": "MUL",
                    "/": "DIV"
                }

                bytecode.append(operations[operator])
                bytecode.append(f"STORE {target}")

        return bytecode
