""" Main Streamlit site file """

if __name__ != "__main__":
    quit()

import streamlit as st

# Config page
PAGE_TITLE = "AG + AJ BPhO Computational"
PAGE_ICON = "🖥️"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="collapsed"
)

st.title("Welcome to the AG + AJ BPhO Computational Challenge entry")