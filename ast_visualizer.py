
def generate_ast_dot(ast):

    lines = [
        "digraph AST {",
        '    graph [bgcolor="white"];',
        '    node [shape=box, style="rounded,filled", '
        'fillcolor="lightblue", color="steelblue"];',
        '    edge [color="gray"];'
    ]

    counter = [0]

    def add_node(node, parent=None):

        if not isinstance(node, tuple):
            return

        counter[0] += 1
        node_id = f"node{counter[0]}"

        node_type = node[0]

        if node_type == "PROGRAM":
            label = "PROGRAM"

        elif node_type == "DECLARE":
            label = f"DECLARE\\n{node[1]} {node[2]}"

        elif node_type == "ASSIGN":
            label = f"ASSIGN\\n{node[1]}"

        elif node_type == "PRINT":
            label = "PRINT"

        elif node_type == "BINOP":
            label = f"OPERATOR\\n{node[1]}"

        elif node_type == "NUMBER":
            label = f"NUMBER\\n{node[1]}"

        elif node_type == "VARIABLE":
            label = f"VARIABLE\\n{node[1]}"

        else:
            label = node_type

        label = label.replace('"', '\\"')

        lines.append(
            f'    {node_id} [label="{label}"];'
        )

        if parent:
            lines.append(
                f"    {parent} -> {node_id};"
            )

        # Process child nodes
        if node_type == "PROGRAM":
            for statement in node[1]:
                add_node(statement, node_id)

        elif node_type == "DECLARE":
            if len(node) > 3 and node[3] is not None:
                add_node(node[3], node_id)

        elif node_type == "ASSIGN":
            add_node(node[2], node_id)

        elif node_type == "PRINT":
            add_node(node[1], node_id)

        elif node_type == "BINOP":
            add_node(node[2], node_id)
            add_node(node[3], node_id)

    add_node(ast)

    lines.append("}")

    return "\n".join(lines)
