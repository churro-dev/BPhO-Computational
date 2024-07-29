# Imports

from math import cos, radians, sin, sqrt, tan, pi

import altair as alt
import pandas as pd
import streamlit as st
from st_pages import add_indentation, show_pages_from_config

# Config page
PAGE_TITLE = "Task 2"
PAGE_ICON = ":memo:"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

add_indentation()

show_pages_from_config()

# Main Content

st.title("Task 2")
st.subheader("Analytic model of drag-free projectile motion")

theta = st.slider(
    label="Launch angle from horizontal /$\ $°", # even out spacing
    min_value=0.0,
    max_value=90.0,
    value=45.0,
    step=0.1,
)
theta_rad = radians(theta)

g = st.number_input(
    label="Strength of gravity$\ g$ / $ms^{-2}$", min_value=0.1, max_value=None, value=9.81
)

u = st.number_input(
    label="Launch speed$\ u$ / $ms^{-1}$", min_value=0.1, max_value=None, value=10.0
)

h = st.number_input(
    label="Initial height$\ h$ / $m$", min_value=0.0, max_value=None, value=2.0
)

datapoints = st.number_input(
    label="Number of datapoints", min_value=1, max_value=1000, value=200
)  # determines how many points to calculate

# Downards direction is negative, input is positive
# Gravity always acts downards, so negative g_strength to get acceleration
a = -g

# For convenience
sin_theta = sin(radians(theta))
cos_theta = cos(radians(theta))
tan_theta = tan(radians(theta))

# Maximum horizontal range
R = ((u**2) / g) * (
    (sin_theta * cos_theta)
    + (cos_theta * sqrt((sin_theta**2) + ((2 * g * h) / (u**2))))
)

distance_increment = R / (datapoints - 1)

x_pos = pd.Series([(distance_increment * i) for i in range(datapoints)])

x_a = ((u**2) / g) * sin_theta * cos_theta

y_a = h + (((u**2) / (2 * g)) * (sin_theta**2))

T = R / (u * cos_theta)

t = pd.Series([x_pos_i / (u * cos_theta) for x_pos_i in x_pos])

y_pos = pd.Series(
    [
        h
        + (x_pos_i * tan_theta)
        - ((g / (2 * (u**2))) * (1 + (tan_theta**2)) * (x_pos_i**2))
        for x_pos_i in x_pos
    ]
)

pi_divisor = pi / theta_rad
if pi_divisor==(const := int(pi_divisor)):
    st.markdown(r"Initial launch elevation$\ \theta_0 = {\large{\frac{\pi}{" + f"{const}\ " + r"}}}\text{rad}$")
else:
    st.markdown(r"Initial launch elevation$\ \theta_0 = " + f"{theta_rad:.2f}\ " + r"\text{rad}$")
st.markdown(f"Range$\ R = {R:.2f}m$")
st.markdown(f"Apogee$\ x_a = {x_a:.2f}m$")
st.markdown(f"Apogee$\ y_a = {y_a:.2f}m$")
st.markdown(f"Time of flight$\ T = {T:.2f}s$")

pos = pd.DataFrame(
    {"t / s": t, "x / m": x_pos, "y / m": y_pos, "x_a / m": x_a, "y_a / m": y_a}
)

plot_points = st.toggle(label="Plot points instead of line?", value=False, help="If turned on, the connected lines will instead not be connected, and you can more clearly see the individually plotted points.")

if not plot_points:
    chart = (
        alt.Chart(pos)
        .mark_line(strokeWidth=4)
        .encode(
            x=alt.X("x / m", title="x / m"), y=alt.Y("y / m", title="y / m")
        )
    )
else:
    chart = (
        alt.Chart(pos)
        .mark_point(size=15)
        .encode(
            x=alt.X("x / m", title="x / m"), y=alt.Y("y / m", title="y / m")
        )
    )

point = (
    alt.Chart(pos).mark_point(color="red", size=50, shape="diamond").encode(x="x_a / m", y="y_a / m")
)

# Combine the chart and the point
st.altair_chart(chart + point, use_container_width=True)

st.subheader("Hover over the line and apogee for more info 📝")
