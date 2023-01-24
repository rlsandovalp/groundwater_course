import pygimli as pg
import streamlit as st

pg.test(show=False , onlydoctests=True)
st.write("# Test was passed?")