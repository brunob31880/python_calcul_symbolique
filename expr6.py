# ou utiliser forward_reference pour flatten_add et simplify_add
from __future__ import annotations
from functools import reduce

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

# Entre guillemet forwad reference
class Expr:
   def diff(self,var:str) -> "Expr":
       raise NotImplementedError()
class Var(Expr):
   def __init__(self,name:str):
       self.name=name
   def diff(self,var:str) -> "Expr":
       return Const(1) if self.name == var else Const(0)
   def simplify(self) -> Expr:
    return self
   def __str__(self):
    return self.name
class Const(Expr):
   def __init__(self,value:int):
       self.value=value
   def diff(self,var:str) -> "Expr":
       return Const(0)
   def simplify(self) -> Expr:
    return self
   def __str__(self):
       return str(self.value)
class Add(Expr):
   def __init__(self,value1:Expr,value2:Expr):
       self.value1=value1
       self.value2=value2
   def diff(self,var:str) -> "Expr":
       return Add(self.value1.diff(var),self.value2.diff(var))
   def simplify(self) -> Expr:
       left = self.value1.simplify()
       right = self.value2.simplify()
       if isinstance(left, Const) and left.value == 0:
           return right
       if isinstance(right, Const) and right.value == 0:
           return left
       return simplify_add(Add(left, right))
   def __str__(self):
       return f"({self.value1}) + ({self.value2})"
class Mul(Expr):
    def __init__(self,value1:Expr,value2:Expr):
       self.value1=value1
       self.value2=value2
    def diff(self,var:str) -> "Expr":
       return Add(Mul(self.value1.diff(var),self.value2),Mul(self.value2.diff(var),self.value1))
    def simplify(self) -> Expr:
       left = self.value1.simplify()
       right = self.value2.simplify()
       if isinstance(left, Const) and left.value == 0:
           return Const(0)
       if isinstance(right, Const) and right.value == 0:
           return Const(0)
       if isinstance(left, Const) and left.value == 1:
           return right
       if isinstance(right, Const) and right.value == 1:
           return left
       return Mul(left, right)
    def __str__(self):
        return f"({self.value1}) * ({self.value2})"
if __name__ == '__main__':
    expr1=Add(Var("x"),Const(2))
    expr2=Var("x")
    expr= Mul(expr1,expr2)
    print(f"Dérivée de {str(expr)} est {expr.diff('x').simplify()}")

