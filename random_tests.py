'''Sandbox for sporadic tests'''
import streamlit as st
import time

with st.empty():
    for seconds in range(60):
        st.write(str(f"⏳ {seconds} seconds have passed"))
        time.sleep(1)

    st.write('1 minute over')