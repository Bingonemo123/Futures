import json
from stattools import Stat
import numpy as np
import json
import pickle
import streamlit as st
st.set_page_config(page_title="stat",layout='wide')
left_column, right_column = st.columns(2)


with left_column:
    # real_data = json.load(open("data.json", 'r'))
    real_data = pickle.load(open('getreadyfull.pkl', 'rb'))
    st.write("# Real Data")
    st.write('number of data:' + str(len(real_data)))
    page = Stat(real_data)
   #  page.transpose(7)
    page.calculations()
    page.strmlt()

    recept = {}
    for f in  page.uplimit:
        if f[3] > 50:
            recept[f[0]] = 'call'
        else:
            recept[f[0]] = 'put'
    print(recept)

    mlt = st.radio('multiplayer', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    st.write("# Pseudo Data 62.4")
    pseudo_data = []
    for d in page.count_data:
        for k in range(mlt * page.count_data[d]):
            pseudo_data.append((np.random.choice((True, False), p=[0.624, 1-0.624]), d))
    pseudopage = Stat(pseudo_data)
    pseudopage.calculations()
    pseudopage.strmlt()

with right_column:
    st.write("# Pseudo Data 50")
    pseudo_data = []
    for d in page.count_data:
        for k in range(mlt* page.count_data[d]):
            pseudo_data.append((np.random.choice((True, False), p=[0.5, 1-0.5]), d))
    pseudopage = Stat(pseudo_data)
    pseudopage.calculations()
    pseudopage.strmlt()