# Imports

import streamlit as st
from st_pages import show_pages_from_config, add_indentation
import pandas as pd
import altair as alt

from math import sin, cos, radians, sqrt


# Config page
PAGE_TITLE = "Task 1"
PAGE_ICON = "📝"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

add_indentation()

show_pages_from_config()

# Main Content

st.title("Task 1")
st.subheader("Simple model of drag-free projectile motion")

launch_angle = st.slider(
    label = "Launch angle from horizontal (°)",
    min_value = 0.0,
    max_value = 90.0,
    value = 45.0,
    step = 0.1,
)

g_strength = st.number_input(
    label = "Strength of gravity (m/s²)",
    min_value = 0.0,
    max_value = None,
    value = 9.81
)

launch_speed = st.number_input(
    label = "Launch speed (m/s)",
    min_value = 0.0,
    max_value = None,
    value = 10.0
)

height = st.number_input(
    label = "Initial height (m)",
    min_value = 0.0,
    max_value = None,
    value = 0.0
)

datapoints = st.number_input(
    label = "Number of datapoints",
    min_value = 1,
    max_value = 5000,
    value = 1000
) # determines how many points to calculate

# Downards direction is negative, input is positive
# Gravity always acts downards, so negative g_strength
g_strength *= -1

# For convenience
sin_theta = sin(radians(launch_angle))
cos_theta = cos(radians(launch_angle))

# Initial speed in x & y directions
u_x = launch_speed * cos_theta
u_y = launch_speed * sin_theta

t_max = - ((u_y + sqrt((u_y ** 2) - (2 * g_strength * height))) / g_strength) # Own equation

st.markdown(
    f"Determined time of flight (t<sub>max</sub>): {t_max} seconds",
    unsafe_allow_html=True
)

time_increment = t_max / (datapoints - 1)

st.write(f"Determined increment of time (Δt): {time_increment} seconds")

t = pd.Series(
    [time_increment * i for i in range(datapoints)]
)

# The rest is done using the provided equations, modified for a negative value of g

x_pos = pd.Series(
    [round(u_x, 14) * t_i for t_i in t]
)

y_pos = pd.Series(
    [height + (u_y * t_i) + (0.5 * g_strength * (t_i ** 2)) for t_i in t]
)

v_x = pd.Series(
    [u_x for _ in t]
)

v_y = pd.Series(
    [u_y + (g_strength * t_i) for t_i in t]
)

v = pd.Series(
    [sqrt((v_x_i ** 2) + (v_y_i ** 2)) for v_x_i, v_y_i in zip(v_x, v_y)]
)

pos = pd.DataFrame(
    {
        "Time (s)": t,
        "x / m": x_pos,
        "y / m": y_pos,
        "X Velocity (m/s)": v_x,
        "Y Velocity (m/s)": v_y,
        "Velocity (m/s)": v
    }
)

chart = (
    alt.Chart(pos)
    .mark_point()
    .encode(
        x="x / m",
        y="y / m",
        color="Velocity (m/s)",
        tooltip=[
            "Time (s)", "x / m", "y / m", "X Velocity (m/s)", "Y Velocity (m/s)", "Velocity (m/s)"
            ]
        )
    .resolve_scale(x="shared", y="shared")
)

st.altair_chart(chart, use_container_width=True)

st.subheader("Hover over the line for more info 📝")