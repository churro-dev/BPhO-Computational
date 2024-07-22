# Imports
from math import asin, cos, radians, sin, sqrt, tan

import altair as alt
import pandas as pd
import streamlit as st
from st_pages import add_indentation, show_pages_from_config

# Config page
PAGE_TITLE = "Task 4"
PAGE_ICON = "📝"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

add_indentation()

show_pages_from_config()

# Main Content

st.title("Task 4")
st.subheader("Drag-free comparison to trajectory for maximal horizontal range R")

theta_deg = st.slider(
    label="Launch angle from horizontal /$\ $°", # even out spacing
    min_value=0.0,
    max_value=90.0,
    value=60.0,
    step=0.1,
)

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
sin_theta_R = sin(radians(theta_deg))
cos_theta_R = cos(radians(theta_deg))
tan_theta_R = tan(radians(theta_deg))

R = ((u**2) / g) * (
    (sin_theta_R * cos_theta_R)
    + (cos_theta_R * sqrt((sin_theta_R**2) + ((2 * g * h) / (u**2))))
)

x_a_R = ((u**2) / g) * sin_theta_R * cos_theta_R

y_a_R = h + (((u**2) / (2 * g)) * (sin_theta_R**2))

R_max = ((u**2) / g) * sqrt(1 + ((2 * h * g) / (u**2)))

theta_R_max_rad = asin(1 / sqrt(2 + ((2 * g * h) / (u**2))))

cos_theta_R_max = cos(theta_R_max_rad)
tan_theta_R_max = tan(theta_R_max_rad)

T_R = R / (u * cos_theta_R)

T_R_max = R_max / (u * cos_theta_R_max)

distance_increment_R = R / (datapoints - 1)

distance_increment_R_max = R_max / (datapoints - 1)


st.markdown(r"$\frac{u^2}{g} = " + f"{(u**2 / g):.2f}" + "m$")
# note: instructions incorrectly state to list $s$ and $s_{\text{max}}$, but they have not instructed to calculate these until task 6.
st.markdown(r"$(x_{a},y_{a}) = " + f"({x_a_R:.2f}m,{y_a_R:.2f}m)$")
st.markdown(r"$R = " + f"{R:.2f}" + "m$")
st.markdown(r"$R_{\text{max}} = " + f"{R_max:.2f}" + "m$")


x_pos_R = pd.Series([(distance_increment_R * i) for i in range(datapoints)])

x_pos_R_max = pd.Series([(distance_increment_R_max * i) for i in range(datapoints)])

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
        "x_a_R / m": x_a_R,
        "y_a_R / m": y_a_R,
    }
)

base = alt.Chart(pos)

plot_points = st.toggle(label="Plot points instead of line?", value=False, help="If turned on, the connected lines will instead not be connected, and you can more clearly see the individually plotted points.")

if not plot_points:
    chart = alt.layer(
        base.mark_line(color="blue", strokeWidth=4).encode(
            x=alt.X("x_R / m", title="x / m"),
            y=alt.Y("y_R / m", title="y / m")
        ),
        base.mark_line(
            color="red",
            strokeWidth=4
        ).encode(x="x_R_max / m", y="y_R_max / m"),
        base.mark_point(color="black", size=20, shape="diamond").encode(x="x_a_R / m", y="y_a_R / m"),
    )
else:
    chart = alt.layer(
        base.mark_point(color="blue", size=10).encode(
            x=alt.X("x_R / m", title="x / m"),
            y=alt.Y("y_R / m", title="y / m")
        ),
        base.mark_point(
            color="red",
            size=10
        ).encode(x="x_R_max / m", y="y_R_max / m"),
        base.mark_point(color="black", size=20, shape="diamond").encode(x="x_a_R / m", y="y_a_R / m"),
    )

st.altair_chart(chart, use_container_width=True)

st.subheader("Hover over each line for more info 📝")
