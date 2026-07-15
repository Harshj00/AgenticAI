import ast
import math
import operator as op


OPERATOR = {ast.Add: lambda x, y: x + y,
            ast.Sub: lambda x, y: x - y,
            ast.Mult: lambda x, y: x * y,
            ast.Div: lambda x, y: x / y,
            ast.Pow: lambda x, y: x ** y,
            ast.USub: lambda x: -x}

FUNCTIONS = {
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,
    'abs': abs,
    'round': round,
    'max': max,
    'min': min
}


def calculator(expression: str):
    print(f"[calculator] received expression: {expression!r}")
    # sanitize common artifacts: replace ^ with **, remove currency symbols and commas
    expr = expression.replace('^', '**')
    expr = expr.replace('₹', '')
    expr = expr.replace(',', '')

    # remove stray words that are not supported function names
    import re
    words = re.findall(r"[A-Za-z_]+", expr)
    for w in words:
        if w not in FUNCTIONS:
            expr = re.sub(r"\b" + re.escape(w) + r"\b", "", expr)

    expr = expr.strip()
    def _evaluate(node):
        if isinstance(node, ast.Constant):
            return node.value
        
        elif isinstance(node, ast.BinOp):
            return OPERATOR[type(node.op)](
                _evaluate(node.left),
                _evaluate(node.right))
        
        elif isinstance(node, ast.UnaryOp):
            return OPERATOR[type(node.op)](
                _evaluate(node.operand)
                )
        
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Invalid Function ")
            
            func_name = node.func.id
            if func_name not in FUNCTIONS:
                raise ValueError(f"Function '{func_name}' is not supported.")
            
            args = [_evaluate(arg) for arg in node.args]
            return FUNCTIONS[func_name](*args)
        raise ValueError(f"Unsupported expression")
    
    try:
        tree = ast.parse(expr, mode='eval')
        result = _evaluate(tree.body)
        return str(result)
    except Exception as e:
        return f"Calculator Error: {e}"


if __name__ == "__main__":
    print(calculator("25 + 18"))
    print(calculator("(45+15)/3"))  