import ast
import math
import operator as op

OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.Mod: op.mod,
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "ln": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "abs": abs,
    "round": round,
    "factorial": math.factorial,
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def _normalize_expression(expression: str) -> str:
    if not isinstance(expression, str):
        raise ValueError("expression must be a string")

    cleaned = expression.strip()
    cleaned = cleaned.replace("×", "*").replace("÷", "/")
    cleaned = cleaned.replace("π", "pi")
    cleaned = cleaned.replace("^", "**")
    return cleaned


def calculator(argument):
    if isinstance(argument, dict):
        expression = argument.get("expression")
    else:
        expression = argument

    if not isinstance(expression, str):
        return "Calculator error: expression must be a string"

    try:
        normalized = _normalize_expression(expression)
        tree = ast.parse(normalized, mode="eval")
        result = _evaluate(tree.body)
        return str(result)
    except Exception as e:
        return f"Calculator error: {str(e)}"


def _evaluate(node):
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.Name):
        if node.id in CONSTANTS:
            return CONSTANTS[node.id]
        raise ValueError(f"Unknown name: {node.id}")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in OPERATORS:
            raise ValueError("Unsupported operator")
        return OPERATORS[op_type](_evaluate(node.left), _evaluate(node.right))

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in OPERATORS:
            raise ValueError("Unsupported unary operator")
        return OPERATORS[op_type](_evaluate(node.operand))

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function call")

        func_name = node.func.id.lower()
        if func_name not in FUNCTIONS:
            raise ValueError(f"Unsupported function: {func_name}")

        args = [_evaluate(arg) for arg in node.args]
        return FUNCTIONS[func_name](*args)

    raise ValueError("Unsupported expression")


if __name__ == "__main__":
    print(calculator("25*18"))
    print(calculator("(245+89)/2"))
    print(calculator("sin(pi/2)"))
    print(calculator("2^10"))