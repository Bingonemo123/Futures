import random
import pandas as pd
import streamlit as st


pseudo_data = [ (random.choice((True, False)), random.randint(0, 600)) for k in range(1000000)]    



count_data = {}
for d in pseudo_data:
    count_data[d[0]] = count_data.setdefault(d[0], 0) +  1


transform_data = {}
for d in pseudo_data:
    transform_data[d[0]] = transform_data.setdefault(d[0], 0) +  (-1)**(not d[1])

pd_td = pd.DataFrame(None, index=range(21), columns=range(31))

for x in range(21):
    for y in range(30):
        pd_td[y][x] = transform_data.get(x*30 + y,None)

st.write(pd_td)

percent_data={}
for d in pseudo_data:
    percent_data[d[0]] = percent_data.setdefault(d[0], 0) +  d[1]
for c in count_data:
    percent_data[c] = round(percent_data[c]/count_data[c]*100, 1)

pd_pd = pd.DataFrame(None, index=range(21), columns=range(31))

for x in range(21):
    for y in range(30):
        pd_pd[y][x] = percent_data.get(x*30 + y,None)



st.write(pd_pd)
