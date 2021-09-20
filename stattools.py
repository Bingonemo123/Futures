import pandas as pd
import sympy 
import math
import streamlit as st
import numpy as np

class Stat:
    def __init__(self, data):
        self.real_data = data
        
        # totals
        self.pd_td = pd.DataFrame(None, index=range(21), columns=range(30))
        # wins minus loses
        self.pd_wld = pd.DataFrame(None, index=range(21), columns=range(30))
        # number of wins
        self.pd_wd = pd.DataFrame(None, index=range(21), columns=range(30))
        # percentages
        self.pd_pd = pd.DataFrame(None, index=range(21), columns=range(30))
        # percentages of percantages
        self.pd_ppcd =  pd.DataFrame(None, index=range(21), columns=range(30))

    def totals(self):
        self.count_data = {}
        for d in self.real_data:
            self.count_data[d[1]] = self.count_data.setdefault(d[1], 0) +  1
        for x in range(21):
            for y in range(30):
                self.pd_td[y][x] = self.count_data.get(x*30 + y,None)

    def winlosediff (self):
        transform_data = {}
        for d in self.real_data:
            transform_data[d[1]] = transform_data.setdefault(d[1], 0) +  (-1)**(not d[0])
        for x in range(21):
            for y in range(30):
                self.pd_wld[y][x] = transform_data.get(x*30 + y,None)

    def numberofwins(self):
        self.True_data={}
        for d in self.real_data:
            self.True_data[d[1]] = self.True_data.setdefault(d[1], 0) +  d[0]
        for x in range(21):
            for y in range(30):
                self.pd_wd[y][x] = self.True_data.get(x*30 + y,None)

    def realpercetange(self):
        percent_data = {}
        for c in self.count_data:
            percent_data[c] = self.True_data[c]/self.count_data[c]
        for x in range(21):
            for y in range(30):
                self.pd_pd[y][x] = round(percent_data.get(x*30 + y,0)*100, 3)

    def Pdf(self, x, y):
        r = sympy.symbols('r')
        h = self.True_data.get(x*30 + y, 0)
        t = self.count_data.get(x*30 + y, 0) - h
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

    def percentageofpercentage(self, load = True):
        my_bar = st.progress(0)
        try:
            if not load:
                raise Exception
            self.pd_ppcd = pd.read_pickle('./Archive/popdf' + str(len(self.real_data)) + '.pkl')
            my_bar.progress(100)
            st.write('Loaded from archive')
        except:
            with st.empty():
                for x in range(21):
                    for y in range(30):
                        my_bar.progress((x*30 + y)/629 )
                        try:
                            c = round(self.Pdf(x, y) * 100, 3)
                            st.write(str(x*30 + y) + '('+ str(x) + ',' + str(y) + ')' + 
                            " :: " +  str (c))
                            self.pd_ppcd[y][x] = format(c, '.2f')
                        except:
                            print(x, y)
                            st.write(str(x*30 + y) + '('+ str(x) + ',' + str(y) + ')' + 
                            " :: " +  'E')
                            self.pd_ppcd[y][x] = 'E'

            if load:
                self.pd_ppcd.to_pickle('./Archive/popdf' + str(len(self.real_data)) + '.pkl')
            else:
                self.pd_ppcd.to_pickle('./Archive/popdfpseudo' + str(len(self.real_data)) + '.pkl')

    def showdata (self):
        limit = 80
        self.uplimit = []
        for x in range(21):
            for y in range(30):
                if float(self.pd_ppcd[y][x]) >= limit and (float(self.pd_pd[y][x]) > 62.5 or float(self.pd_pd[y][x]) < 37.5):
                    self.uplimit.append((x, y, x*30 + y,  self.pd_ppcd[y][x], self.pd_td[y][x], self.pd_pd[y][x], self.pd_wd[y][x]))

        self.pd_showdata = pd.DataFrame(self.uplimit, columns=['x', 'y','index',' percentage', 'Total occurence', 'real %', 'wins'])


    def shownumbers (self):
        self.soto = sum([h[4] for h in self.uplimit if h[4] != None])    #sumoftotaloccurences
        self.sow = sum(h[6] for h in self.uplimit if h[5] > 50) + sum(h[4] - h[6] for h in self.uplimit if h[5] < 50) 
        self.ap = [float(h[3]) for h in self.uplimit if h[2] != None]
        self.ap = sum(self.ap)/ len(self.ap) # average percantage
        self.rp = [float(h[3]) * h[4] for h in self.uplimit if (h[3] != None and h[4] != None) ]
        self.rp = sum(self.rp)/self.soto # relative percantage
    
    def NPdf(self, h, t):
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

    def strmlt (self, load):
        st.set_page_config(page_title="Pseudo stat",layout='wide')
        default_width = None
        st.write("# Real Data")
        st.write('number of data:' + str(len(self.real_data)))
        self.totals()
        self.winlosediff()
        self.numberofwins()
        self.realpercetange()
        self.percentageofpercentage(load=load)
        self.showdata()
        self.shownumbers()
        left_column, right_column = st.columns(2)
        with left_column:
            st.dataframe(self.showdata)
            st.write('Sum of Total occurences: ' + str(self.soto))
            st.write('Sum of wins: ' + str(self.sow))
            st.write('Average percantage: ' + str(self.ap))
            st.write('Relative percantage: ' + str(self.rp))
            st.write('Abs %: ' + str(self.sow/self.soto * 100))
            st.write('% of abs % being above 62.5 % :' + str(self.NPdf(self.sow, self.soto-self.sow)* 100))
            # st.write('Expected value : ' + str( EV(sow/soto, soto)))

        with right_column:
            chart_data = pd.DataFrame([float(self.EV(t, self.soto)) for t in np.round(np.linspace(0.625, 0.630, 10), decimals=4) ], index = np.round(np.linspace(0.625, 0.630, 10), decimals=4), columns = ['p'] )
            st.bar_chart(chart_data)
            st.write(self.EVF())

            recept = {}
            for f in  self.uplimit:
                if f[5] > 50:
                    recept[f[2]] = 'call'
                else:
                    recept[f[2]] = 'put'

            if st.button('Show recept'):
                st.write(recept)