# Entre guillemet forwad reference
class Expr:
   def diff(self,var:str) -> "Expr":
       raise NotImplementedError()
class Var(Expr):
   def __init__(self,name:str):
       self.name=name
   def diff(self,var:str) -> "Expr":
       if (var==self.name):
           return Const(1)
       else:
           return Const(0)
class Const(Expr):
   def __init__(self,value:int):
       self.value=value
   def diff(self,var:str) -> "Expr":
       return Const(0)
   def __str__(self):
       return str(self.value)
if __name__ == '__main__':
   expr1=Const(1)
   print(f"Dérivée {expr1.diff('x')}")
