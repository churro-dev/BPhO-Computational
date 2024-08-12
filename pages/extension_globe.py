# Imports / page configuration

from math import cos, radians, sin, acos, atan2, asin

import altair as alt
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

## loading globe texture data and plotting
dataset = load_globe()
texture = load_globe_texture()
pl = pv.Plotter()
pl.add_mesh(dataset, texture=texture)
pl.camera_position = 'iso'

## Inputs

lat_0_deg = st.number_input("Launch point latitude (degrees)", -90, 90, 10)
lat_0_rad = radians(lat_0_deg)
lon_0_deg = st.number_input("Launch point longitude (degrees)", -180, 180, 10)
lon_0_rad = radians(lon_0_deg)

# lat_n_deg = st.number_input("Landing point latitude (degrees)", -90, 90, 50)
# lat_n_rad = radians(lat_n_deg)
# lon_n_deg = st.number_input("Landing point longitude (degrees)", -180, 180, 50)
# lon_n_rad = radians(lon_n_deg)

bearing = st.slider(
    label="Bearing from north /$\ $°", # even out spacing
    min_value=0.0,
    max_value=360.0,
    value=45.0,
    step=0.1
)
bearing_rad = radians(bearing)

g = st.number_input(
    label="Strength of gravity$\ g$ / $ms^{-2}$", min_value=0.1, max_value=None, value=(num := 9.81), format=f"%.{len(str(num).split('.')[-1])}f"
)

# some calculation based on the strength of gravity and radius of Earth to determine maximum launch speed allowed to be inputted
R = 6371000 # Average earth radius
cosmic_velocity = np.sqrt(R * g)
u = st.number_input(
    label="Launch speed$\ u$ / $ms^{-1}$", min_value=0.1, max_value=float(cosmic_velocity), value=(num := cosmic_velocity/2), format=f"%.{len(str(num).split('.')[-1])}f"
)
v = u
v_tilde = v / np.sqrt(R * g)

h = st.number_input(
    label="Initial height$\ h$ / $m$", min_value=0.0, max_value=None, value=(num := 2.0), format=f"%.{len(str(num).split('.')[-1])}f"
)

# this whole with thing is a container containing details and conversion of drag coefficient
container = st.container(border=True)
with container:
    
    custom = st.toggle(label="Use custom drag coefficient", value=True, help="Turn on to use a custom drag coefficient rather than a preset shape.")
    
    shape = st.selectbox(
        label="Shape of projectile",
        options=["Sphere", "Half-sphere", "Cone", "Cube", "Angled Cube", "Long Cylinder", "Short Cylinder", "Streamlined Body", "Streamlined Half-body"],
        index=0,
        disabled=custom
    )
    
    drag_convert = {
        "Sphere": 0.47,
        "Half-sphere": 0.42,
        "Cone": 0.50,
        "Cube": 1.05,
        "Angled Cube": 0.80,
        "Long Cylinder": 0.82,
        "Short Cylinder": 1.15,
        "Streamlined Body": 0.04,
        "Streamlined Half-body": 0.09
    }
    
    if custom:
        default = 0.1
    else:
        default = drag_convert[shape]
    
    cD = st.number_input(
        label="Drag coefficient$\ C_D$",
        min_value=0.0,
        max_value=None,
        value=default,
        format=f"%.{len(str(num).split('.')[-1])}f",
        disabled=(not custom)
    )

A = st.number_input(
    label="Cross-sectional area$\ A$ / $m^2$", min_value=0.0, max_value=None, value=(num := 0.007854), format=f"%.{len(str(num).split('.')[-1])}f"
)

rho = st.number_input(
    label="Air density$\ \\rho$ / $kgm^{-3}$", min_value=0.0, max_value=None, value=(num := 1.0), format=f"%.{len(str(num).split('.')[-1])}f"
)

m = st.number_input(
    label="Mass$\ m$ / $kg$", min_value=0.0, max_value=None, value=(num := 0.1), format=f"%.{len(str(num).split('.')[-1])}f"
)

datapoints = st.number_input(
    label="Number of datapoints", min_value=2, max_value=5000, value=(num := 20), step=1, format="%d"
)

## End of inputs

# Converting latitude and longitude to cartesian coordinates

