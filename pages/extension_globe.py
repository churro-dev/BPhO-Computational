# Imports / page configuration

from math import cos, radians, sin, atan, degrees, sqrt, acos

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

g = st.number_input(
    label="Strength of gravity$\ g$ / $ms^{-2}$", min_value=0.1, max_value=None, value=(num := 9.81), format=f"%.{len(str(num).split('.')[-1])}f"
)

# some calculation based on the strength of gravity and radius of Earth to determine maximum launch speed allowed to be inputted
R = 6371000 # Average earth radius
cosmic_velocity = np.sqrt(R * g)
u = st.number_input(
    label="Launch speed$\ u$ / $ms^{-1}$", min_value=0.1, max_value=float(cosmic_velocity), value=(num := cosmic_velocity/2), format=f"%.{len(str(num).split('.')[-1])}f"
)
twod_v = u
twod_v_tilde = twod_v / np.sqrt(R * g)

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
    label="Number of datapoints", min_value=2, max_value=5000, value=(num := 100), step=1, format="%d"
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

# Plottinga  sphere at the staring coordinatets - *1000s are required for some reason, I guess the plotter uses mm or something for their coordinates
sphere_0 = pv.Sphere(radius = 100000000, center = (x_0*1000, y_0*1000, z_0*1000), theta_resolution=10, phi_resolution=10)
pl.add_mesh(sphere_0, color='red', opacity=0.5)

# sphere_n = pv.Sphere(radius = 100000000, center = (x_n*1000, y_n*1000, z_n*1000), theta_resolution=10, phi_resolution=10)
# pl.add_mesh(sphere_n, color='yellow', opacity=0.5)

# Numerical Method for Projectile Trajectory

# imagine projectile motion as 2d in direction of bearing, looking at it from the side
# equations from https://en.wikipedia.org/wiki/Projectile_motion

# angle input here - optimal trajectory angle is calculated and set as the default value
optimal_angle = (0.5) * acos((twod_v_tilde**2) / (2 - (twod_v_tilde**2)))
theta_deg = st.slider(
    label="Launch angle from horizontal /$\ $°", # even out spacing
    min_value=0.0,
    max_value=90.0,
    value=float(optimal_angle),
    step=0.1
)
theta_rad = radians(theta_deg)

# 2d projectile motion initial state calculations - the names expain what's being calculated
twod_v_x = u * cos(radians(theta_deg))
twod_v_y = u * sin(radians(theta_deg))
print(f"Velocity: {u}, Second cosmic velocity: {cosmic_velocity}")
d = ((((twod_v)**2) * sin(2 * theta_rad)) / g) / np.sqrt(1 - ((2-((twod_v_tilde)**2)) * (twod_v_tilde**2) * (cos(theta_rad)**2)))
print(f"Distance: {d}")
twod_t_max = (((2*twod_v) * sin(theta_rad)) / g) * (1 / (2 - (twod_v_tilde**2))) * (1 + ((1 / (np.sqrt(2-(twod_v_tilde**2))*twod_v_tilde*sin(theta_rad))) * np.arcsin((np.sqrt(2-(twod_v_tilde**2))*twod_v_tilde*sin(theta_rad))/np.sqrt(1-((2-(twod_v_tilde**2))*(twod_v_tilde**2)*(cos(theta_rad)**2))))))
print(f"Time of flight: {twod_t_max}")

# calculating time step
twod_dt = twod_t_max / datapoints
t = 0.0

# More initial 2d conditions
twod_t = [0]
twod_x = [0]
twod_y = [R]
twod_v = [u]
twod_vx = [u * cos(theta_rad)]
twod_vy = [u * sin(theta_rad)]
twod_ax = 0
twod_ay = -g

k = (0.5 * cD * rho * A) / m

# Loop for 2d projectile motion # NOT USING DRAG YET # TODO
for datapoint in range(datapoints):
    t = twod_t[-1] + twod_dt
    twod_t.append(t)
    
    twod_g_theta_rad = atan(twod_x[-1] / twod_y[-1]) # calculates angle at which gravity should act on projectile - this changes as the projectile travels around the globe.
    twod_ax = (- (g * sin(twod_g_theta_rad)))# - (twod_vx[-1] * k * twod_v[-1]) # calculations to subtract velocity based on drag is commented out because it is acting weird idk why
    twod_ay = (- (g * cos(twod_g_theta_rad)))# - (twod_vy[-1] * k * twod_v[-1]) # calculations to subtract velocity based on drag is commented out because it is acting weird idk why
    
    x = twod_x[-1] + (twod_vx[-1] * twod_dt) + (0.5 * twod_ax * (twod_dt**2)) # calculates new x position based on velocity and acceleration
    twod_x.append(x)
    
    y = twod_y[-1] + (twod_vy[-1] * twod_dt) + (0.5 * twod_ay * (twod_dt**2)) # calculates new y position based on velocity and acceleration
    twod_y.append(y)
    
    v_x = twod_vx[-1] + (twod_ax * twod_dt) # calculates new x velocity based on acceleration
    twod_vx.append(v_x)
    
    v_y = twod_vy[-1] + (twod_ay * twod_dt) # calculates new y velocity based on acceleration
    twod_vy.append(v_y)
    
    v = sqrt((twod_vx[-1]**2) + (twod_vy[-1]**2)) # calculates overall velocity based on x and y velocities
    twod_v.append(v)

