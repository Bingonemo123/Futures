import pandas as pd
import streamlit as st
import numpy as np
import math 
import random
import sympy
real_data = [ (np.random.choice((True, False), p=[0.624, 1-0.624]), random.randint(0, 600)) for k in range(37954)]    

st.set_page_config(page_title="Pseudo stat",layout='wide')
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
    end = 0.375
    fs = d*sum([prec * form.subs(r, start + prec * k ) for k in range(int((end-start)//prec))])
    start =  0.625
    end = 1
    ss = d*sum([prec * form.subs(r, start + prec * k ) for k in range(int((end-start)//prec))])
    return fs + ss

st.write("Percentages of Percentages")
my_bar = st.progress(0)
pd_ppcd =  pd.DataFrame(None, index=range(21), columns=range(30))
try:
    # raise SyntaxError
    pd_ppcd = pd.read_pickle('./Archive/popdfpseudo' + str(len(real_data)) + '.pkl')
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

    pd_ppcd.to_pickle('./Archive/popdfpseudo' + str(len(real_data)) + '.pkl')

st.dataframe(pd_ppcd, width=default_width)

'''---------------------------------------------------------------------------------------'''
left_column, right_column = st.columns(2)

with left_column:
    limit = 80
    uplimit = []
    for x in range(21):
        for y in range(30):
            if float(pd_ppcd[y][x]) >= limit and (float(pd_pd[y][x]) > 62.5 or float(pd_pd[y][x]) < 37.5):
                uplimit.append((x, y, x*30 + y,  pd_ppcd[y][x], pd_cd[y][x], pd_pd[y][x], pd_td[y][x]))

    pd_showdata = pd.DataFrame(uplimit, columns=['x', 'y','index',' percentage', 'Total occurence', 'real %', 'wins'])
    st.write(pd_showdata)

    soto = sum([h[4] for h in uplimit if h[4] != None])    #sumoftotaloccurences
    st.write('Sum of Total occurences: ' + str(soto))
    sow = sum(h[6] for h in uplimit if h[5] > 50) + sum(h[4] - h[6] for h in uplimit if h[5] < 50) 
    st.write('Sum of wins: ' + str(sow))
    ap = [float(h[3]) for h in uplimit if h[2] != None]
    ap = sum(ap)/ len(ap) # average percantage
    st.write('Average percantage: ' + str(ap))
    rp = [float(h[3]) * h[4] for h in uplimit if (h[3] != None and h[4] != None) ]
    rp = sum(rp)/soto # relative percantage
    st.write('Relative percantage: ' + str(rp))
    st.write('Abs %: ' + str(sow/soto * 100))

    def NPdf(h, t):
        r = sympy.symbols('r')
        a = math.factorial(h+t+1)
        b = math.factorial(h) *  math.factorial(t) 
        d = a//b
        form = (r**h)*((1-r)**t)
        prec = 0.001
        start =  0.625
        end = 1
        ss = d*sum([prec * form.subs(r, start + prec * k ) for k in range(int((end-start)//prec))])
        return ss

    st.write('% of abs % being above 62.5 % :' + str(NPdf(sow, soto-sow)* 100))

    def EV (perc, total):
        x, n, p ,m, k, j = sympy.symbols("x n p m k j")
        bi = sympy.functions.combinatorial.factorials.binomial(k, j)
        exp = bi *(x*((n+m)*p)**(k-j)*((n-1)*(1-p))**(j))/n**k
        bisum = sympy.Sum(exp, (j, 0, k))
        subsbisum = bisum.subs([(n,2),(p, perc), (m,0.6), (k, total)])
        return subsbisum.doit().subs(x, 1)

    st.write('Expected value : ' + str( EV(sow/soto, soto)))

with right_column:
    chart_data = pd.DataFrame([float(EV(t, soto)) for t in np.round(np.linspace(0.625, 0.630, 10), decimals=4) ], index = np.round(np.linspace(0.625, 0.630, 10), decimals=4), columns = ['p'] )
    st.bar_chart(chart_data)
    def EVF():
        x, n, p ,m, k, j = sympy.symbols("x n p m k j")
        bi = sympy.functions.combinatorial.factorials.binomial(k, j)
        exp = bi *(x*((n+m)*p)**(k-j)*((n-1)*(1-p))**(j))/n**k
        bisum = sympy.Sum(exp, (j, 0, k))
        return bisum
    st.write(EVF())
'''---------------------------------------------------------------------------------------'''

recept = {}
for f in  uplimit:
    if f[5] > 50:
        recept[f[2]] = 'call'
    else:
        recept[f[2]] = 'put'

if st.button('Show recept'):
    st.write(recept)