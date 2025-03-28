from symcalc import Var, Const, Add, Mul,Expr

def is_operator(c: str) -> bool:
    return c in "+*"

def main_op(s: str) -> int:
    parenthesis = 0
    main_op_index = -1

    for i in range(len(s) - 1, -1, -1):  # parcours de droite à gauche
        c = s[i]
        if c == ')':
            parenthesis += 1
        elif c == '(':
            parenthesis -= 1
        elif parenthesis == 0 and is_operator(c):
            return i  # dès qu'on trouve un opérateur principal, on peut s'arrêter
    return -1  # aucun opérateur trouvé au niveau 0

def parse_expr(s: str) -> Expr:
    s = s.strip()

    if s.startswith("(") and s.endswith(")"):
        s = s[1:-1].strip()

    op_index = main_op(s)

    if op_index != -1:
        op = s[op_index]
        left = parse_expr(s[:op_index])
        right = parse_expr(s[op_index + 1:])

        if op == "+":
            return Add(left, right)
        elif op == "*":
            return Mul(left, right)
        else:
            raise ValueError(f"Opérateur inconnu : {op}")

    # cas simple
    if s.isdigit():
        return Const(int(s))
    elif s.isidentifier():
        return Var(s)
    else:
        raise ValueError(f"Expression invalide : {s}")

if __name__ == "__main__":
    expr = parse_expr("x * (x + 2)")
    print(expr)
    print(expr.diff("x").simplify())
