# symcalc/simplify.py
from __future__ import annotations
from functools import reduce
from .core import Expr, Add, Const, Var, Mul

def flatten_add(expr: Expr) -> list[Expr]:
    if isinstance(expr, Add):
        return flatten_add(expr.value1) + flatten_add(expr.value2)
    else:
        return [expr]

def simplify_add(expr: Add):
    terms = flatten_add(expr)
    variables = {}
    const_sum = 0

    for term in terms:
        if isinstance(term, Const):
            const_sum += term.value
        elif isinstance(term, Var):
            key = term.name
            variables[key] = variables.get(key, 0) + 1
        else:
            # Pour Mul, Add, etc. — à traiter plus tard
            pass

    # Crée les parties variables
    var_terms = [
        Mul(Const(count), Var(name)) if count > 1 else Var(name)
        for name, count in variables.items()
    ]
 
    # Ajoute la constante si elle n’est pas nulle
    if const_sum != 0:
        var_terms.append(Const(const_sum))

    # Recombine les termes avec Add
    if not var_terms:
        return Const(0)
    else:
        return reduce(lambda a, b: Add(a, b), var_terms)
