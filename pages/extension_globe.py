# Imports

from math import cos, radians, sin, sqrt, tan, atan, degrees, pi

import pandas as pd
import streamlit as st
from st_pages import add_indentation, show_pages_from_config
from pyvista.examples import load_globe, load_globe_texture
import pyvista as pv
from stpyvista import stpyvista

# Config page
PAGE_TITLE = "Global Projectile Motion"
PAGE_ICON = ":memo:"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

add_indentation()

show_pages_from_config()

# Main Content

dataset = load_globe()
texture = load_globe_texture()
pl = pv.Plotter()
pl.add_mesh(dataset, texture=texture)

pl.camera_position = 'iso'

stpyvista(pl)