# Imports

from math import cos, radians, sin, sqrt, tan

import altair as alt
import pandas as pd
import streamlit as st
from st_pages import add_indentation, show_pages_from_config

# Config page
PAGE_TITLE = "Task 2"
PAGE_ICON = "📝"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

add_indentation()

show_pages_from_config()

# Main Content

st.title("Task 2")
st.subheader("Analytic model of drag-free projectile motion")

theta = st.slider(
    label="Launch angle from horizontal (°)",
    min_value=0.0,
    max_value=90.0,
    value=45.0,
    step=0.1,
)

g = st.number_input(
    label="Strength of gravity (m/s²)", min_value=0.0, max_value=None, value=9.81
)

u = st.number_input(
    label="Launch speed (m/s)", min_value=0.0, max_value=None, value=10.0
)

h = st.number_input(
    label="Initial height (m)", min_value=0.0, max_value=None, value=0.0
)

datapoints = st.number_input(
    label="Number of datapoints", min_value=1, max_value=5000, value=1000
)  # determines how many points to calculate

# Downards direction is negative, input is positive
# Gravity always acts downards, so negative g_strength to get acceleration
acceleration = -g

# For convenience
sin_theta = sin(radians(theta))
cos_theta = cos(radians(theta))
tan_theta = tan(radians(theta))

# Maximum horizontal range
R = ((u**2) / g) * (
    (sin_theta * cos_theta)
    + (cos_theta * sqrt((sin_theta**2) + ((2 * g * h) / (u**2))))
)

st.write(f"Determined maximum horizontal range R: {R}m")

distance_increment = R / (datapoints - 1)

st.write(f"Increment of distance (Δx): {distance_increment}m")

x_pos = pd.Series([(distance_increment * i) for i in range(datapoints)])

x_a = ((u**2) / g) * sin_theta * cos_theta

y_a = h + (((u**2) / (2 * g)) * (sin_theta**2))

T = R / (u * cos_theta)

st.write(f"Time of flight T: {T}s")

t = pd.Series([x_pos_i / (u * cos_theta) for x_pos_i in x_pos])

y_pos = pd.Series(
    [
        h
        + (x_pos_i * tan_theta)
        - ((g / (2 * (u**2))) * (1 + (tan_theta**2)) * (x_pos_i**2))
        for x_pos_i in x_pos
    ]
)

pos = pd.DataFrame(
    {"t / s": t, "x / m": x_pos, "y / m": y_pos, "x_a / m": x_a, "y_a / m": y_a}
)

# Plotting the chart
chart = (
    alt.Chart(pos)
    .mark_point()
    .encode(
        x=alt.X("x / m", title="x / m"), y=alt.Y("y / m", title="y / m"), color="t / s"
    )
)

# Adding a separate point
point = (
    alt.Chart(pos).mark_point(color="red", size=100).encode(x="x_a / m", y="y_a / m")
)

# Combine the chart and the point
st.altair_chart(chart + point, use_container_width=True)

st.subheader("Hover over the line and apogee for more info 📝")
