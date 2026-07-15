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
    ast.Mod: op.mod
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "exp": math.exp,
    "abs": abs,
    "round": round,
}

def calculator(expression):
    try:
        tree = ast.parse(expression, mode='eval')
        result = _evaluate(tree.body)
        return str(result)
    except Exception as e:
        return f"Calculator error: {str(e)}"
    
def _evaluate(node):
    if isinstance(node, ast.Constant):
        return node.value
    
    elif isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](
            _evaluate(node.left),
            _evaluate(node.right)
        )
    elif isinstance(node, ast.UnaryOp):
        return OPERATORS[type(node.op)](
            _evaluate(node.operand)
        )
    
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalide function call")
        
        func_name = node.func.id

        if func_name not in FUNCTIONS:
            raise ValueError(f"Unsupported Function: {func_name}")
        
        args = [_evaluate(arg) for arg in node.args]

        return FUNCTIONS[func_name](*args)
    raise ValueError("UNSUPPORTED EXPRESSION")


if __name__ == "__main__":
    print(calculator("25*18"))
    print(calculator("(245+89)/2"))