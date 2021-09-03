
import pandas as pd
import streamlit as st
import pickle
import math 
import sympy
real_data = pickle.load(open("data.pkl", 'rb'))   
default_width = 25
count_data = {}
for d in real_data:
    count_data[d[1]] = count_data.setdefault(d[1], 0) +  1
pd_cd = pd.DataFrame(None, index=range(21), columns=range(30))
for x in range(21):
    for y in range(30):
        pd_cd[y][x] = count_data.get(x*30 + y,None)
st.write("# Real Data")
st.write("Total numbers")
st.dataframe(pd_cd, width=default_width)
'''---------------------------------------------------------------------------------------'''

transform_data = {}
for d in real_data:
    transform_data[d[1]] = transform_data.setdefault(d[1], 0) +  (-1)**(not d[0])

pd_td = pd.DataFrame(None, index=range(21), columns=range(30))

for x in range(21):
    for y in range(30):
        pd_td[y][x] = transform_data.get(x*30 + y,None)
st.write('Win lose difference')
st.dataframe(pd_td, width=default_width)

'''---------------------------------------------------------------------------------------'''

True_data={}
for d in real_data:
    True_data[d[1]] = True_data.setdefault(d[1], 0) +  d[0]

pd_td = pd.DataFrame(None, index=range(21), columns=range(30))
for x in range(21):
    for y in range(30):
        pd_td[y][x] = True_data.get(x*30 + y,None)

st.write("Number of Trues")
st.dataframe(pd_td, width=default_width)
'''---------------------------------------------------------------------------------------'''
percent_data = {}
for c in count_data:
    percent_data[c] = True_data[c]/count_data[c]

pd_pd = pd.DataFrame(None, index=range(21), columns=range(30))

for x in range(21):
    for y in range(30):
        pd_pd[y][x] = round(percent_data.get(x*30 + y,0)*100, 3)

st.write("Percentages")
st.dataframe(pd_pd, width=default_width)

'''---------------------------------------------------------------------------------------'''

pd_cpd = pd.DataFrame(None, index=range(21), columns=range(30))

def Pdf(x, y):
    r = sympy.symbols('r')
    h = True_data.get(x*30 + y, 0)
    t = count_data.get(x*30 + y, 0) - h
    a = math.factorial(h+t+1)
    b = math.factorial(h) *  math.factorial(t) 
    d = a//b
    form = (r**h)*((1-r)**t)
    prec = 0.001
    start = 0
    end = 0.325
    fs = d*sum([prec * form.subs(r, start + prec * x ) for x in range(int((end-start)//prec))])
    start =  0.625
    end = 1
    ss = d*sum([prec * form.subs(r, start + prec * x ) for x in range(int((end-start)//prec))])
    return fs + ss

st.write("Percentages of Percentages")
st.dataframe(pd_cpd, width=default_width)
for x in range(21):
    for y in range(30):
        try:
            pd_cpd[y][x] =  Pdf(x, y)
        except:
            print(x, y)
            pd_cpd[y][x] = 'E'