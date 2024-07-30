# Imports

from math import cos, radians, sin, sqrt, tan, atan, degrees, pi

import altair as alt
import pandas as pd
import streamlit as st
from st_pages import add_indentation, show_pages_from_config
import pyvista
import stpyvista
import geovista

# Config page
PAGE_TITLE = "Global Projectile Motion"
PAGE_ICON = ":memo:"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

add_indentation()

show_pages_from_config()

# Main Content

