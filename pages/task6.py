# Imports
from math import asin, cos, degrees, radians, sin, sqrt, tan, log

import altair as alt
import pandas as pd
import streamlit as st
from st_pages import add_indentation, show_pages_from_config

# Config page
PAGE_TITLE = "Task 6"
PAGE_ICON = "📝"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

add_indentation()

show_pages_from_config()

# Main Content

st.title("Task 6")
st.subheader("Updated projectile model with calculation of distance traveled by projectile (length of inverted parabolic arc)")

theta_deg = st.slider(
    label="Launch angle from horizontal (°)",
    min_value=0.0,
    max_value=89.9,
    value=60.0,
    step=0.1,
)

g = st.number_input(
    label="Strength of gravity (m/s²)", min_value=0.1, max_value=None, value=9.81
)

u = st.number_input(
    label="Launch speed (m/s)", min_value=0.1, max_value=None, value=10.0
)

h = st.number_input(
    label="Initial height (m)", min_value=0.0, max_value=None, value=2.0
)

datapoints = st.number_input(
    label="Number of datapoints", min_value=1, max_value=5000, value=1000
)  # determines how many points to calculate

# Downards direction is negative, input is positive
# Gravity always acts downards, so negative g_strength to get acceleration
acceleration = -g

# For convenience
sin_theta_R = sin(radians(theta_deg))
cos_theta_R = cos(radians(theta_deg))
tan_theta_R = tan(radians(theta_deg))

R = ((u**2) / g) * ((sin_theta_R * cos_theta_R)+ (cos_theta_R * sqrt((sin_theta_R**2) + ((2 * g * h) / (u**2)))))

st.write(f"R = {R}")

R_max = ((u**2) / g) * sqrt(1 + ((2 * h * g) / (u**2)))

st.markdown(f"R<sub>max</sub> = {R_max}", unsafe_allow_html=True)

theta_R_max_rad = asin(1 / sqrt(2 + ((2 * g * h) / (u**2))))

sin_theta_R_max = sin(theta_R_max_rad)
cos_theta_R_max = cos(theta_R_max_rad)
tan_theta_R_max = tan(theta_R_max_rad)

st.markdown(
    f"θ<sub>R<sub>max</sub></sub> = {degrees(theta_R_max_rad)}", unsafe_allow_html=True
)

T_R = R / (u * cos_theta_R)

st.write(f"Time of flight T: {T_R}s")

T_R_max = R_max / (u * cos_theta_R_max)

st.markdown(f"T<sub>max</sub>: {T_R_max}s", unsafe_allow_html=True)

distance_increment_R = R / (datapoints - 1)

distance_increment_R_max = R_max / (datapoints - 1)

x_pos_R = pd.Series([(distance_increment_R * i) for i in range(datapoints)])

x_pos_R_max = pd.Series([(distance_increment_R_max * i) for i in range(datapoints)])


z_1_R = tan_theta_R - (((g * R) / (u**2)) * (1 + (tan_theta_R**2)))

z_2_R = tan_theta_R

d_R = ((u**2) / (g * (1 + (tan_theta_R**2)))) * (((1/2) * ((log(abs(sqrt(1 + (z_1_R**2)) + z_1_R))) + (z_1_R * sqrt(1 + (z_1_R**2))))) - ((1/2) * ((log(abs(sqrt(1 + (z_2_R**2)) + z_2_R))) + (z_2_R * sqrt(1 + (z_2_R**2))))))

st.markdown(f"d<sub>R</sub>: {d_R}m", unsafe_allow_html=True)


z_1_R_max = tan_theta_R_max - (((g * R_max) / (u**2)) * (1 + (tan_theta_R_max**2)))

z_2_R_max = tan_theta_R_max

d_R_max = ((u**2) / (g * (1 + (tan_theta_R_max**2)))) * (((1/2) * ((log(abs(sqrt(1 + (z_1_R_max**2)) + z_1_R_max))) + (z_1_R_max * sqrt(1 + (z_1_R_max**2))))) - ((1/2) * ((log(abs(sqrt(1 + (z_2_R_max**2)) + z_2_R_max))) + (z_2_R_max * sqrt(1 + (z_2_R_max**2))))))

st.markdown(f"d<sub>R<sub>max</sub></sub>: {d_R_max}m", unsafe_allow_html=True)

x_a = ((u**2) / g) * sin_theta_R * cos_theta_R

y_a = h + (((u**2) / (2 * g)) * (sin_theta_R**2))


y_pos_R = pd.Series(
    [
        h
        + (x_pos_R_i * tan_theta_R)
        - ((g / (2 * (u**2))) * (1 + (tan_theta_R**2)) * (x_pos_R_i**2))
        for x_pos_R_i in x_pos_R
    ]
)

y_pos_R_max = pd.Series(
    [
        h
        + (x_pos_R_max_i * tan_theta_R_max)
        - ((g / (2 * (u**2))) * (1 + (tan_theta_R_max**2)) * (x_pos_R_max_i**2))
        for x_pos_R_max_i in x_pos_R_max
    ]
)

t_R = pd.Series([x_pos_R_i / (u * cos_theta_R) for x_pos_R_i in x_pos_R])

t_R_max = pd.Series(
    [x_pos_R_max_i / (u * cos_theta_R_max) for x_pos_R_max_i in x_pos_R_max]
)

pos = pd.DataFrame(
    {
        "t_R / s": t_R,
        "t_R_max / s": t_R_max,
        "x_R / m": x_pos_R,
        "x_R_max / m": x_pos_R_max,
        "y_R / m": y_pos_R,
        "y_R_max / m": y_pos_R_max,
        "x_a / m": x_a,
        "y_a / m": y_a,
    }
)

base = alt.Chart(pos)

chart = alt.layer(
    base.mark_point(color="blue").encode(
        x=alt.X("x_R / m", title="x / m"),
        y=alt.Y("y_R / m", title="y / m"),
        strokeWidth=("t_R / s"),
    ),
    base.mark_point(
        color="red",
    ).encode(x="x_R_max / m", y="y_R_max / m", strokeWidth="t_R_max / s"),
    base.mark_point(color="black", size=200).encode(x="x_a / m", y="y_a / m")
)

st.altair_chart(chart, use_container_width=True)

st.subheader("Hover over each line for more info 📝")