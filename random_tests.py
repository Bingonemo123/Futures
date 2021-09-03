import math 
import sympy

def Pdf():
    r = sympy.symbols('r')
    h = True_data.get(x*30 + y, 0)
    t = count_data.get(x*30 + y, 0) - h
    a = Decimal(math.factorial(h+t+1))
    b = Decimal( math.factorial(h) *  math.factorial(t) )
    d = a/b
    return d*(r**h)*((1-r)**t)



Cpdf = Pdf(x, y)
print(sympy.integrate(Cpdf, (r, 0.375, 0.625))

