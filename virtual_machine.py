
class VirtualMachine:

    def __init__(self):
        self.stack = []
        self.variables = {}
        self.output = []
        self.execution_trace = []

    def execute(self, bytecode):

        self.stack = []
        self.variables = {}
        self.output = []
        self.execution_trace = []

        for step, instruction in enumerate(bytecode, start=1):

            parts = instruction.split()
            operation = parts[0]

            if operation == "PUSH":
                self.stack.append(int(parts[1]))

            elif operation == "LOAD":
                variable = parts[1]

                if variable not in self.variables:
                    raise ValueError(
                        f"Undefined variable: {variable}"
                    )

                self.stack.append(self.variables[variable])

            elif operation == "STORE":
                variable = parts[1]
                self.variables[variable] = self.stack.pop()

            elif operation == "ADD":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)

            elif operation == "SUB":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)

            elif operation == "MUL":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)

            elif operation == "DIV":
                b = self.stack.pop()
                a = self.stack.pop()

                if b == 0:
                    raise ZeroDivisionError(
                        "Division by zero"
                    )

                self.stack.append(a // b)

            elif operation == "PRINT":
                value = self.stack.pop()
                self.output.append(value)

            else:
                raise ValueError(
                    f"Unknown bytecode instruction: {instruction}"
                )

            self.execution_trace.append({
                "Step": step,
                "Instruction": instruction,
                "Stack": str(self.stack.copy()),
                "Variables": str(self.variables.copy()),
                "Output": str(self.output.copy())
            })

        return self.output