# prints first and last positions to console
print(f"({twod_vx[0]}, {twod_vy[0]}, {twod_v[0]})")
print(f"({twod_vx[-1]}, {twod_vy[-1]}, {twod_v[-1]})")

# removes height of first projectile from all values to make it easier to plott on a 2d graph (basically just lowers it down to start at (0,0))
plotting_twod_y = []
first_y = twod_y[0]
for i, pos in enumerate(twod_y):
    plotting_twod_y.append(twod_y[i] - first_y)

# create plotting dataframe
df = {
    "x": pd.Series(twod_x),
    "y": pd.Series(plotting_twod_y)
}

# plot 2d projectile trajectory graph
chart = alt.Chart(pd.DataFrame(df)).mark_circle().encode(
    x='x',
    y='y'
)

# plot 2d graph
st.altair_chart(chart, use_container_width=True)

# making a zip of the x and y values to make it easier to plot the spheres - the z values are all 0
# example of what this looks like: [[x1, y1, z1], [x2, y2, z2], ...] where all z values start as 0
vectors = list(zip(twod_x, plotting_twod_y, [0]*len(twod_x)))
print(f"Vectors: {vectors[0], vectors[-1]}")

# rotate vectors so the motion is aligned with planetary surface - *rot* stands for rotation
lon_change = lon_0_deg + 180 # longitude is measured between -180 and 180, so this makes it 0 through 360
x_rot_angle = 270 - lon_change # I got this through trial and error as how to get the rotation angle right
x_rot_angle = radians(x_rot_angle) # converts rotation angle to radians
x_rot_matrix = [ # rotation matrix about x axis
    [cos(x_rot_angle), -sin(x_rot_angle), 0],
    [sin(x_rot_angle), cos(x_rot_angle), 0],
    [0, 0, 1]
]
y_rot_angle = lat_0_rad # also got this through trial and error
y_rot_matrix = [ # rotation matrix about y axis
    [cos(y_rot_angle), 0, sin(y_rot_angle)],
    [0, 1, 0],
    [-sin(y_rot_angle), 0, cos(y_rot_angle)]
]


for i, vector in enumerate(vectors):
    vectors[i] = np.dot(
        vector, np.dot(x_rot_matrix, y_rot_matrix)
    ) # does matrix multiplication with the original xyz vector and the result of the matrix multiplication of the two rotation matrices
    

displaced_distance = [x_0 - twod_x[0], y_0 - plotting_twod_y[0], z_0] # calculates distance from the inputtted launch point to current position of projectile launch, as the position changes when rotating the vectors

# makes a new list of vectors, and transforms the rotated vectors so that the initial launch point is the same as the inputted launch point using the variable defined above
positioned_vectors = []
for vector in vectors:
    temp = []
    for original, transform in zip(vector, displaced_distance):
        temp.append(original + transform)
    positioned_vectors.append(temp)

print(f"Positioned vectors: {positioned_vectors[0], positioned_vectors[-1]}") # prints starting and landing locations of projectile
print(f"Original location: {x_0, y_0, z_0}")


# Everything that plots the projectile motion is below:


print(f"Num vectors: {len(positioned_vectors)}") # prints number of points to be plotted to console
for pos in positioned_vectors: # plots a sphere at each point in the trajectory - resolution is low to make it run faster
    sphere = pv.Sphere(radius=10000000, center=(pos[0]*1000, pos[1]*1000, pos[2]*1000), theta_resolution=10, phi_resolution=10)
    pl.add_mesh(sphere, color='yellow', opacity=1) # yellow contrasts with Earth so that you can easily see the spheres

# Display the plot

# > Locally (on machine):
pl.show_axes()
pl.show()
pl.close()

# > On website (is a little slower, will switch to this once the whole 3d thing is fully implemented):
# stpyvista(pl, use_container_width=True)