from stattools import Stat
import random
import numpy as np
import pickle
import streamlit as st
st.set_page_config(page_title="stat",layout='wide')
left_column, right_column = st.columns(2)



with left_column:
    real_data = pickle.load(open("data.pkl", 'rb'))
    st.write("# Real Data")
    st.write('number of data:' + str(len(real_data)))
    page = Stat(real_data)
    # page.transpose(2)
    page.calculations()
    page.strmlt()

    st.write("# Pseudo Data 62.4")
    pseudo_data = []
    for d in page.count_data:
        for k in range(page.count_data[d]):
            pseudo_data.append((np.random.choice((True, False), p=[0.624, 1-0.624]), d))
    pseudopage = Stat(pseudo_data)
    pseudopage.calculations()
    pseudopage.strmlt()
with right_column:
    st.write("# Pseudo Data 50")
    pseudo_data = []
    for d in page.count_data:
        for k in range(page.count_data[d]):
            pseudo_data.append((np.random.choice((True, False), p=[0.5, 1-0.5]), d))
    pseudopage = Stat(pseudo_data)
    pseudopage.calculations()
    pseudopage.strmlt()