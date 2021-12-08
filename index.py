#index.py
import akinator
import dessinemoi
import streamlit as st

#LAYOUT
st.set_page_config(layout="wide")

PAGES = {
    "Akinator": akinator,
    "Dessine-moi...": dessinemoi
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Quelle application ?", list(PAGES.keys()))
page = PAGES[selection]
page.app()