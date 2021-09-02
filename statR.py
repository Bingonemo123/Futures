import decimal
import pandas as pd
import streamlit as st
import pickle
import math 
from decimal import Decimal
real_data = pickle.load(open("data.pkl", 'rb'))   

count_data = {}
for d in real_data:
    count_data[d[1]] = count_data.setdefault(d[1], 0) +  1
pd_cd = pd.DataFrame(None, index=range(21), columns=range(30))
for x in range(21):
    for y in range(30):
        pd_cd[y][x] = count_data.get(x*30 + y,None)
st.write("# Real Data")
st.write("Total numbers")
st.write(pd_cd)
'''---------------------------------------------------------------------------------------'''

transform_data = {}
for d in real_data:
    transform_data[d[1]] = transform_data.setdefault(d[1], 0) +  (-1)**(not d[0])

pd_td = pd.DataFrame(None, index=range(21), columns=range(30))

for x in range(21):
    for y in range(30):
        pd_td[y][x] = transform_data.get(x*30 + y,None)
st.write('Win lose difference')
st.write(pd_td)

'''---------------------------------------------------------------------------------------'''

True_data={}
for d in real_data:
    True_data[d[1]] = True_data.setdefault(d[1], 0) +  d[0]

pd_td = pd.DataFrame(None, index=range(21), columns=range(30))
for x in range(21):
    for y in range(30):
        pd_td[y][x] = True_data.get(x*30 + y,None)

st.write("Number of Trues")
st.write(pd_td)
'''---------------------------------------------------------------------------------------'''
percent_data = {}
for c in count_data:
    percent_data[c] = True_data[c]/count_data[c]

pd_pd = pd.DataFrame(None, index=range(21), columns=range(30))

for x in range(21):
    for y in range(30):
        pd_pd[y][x] = round(percent_data.get(x*30 + y,0)*100, 3)

st.write("Percentages")
st.write(pd_pd)

'''---------------------------------------------------------------------------------------'''

pd_cpd = pd.DataFrame(None, index=range(21), columns=range(30))

for x in range(21):
    for y in range(30):
        r = Decimal(percent_data.get(x*30 + y, 0))
        h = int(True_data.get(x*30 + y, 0))
        t = count_data.get(x*30 + y, 0) - h
        a = Decimal(math.factorial(h+t+1))
        b = Decimal( math.factorial(h) *  math.factorial(t) )
        d = a/b
        try:
            z = r**h
        except decimal.InvalidOperation:
            z = 1
        q = (1-r)**t
        print(d*z*q)
        pd_cpd[y][x] = int(d *z *q)
st.write("Percentages of Percentages")
st.write(pd_cpd)