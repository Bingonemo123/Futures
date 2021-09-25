from stattools import Stat
import random
import numpy as np
import pickle
import streamlit as st
st.set_page_config(page_title="Pseudo stat",layout='wide')
real_data = pickle.load(open("data.pkl", 'rb'))   

page = Stat(real_data)
page.transpose(2)
page.calculations(True)
page.strmlt()

pseudo_data = [ (np.random.choice((True, False), p=[0.624, 1-0.624]), random.randint(0, 600)) for k in range(len(real_data))]    
pseudopage = Stat(pseudo_data)
pseudopage.calculations(False)
pseudopage.pseudostrmlt()

pseudo_data = [ (np.random.choice((True, False), p=[0.5, 0.5]), random.randint(0, 600)) for k in range(len(real_data))]    
pseudopage = Stat(pseudo_data)
pseudopage.calculations(False)
pseudopage.pseudostrmlt()