import pandas as pd
import sympy 
import math
import streamlit as st
import numpy as np
from scipy import stats

class Stat:
    def __init__(self, data):
        self.real_data = data


    def transpose(self, position):
        self.sandwictch = []
        for d in self.real_data:
            try:
                self.sandwictch.append((d[0], d[position]))
            except:
                continue
        self.real_data = self.sandwictch

    def totals(self):
        self.count_data = {}
        for d in self.real_data:
            self.count_data[d[1]] = self.count_data.setdefault(d[1], 0) +  1

    def winlosediff (self):
        transform_data = {}
        for d in self.real_data:
            transform_data[d[1]] = transform_data.setdefault(d[1], 0) +  (-1)**(not d[0])

    def numberofwins(self):
        self.True_data={}
        for d in self.real_data:
            self.True_data[d[1]] = self.True_data.setdefault(d[1], 0) +  d[0]

    def realpercetange(self):
        self.percent_data = {}
        for c in self.count_data:
            self.percent_data[c] = 100 * self.True_data[c]/self.count_data[c]

    def scipicdf(self, h, t):
        return  1 - stats.beta.cdf(0.625, h + 1, t + 1) + stats.beta.cdf(0.375, h + 1, t + 1)

    def scipp(self):
        my_bar = st.progress(0)
        self.ppcd = {}
        with st.empty():
            progress_count = 0 
            for d in self.count_data:
                try:
                    h = self.True_data.get(d, 0)
                    t = self.count_data.get(d, 0) - h
                    c = round(self.scipicdf(h, t) * 100, 3)
                    st.write(str(d) + " :: " +  str (c))
                    self.ppcd[d] = format(c, '.2f')
                except Exception as e:
                    print(d, e)
                    st.write(str(d) +" :: " +  'E')
                    self.ppcd[d] = 'E'
                progress_count += 1
                my_bar.progress(progress_count/len(self.count_data) )

    def showdata (self):
        limit = 80
        self.uplimit = []
        for d in self.count_data:
            if float(self.ppcd[d]) >= limit and (float(self.percent_data[d]) > 62.5 or float(self.percent_data[d]) < 37.5):
                self.uplimit.append((d, self.ppcd[d], self.count_data[d], self.percent_data[d], self.True_data[d]))

        self.pd_showdata = pd.DataFrame(self.uplimit, columns=['index',' percentage', 'Total occurence', 'real %', 'wins'])


    def shownumbers (self):
        self.soto = sum([h[2] for h in self.uplimit if h[2] != None])    #sumoftotaloccurences
        self.sow = sum(h[4] for h in self.uplimit if (h[3] > 50 and h[4] != None)) + sum(h[2] - h[4] for h in self.uplimit if (h[3] < 50 and (h[2] != None or h[4] != None))) 
        self.ap = [float(h[3]) for h in self.uplimit if h[2] != None]
        try:
            self.ap = sum(self.ap)/ len(self.ap) # average percantage
        except ZeroDivisionError:
            self.ap = 0
        self.rp = [float(h[3]) * h[4] for h in self.uplimit if (h[3] != None and h[4] != None) ]
        try:
            self.rp = sum(self.rp)/self.soto # relative percantage
        except ZeroDivisionError:
            self.rp = 0
        try:
            self.ab = self.sow/self.soto
        except ZeroDivisionError:
            self.ab = 0

    def EV (self, perc, total):
        x, n, p ,m, k, j = sympy.symbols("x n p m k j")
        bi = sympy.functions.combinatorial.factorials.binomial(k, j)
        exp = bi *(x*((n+m)*p)**(k-j)*((n-1)*(1-p))**(j))/n**k
        bisum = sympy.Sum(exp, (j, 0, k))
        subsbisum = bisum.subs([(n,2),(p, perc), (m,0.6), (k, total)])
        return subsbisum.doit().subs(x, 1)

    def EVF(self):
        x, n, p ,m, k, j = sympy.symbols("x n p m k j")
        bi = sympy.functions.combinatorial.factorials.binomial(k, j)
        exp = bi *(x*((n+m)*p)**(k-j)*((n-1)*(1-p))**(j))/n**k
        bisum = sympy.Sum(exp, (j, 0, k))
        return bisum

    def calculations(self):
        self.totals()
        self.winlosediff()
        self.numberofwins()
        self.realpercetange()
        self.scipp()
        self.showdata()
        self.shownumbers()

    def strmlt (self):
        st.dataframe(self.pd_showdata)
        st.write('Sum of Total occurences: ' + str(self.soto))
        st.write('Sum of wins: ' + str(self.sow))
        st.write('Average percantage: ' + str(self.ap))
        st.write('Relative percantage: ' + str(self.rp))
        st.write('Abs %: ' + str(self.ab * 100))
        st.write('% of abs % being above 62.5 % :' + str((1 - stats.beta.cdf(0.625, self.sow + 1, self.soto-self.sow + 1))* 100))
        # st.write('Expected value : ' + str( EV(sow/soto, soto)))

        '''
        if 'chart_data' not in  st.session_state:
            st.session_state['chart_data'] = pd.DataFrame([float(self.EV(t, self.soto)) for t in np.round(np.linspace(0.625, 0.630, 10), decimals=4) ], index = np.round(np.linspace(0.625, 0.630, 10), decimals=4), columns = ['p'] )
        st.bar_chart(st.session_state['chart_data'])
        st.write(self.EVF())

        recept = {}
        for f in  self.uplimit:
            if f[5] > 50:
                recept[f[2]] = 'call'
            else:
                recept[f[2]] = 'put'

        if st.button('Show recept'):
            st.write(recept)
        '''





