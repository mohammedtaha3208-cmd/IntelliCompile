
class CodeOptimizer:
    def __init__(self):
        self.optimized_code = []
        self.constants = {}

    def optimize(self, code):
        self.constants = {}
        propagated_code = []

        # Constant Folding and Constant Propagation
        for instruction in code:
            parts = instruction.split()

            if len(parts) == 3 and parts[1] == "=":
                target, _, value = parts

                if value in self.constants:
                    value = str(self.constants[value])

                if value.isdigit():
                    self.constants[target] = int(value)
                else:
                    self.constants.pop(target, None)

                propagated_code.append(
                    f"{target} = {value}"
                )

            elif len(parts) == 5 and parts[1] == "=":
                target, _, left, operator, right = parts

                left = str(self.constants.get(left, left))
                right = str(self.constants.get(right, right))

                if left.isdigit() and right.isdigit():
                    a, b = int(left), int(right)

                    if operator == "+":
                        result = a + b
                    elif operator == "-":
                        result = a - b
                    elif operator == "*":
                        result = a * b
                    elif operator == "/" and b != 0:
                        result = a // b
                    else:
                        propagated_code.append(instruction)
                        continue

                    self.constants[target] = result
                    propagated_code.append(
                        f"{target} = {result}"
                    )
                else:
                    self.constants.pop(target, None)
                    propagated_code.append(
                        f"{target} = {left} {operator} {right}"
                    )

            elif parts[0] == "PRINT":
                 propagated_code.append(instruction)

        # Dead-Code Elimination
        used_variables = set()
        final_code = []

        for instruction in reversed(propagated_code):
            parts = instruction.split()

            if parts[0] == "PRINT":
                used_variables.add(parts[1])
                final_code.append(instruction)

            elif len(parts) >= 3 and parts[1] == "=":
                target = parts[0]

                if target in used_variables:
                    final_code.append(instruction)

                    if len(parts) == 5:
                        used_variables.update(
                            [parts[2], parts[4]]
                        )
                    else:
                        used_variables.add(parts[2])

        self.optimized_code = list(reversed(final_code))
        return self.optimized_code
