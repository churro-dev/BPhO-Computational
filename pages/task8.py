# Imports

from math import cos, radians, sin, sqrt, tan, atan, degrees, pi

import altair as alt
import pandas as pd
import streamlit as st
from st_pages import add_indentation, show_pages_from_config
import time

# Config page
PAGE_TITLE = "Task 8"
PAGE_ICON = ":memo:"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

add_indentation()

show_pages_from_config()

# Main Content

st.title("Task 8")
st.subheader("Bouncing projectile trajectory")

theta_deg = st.slider(
    label="Launch angle from horizontal /$\ $°", # even out spacing
    min_value=0.0,
    max_value=90.0,
    value=45.0,
    step=0.1,
)
theta_rad = radians(theta_deg)
initial_theta_rad = theta_rad

g = st.number_input(
    label="Strength of gravity$\ g$ / $ms^{-2}$", min_value=0.1, max_value=None, value=9.81
)

u = st.number_input(
    label="Launch speed$\ u$ / $ms^{-1}$", min_value=0.1, max_value=None, value=10.0
)

h = st.number_input(
    label="Initial height$\ h$ / $m$", min_value=0.0, max_value=None, value=12.0
)

N = st.number_input(
    label="Number of bounces$\ N$", min_value=1, max_value=100, value=8
)

e = st.slider(
    label="Coefficient of restitution$\ e$",
    min_value = 0.01,
    max_value = 1.00,
    value = 0.75,
    step = 0.01
)

datapoints = st.number_input(
    label="Number of datapoints per bounce", min_value=2, max_value=1000, value=100
)  # determines how many points to calculate

# Downards direction is negative, input is positive
# Gravity always acts downards, so negative g_strength to get acceleration
a = -g

global x, y, u_x, u_y, R, T_max, R_max, x_poses, y_poses
x = 0
y = h

x_poses = []
y_poses = []

T_max = 0
R_max = 0

times = []
for bounce_count in range(N+1):
    # Calculations
    sin_theta = sin(theta_rad)
    cos_theta = cos(theta_rad)
    tan_theta = tan(theta_rad)
    # Current cycle
    if bounce_count == 0:
        u_x = u * cos_theta
        u_y = u * sin_theta
        R = ((u**2) / g) * (
            (sin_theta * cos_theta)
            + (cos_theta * sqrt((sin_theta**2) + ((2 * g * y) / (u**2))))
        )
    else:
        R = ((u**2)*sin(2*theta_rad)) / (g)
    dx = R / (datapoints - 1)
    relative_x_pos = [(dx * i) for i in range(datapoints)]
    x_pos = [(x + (dx * i)) for i in range(datapoints)]
    R_max += R
    T = R / (u_x)
    times.append(T)
    T_max += T
    y_pos = [
        round(y
        + ((x_pos_i * tan_theta)
        - ((g / (2 * (u**2))) * (1 + (tan_theta**2)) * (x_pos_i**2))), 10)
        for x_pos_i in relative_x_pos
    ]
    # Prepare for next cycle
    v_x = u_x
    v_y = sqrt((u_y**2) + (2 * g * y))
    u_x = v_x
    u_y = v_y * e
    u = sqrt((u_x**2) + (u_y**2))
    theta_rad = atan(u_y / u_x)
    theta_deg = degrees(theta_rad)
    x_poses += (x_pos)
    y_poses += (y_pos)
    x = x_pos[-1]
    y = y_pos[-1]

pi_divisor = pi / initial_theta_rad
if pi_divisor==(const := int(pi_divisor)):
    st.markdown(r"Initial launch elevation$\ \theta_0 = {\large{\frac{\pi}{" + f"{const}\ " + r"}}}\text{rad}$")
else:
    st.markdown(r"Initial launch elevation$\ \theta_0 = " + f"{initial_theta_rad:.2f}\ " + r"\text{rad}$")

st.markdown(r"Total range $\ R_{\text{max}}" + f" = {R_max:.2f}m$")
st.markdown(r"Total time $\ T_{\text{max}}" + f" = {T_max:.2f}s$")

pos_df = pd.DataFrame(
    {"x / m": pd.Series(x_poses),
     "y / m": pd.Series(y_poses)
    }
)

plot_points = st.toggle(label="Plot points instead of line?", value=False, help="If turned on, the connected lines will instead not be connected, and you can more clearly see the individually plotted points.")

if not plot_points:
    chart = (
        alt.Chart(pos_df)
        .mark_line(strokeWidth=4)
        .encode(
            x=alt.X("x / m", title="x / m"),
            y=alt.Y("y / m", title="y / m")
        )
    )
else:
    chart = (
        alt.Chart(pos_df)
        .mark_point(size=15)
        .encode(
            x=alt.X("x / m", title="x / m"),
            y=alt.Y("y / m", title="y / m")
        )
    )

st.altair_chart(chart, use_container_width=True)

st.subheader("Hover over the line for more info 📝")

animate_button = st.button("Animate trajectory")
if animate_button:
    chart = st.empty()
    time_between_points = dx / u_x
    formatted = "{:e}".format(time_between_points)
    pow_ten = int(formatted.split("-")[-1])
    new_time = time_between_points * (10**pow_ten)
    slow_constant = round(new_time)
    if not plot_points:
        for i in pos_df.index[:(pos_df.index[-1] // (datapoints // slow_constant))]:
            i += 1
            i *= (datapoints // slow_constant)
            i -= 1
            data_to_be_added = pos_df.iloc[0: i + (datapoints//slow_constant), :]

            x = alt.Chart(data_to_be_added).mark_line(strokeWidth=4).encode(
                x='x / m', 
                y='y / m',
            )

            time.sleep(0.1)

            chart.altair_chart(x, use_container_width=True)
    else:
        for i in pos_df.index[:(pos_df.index[-1] // (datapoints // slow_constant))]:
            i += 1
            i *= (datapoints // slow_constant)
            i -= 1
            data_to_be_added = pos_df.iloc[0: i + (datapoints//slow_constant), :]

            x = alt.Chart(data_to_be_added).mark_circle(size=15).encode(
                x='x / m', 
                y='y / m',
            )

            time.sleep(0.1)

            chart.altair_chart(x, use_container_width=True)