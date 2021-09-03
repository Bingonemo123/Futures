import math 
import sympy

def manualPdf():
    r = sympy.symbols('r')
    h = 0
    t = 0
    a = math.factorial(h+t+1)
    b = math.factorial(h) *  math.factorial(t)
    d = a//b
    form = (r**h)*((1-r)**t)
    prec = 0.001
    start = 0
    end = 0.45
    fs =  sum([prec * form.subs(r, start + prec * x ) for x in range(int((end-start)//prec))]) 
    start = 0.55
    end = 1
    ss = sum([prec * form.subs(r, start + prec * x ) for x in range(int((end-start)//prec))]) 
    return d*(fs + ss)

print(manualPdf())