from symcalc import Var, Const, Add, Mul

# Exemple : (x + 2) * x
x = Var("x")
expr = Mul(Add(x, Const(2)), x)
print(f"Expr: {expr}")
print(f"Dérivée: {expr.diff('x').simplify()}")
