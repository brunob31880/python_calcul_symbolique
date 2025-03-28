# symcalc/core.py
from __future__ import annotations
from functools import reduce

class Expr:
   def diff(self,var:str) -> "Expr":
       raise NotImplementedError()
   def eval(self, env: dict[str, float]) -> float:
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
   def eval(self, env: dict[str, float]) -> float:
        if self.name in env:
            return env[self.name]
        else:
            raise ValueError(f"Variable '{self.name}' non fournie dans env")

class Const(Expr):
   def __init__(self,value:int):
       self.value=value
   def diff(self,var:str) -> "Expr":
       return Const(0)
   def simplify(self) -> Expr:
    return self
   def __str__(self):
       return str(self.value)
   def eval(self, env: dict[str, float]) -> float:
       return self.value
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
       from .simplify import simplify_add
       return simplify_add(Add(left, right))
   def __str__(self):
       return f"({self.value1}) + ({self.value2})"
   def eval(self, env: dict[str, float]) -> float:
        return self.value1.eval(env) + self.value2.eval(env)
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
    def eval(self, env: dict[str, float]) -> float:
        return self.value1.eval(env) * self.value2.eval(env)
if __name__ == '__main__':
    expr1=Add(Var("x"),Const(2))
    expr2=Var("x")
    expr= Mul(expr1,expr2)
    print(f"Dérivée de {str(expr)} est {expr.diff('x').simplify()}")

