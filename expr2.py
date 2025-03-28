# Entre guillemet forwad reference
class Expr:
   def diff(self,var:str) -> "Expr":
       raise NotImplementedError()
class Var(Expr):
   def __init__(self,name:str):
       self.name=name
   def diff(self,var:str) -> "Expr":
       return Const(1) if self.name == var else Const(0)
   def __str__(self):
    return self.name
class Const(Expr):
   def __init__(self,value:int):
       self.value=value
   def diff(self,var:str) -> "Expr":
       return Const(0)
   def __str__(self):
       return str(self.value)
class Add(Expr):
   def __init__(self,value1:Expr,value2:Expr):
       self.value1=value1
       self.value2=value2
   def diff(self,var:str) -> "Expr":
       return Add(self.value1.diff(var),self.value2.diff(var))
   def __str__(self):
       return str(self.value1)+"+"+str(self.value2)

if __name__ == '__main__':
    expr1 = Const(1)
    print(f"Dérivée de {expr1} par rapport à x : {expr1.diff('x')}")
    expr2 = Var("x")
    print(f"Dérivée de {expr2} par rapport à x : {expr2.diff('x')}")
    print(f"Dérivée de {expr2} par rapport à y : {expr2.diff('y')}")

    expr3= Add(Var("x"),Const(2))
    print(expr3.diff('x'))
