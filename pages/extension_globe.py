# Imports

from math import cos, radians, sin, asin, atan2

import numpy as np
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

lat_0_deg = st.number_input("Launch point latitude (degrees)", -90, 90, 10)
lat_0_rad = radians(lat_0_deg)
lon_0_deg = st.number_input("Launch point longitude (degrees)", -180, 180, 10)
lon_0_rad = radians(lon_0_deg)

lat_n_deg = st.number_input("Landing point latitude (degrees)", -90, 90, 50)
lat_n_rad = radians(lat_n_deg)
lon_n_deg = st.number_input("Landing point longitude (degrees)", -180, 180, 50)
lon_n_rad = radians(lon_n_deg)


R = 6371000 # Average earth radius
x_0 = R * cos(lat_0_rad) * cos(lon_0_rad)
y_0 = R * cos(lat_0_rad) * sin(lon_0_rad)
z_0 = R * sin(lat_0_rad)
x_n = R * cos(lat_n_rad) * cos(lon_n_rad)
y_n = R * cos(lat_n_rad) * sin(lon_n_rad)
z_n = R * sin(lat_n_rad)

# backconversion formulas
# lat = asin(z / R)
# lon = atan2(y, x)

st.write(f"Position: ({x_0}, {y_0}, {z_0})")

sphere_0 = pv.Sphere(radius = 100000000, center = (x_0*1000, y_0*1000, z_0*1000), theta_resolution=10, phi_resolution=10)
pl.add_mesh(sphere_0, color='red', opacity=0.5)

sphere_n = pv.Sphere(radius = 100000000, center = (x_n*1000, y_n*1000, z_n*1000), theta_resolution=10, phi_resolution=10)
pl.add_mesh(sphere_n, color='yellow', opacity=0.5)

stpyvista(pl, use_container_width=True)