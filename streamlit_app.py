"""Home Page"""

# Imports

import streamlit as st
from st_pages import show_pages_from_config, add_indentation


# Config page
PAGE_TITLE = "BPhO CC 2024"
PAGE_ICON = "🖥️"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

add_indentation()

show_pages_from_config()

# Main Content

st.title("Welcome to our BPhO Computational Challenge entry.")

st.subheader("Please navigate to another page to begin viewing the task completions.")
