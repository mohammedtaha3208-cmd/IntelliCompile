
import re

KEYWORDS = {"int", "float", "if", "else", "print"}

TOKEN_SPECIFICATION = [
    ("NUMBER",   r"\d+"),
    ("ID",       r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("OPERATOR", r"[+\-*/=<>]"),
    ("SYMBOL",   r"[(){};,]"),
    ("SKIP",     r"[ \t]+"),
    ("NEWLINE",  r"\n"),
    ("MISMATCH", r"."),
]

def tokenize(source_code):
    tokens = []
    errors = []

    pattern = "|".join(
        f"(?P<{name}>{regex})"
        for name, regex in TOKEN_SPECIFICATION
    )

    line_number = 1

    for match in re.finditer(pattern, source_code):
        token_type = match.lastgroup
        value = match.group()

        if token_type == "NUMBER":
            tokens.append(("NUMBER", value, line_number))

        elif token_type == "ID":
            if value in KEYWORDS:
                tokens.append(("KEYWORD", value, line_number))
            else:
                tokens.append(("IDENTIFIER", value, line_number))

        elif token_type in ("OPERATOR", "SYMBOL"):
            tokens.append((token_type, value, line_number))

        elif token_type == "NEWLINE":
            line_number += 1

        elif token_type == "MISMATCH":
            errors.append(
                f"Invalid character '{value}' at line {line_number}"
            )

    return tokens, errors