x_0 = R * cos(lat_0_rad) * cos(lon_0_rad)
y_0 = R * cos(lat_0_rad) * sin(lon_0_rad)
z_0 = R * sin(lat_0_rad)
# x_n = R * cos(lat_n_rad) * cos(lon_n_rad)
# y_n = R * cos(lat_n_rad) * sin(lon_n_rad)
# z_n = R * sin(lat_n_rad)

# backconversion formulas
# lat = asin(z / R)
# lon = atan2(y, x)

st.write(f"Position: ({x_0}, {y_0}, {z_0})")

# Plotting a sphere at the starting coordinates: *1000s are required for some reason, I guess the plotter uses mm or something for their coordinates
sphere_0 = pv.Sphere(radius = 100000000, center = (x_0*1000, y_0*1000, z_0*1000), theta_resolution=10, phi_resolution=10)
pl.add_mesh(sphere_0, color='red', opacity=0.5)

# sphere_n = pv.Sphere(radius = 100000000, center = (x_n*1000, y_n*1000, z_n*1000), theta_resolution=10, phi_resolution=10)
# pl.add_mesh(sphere_n, color='yellow', opacity=0.5)

# Numerical Method for Projectile Trajectory

# imagine projectile motion as 2d in direction of bearing, looking at it from the side
# equations from https://en.wikipedia.org/wiki/Projectile_motion

# angle input here - optimal trajectory angle is calculated and set as the default value
optimal_angle = (0.5) * acos((v_tilde**2) / (2 - (v_tilde**2)))
theta_deg = st.slider(
    label="Launch angle from horizontal /$\ $°", # even out spacing
    min_value=0.0,
    max_value=90.0,
    value=float(optimal_angle),
    step=0.1
)
theta_rad = radians(theta_deg)

# 2d projectile motion initial state calculations - the names expain what's being calculated
d = ((((v)**2) * sin(2 * theta_rad)) / g) / np.sqrt(1 - ((2-((v_tilde)**2)) * (v_tilde**2) * (cos(theta_rad)**2)))
print(f"Distance: {d}")
t_max = (((2*v) * sin(theta_rad)) / g) * (1 / (2 - (v_tilde**2))) * (1 + ((1 / (np.sqrt(2-(v_tilde**2))*v_tilde*sin(theta_rad))) * np.arcsin((np.sqrt(2-(v_tilde**2))*v_tilde*sin(theta_rad))/np.sqrt(1-((2-(v_tilde**2))*(v_tilde**2)*(cos(theta_rad)**2))))))
print(f"Time of flight: {t_max}")

# Interpolation and graphing

Ad = d / R # angular distance

lat_n_rad =  asin(sin(lat_0_rad) * cos(Ad)  + cos(lat_0_rad) * sin(Ad) * cos(bearing_rad))
lon_n_rad = lon_0_rad + atan2(sin(bearing_rad) * sin(Ad) * cos(lat_0_rad), cos(Ad) - sin(lat_0_rad) * sin(lat_n_rad))

x_n = R * cos(lat_n_rad) * cos(lon_n_rad)
y_n = R * cos(lat_n_rad) * sin(lon_n_rad)
z_n = R * sin(lat_n_rad)

def slerp_unit_vectors(p0, p1, t):
    
    omega = np.arccos(np.dot(p0, p1) / (np.linalg.norm(p0) * np.linalg.norm(p1)))
    d = sin(omega)
    s0 = sin((1 - t) * omega)
    s1 = sin(t * omega)
    
    return (p0 * s0 + p1 * s1) / d

dt = t_max / (datapoints - 1)

for i in range(datapoints + 1):
    t = i * dt
    if 0 <= t <= 1:
        point = slerp_unit_vectors(np.array([x_0, y_0, z_0]), np.array([x_n, y_n, z_n]), t)
        sphere = pv.Sphere(radius = 100000000, center = (point[0]*1000, point[1]*1000, point[2]*1000), theta_resolution=10, phi_resolution=10)
        pl.add_mesh(sphere, color='orange', opacity=0.5)

# Display the plot

## > Locally (on machine):
### pl.show_axes()
### pl.show()
### pl.close()

## > On website:
stpyvista(pl, use_container_width=True)