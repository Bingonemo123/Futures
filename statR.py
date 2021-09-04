
import pandas as pd
import streamlit as st
import pickle
import math 
import sympy
real_data = pickle.load(open("data.pkl", 'rb'))   

st.set_page_config(page_title="Real statistics",layout='wide')
default_width = None
count_data = {}
for d in real_data:
    count_data[d[1]] = count_data.setdefault(d[1], 0) +  1
pd_cd = pd.DataFrame(None, index=range(21), columns=range(30))
for x in range(21):
    for y in range(30):
        pd_cd[y][x] = count_data.get(x*30 + y,None)
st.write("# Real Data")
st.write('number of data:' + str(len(real_data)))
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
my_bar = st.progress(0)
pd_ppcd =  pd.DataFrame(None, index=range(21), columns=range(30))
try:
    pd_ppcd = pd.read_pickle('./Archive/popdf' + str(len(real_data)) + '.pkl')
    my_bar.progress(100)
    st.write('Loaded from archive')
except:
    with st.empty():
        for x in range(21):
            for y in range(30):
                my_bar.progress((x*30 + y)/629 )
                try:
                    c = round(Pdf(x, y) * 100, 3)
                    st.write(str(x*30 + y) + '('+ str(x) + ',' + str(y) + ')' + 
                    " :: " +  str (c))
                    pd_ppcd[y][x] = format(c, '.2f')
                except:
                    print(x, y)
                    st.write(str(x*30 + y) + '('+ str(x) + ',' + str(y) + ')' + 
                    " :: " +  'E')
                    pd_ppcd[y][x] = 'E'

    pd_ppcd.to_pickle('./Archive/popdf' + str(len(real_data)) + '.pkl')

st.dataframe(pd_ppcd, width=default_width)

'''---------------------------------------------------------------------------------------'''
limit = 80
uplimit = []
for x in range(21):
    for y in range(30):
        if float(pd_ppcd[y][x]) >= limit:
            uplimit.append((x, y, x*30 + y,  pd_ppcd[y][x], pd_cd[y][x], pd_pd[y][x]))

pd_showdata = pd.DataFrame(uplimit, columns=['x', 'y','index',' percentage', 'Total occurence', 'real %'])
st.write(pd_showdata)

soto = sum([h[4] for h in uplimit if h[4] != None])    #sumoftotaloccurences
st.write('Sum of Total occurences: ' + str(soto))
ap = [float(h[3]) for h in uplimit if h[2] != None]
ap = sum(ap)/ len(ap) # average percantage
st.write('Average percantage: ' + str(ap))
rp = [float(h[3]) * h[4] for h in uplimit if (h[3] != None and h[4] != None) ]
rp = sum(rp)/soto # relative percantage
st.write('Relative percantage: ' + str(rp))