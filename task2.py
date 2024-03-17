# Imports

import streamlit as st
from st_pages import show_pages_from_config
import pandas as pd
import altair as alt

from math import sin, cos, tan, radians, sqrt


# Config page
PAGE_TITLE = "Task 2"
PAGE_ICON = "🖥️"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

show_pages_from_config()

# Main Content

st.title("Task 2")
st.subheader("Analytic model of drag-free projectile motion")

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
# Gravity always acts downards, so negative g_strength to get acceleration
acceleration = g_strength * -1

# For convenience
sin_theta = sin(radians(launch_angle))
cos_theta = cos(radians(launch_angle))
tan_theta = tan(radians(launch_angle))

# Maximum horizontal range
R = ((launch_speed ** 2) / g_strength)*((sin_theta * cos_theta) + (cos_theta * sqrt((sin_theta ** 2) + ((2 * g_strength * height)/(launch_speed ** 2)))))

st.write(f"Determined maximum horizontal range R: {R}m")

distance_increment = R / (datapoints - 1)

st.write(f"Increment of distance (Δx): {distance_increment}m")

x_pos = pd.Series(
    [(distance_increment * i) for i in range(datapoints)]
)

x_a = ((launch_speed ** 2) / g_strength) * sin_theta * cos_theta

y_a = height + (((launch_speed ** 2) / (2 * g_strength)) * (sin_theta ** 2))

T = R / (launch_speed * cos_theta)

t = pd.Series(
    [x_pos_i / (launch_speed * cos_theta) for x_pos_i in x_pos]
)

y_pos = pd.Series(
    [height + (x_pos_i * tan_theta) - (((g_strength) / (2 * (launch_speed ** 2))) * (1 + (tan_theta ** 2)) * (x_pos_i ** 2)) for x_pos_i in x_pos]
)

pos = pd.DataFrame(
    {
        "Time (s)": t,
        "x / m": x_pos,
        "y / m": y_pos,
        "x_a / m": x_a,
        "y_a / m": y_a
    }
)

# Plotting the chart
chart = alt.Chart(pos).mark_line().encode(
    x='x / m',
    y='y / m'
)

# Adding a separate point
point = (alt.Chart(pos)
    .mark_point(color='red', size=100)
    .encode(
        x='x_a / m',
        y='y_a / m'
    )
)

# Combine the chart and the point
st.altair_chart(chart + point, use_container_width=True)

st.subheader("Hover over the line and apogee for more info 📝")