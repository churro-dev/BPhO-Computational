# Imports

import streamlit as st
from st_pages import show_pages_from_config
import pandas as pd
import altair as alt

from math import sin, cos, tan, atan, degrees, radians, sqrt


# Config page
PAGE_TITLE = "Task 3"
PAGE_ICON = "📝"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

show_pages_from_config()

# Main Content

st.title("Task 2")
st.subheader("Analytic model of drag-free projectile motion")

X = st.number_input(
    label = "Target X in m",
    min_value = 0.0,
    max_value = None,
    value = 1000.0
)

Y = st.number_input(
    label = "Target Y in m",
    min_value = 0.0,
    max_value = None,
    value = 300.0
)

g = st.number_input(
    label = "Strength of gravity (m/s²)",
    min_value = 0.0,
    max_value = None,
    value = 9.81
)

a = -g

u_min = sqrt(g) * sqrt(Y + sqrt((X**2) + (Y**2)))

st.write(f"Minimum launch speed to reach target: {u_min} m/s")

u = st.number_input(
    label = "Launch speed (m/s)",
    min_value = u_min,
    max_value = None,
    value = u_min
)

h = st.number_input(
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
)

distance_increment = X / (datapoints - 1)

x = pd.Series(
    [(distance_increment * i) for i in range(datapoints)]
)

theta_u_min_rad = atan((Y + sqrt((X ** 2) + (Y ** 2))) / X)

quadratic_a = (g / (2 * (u ** 2))) * (X ** 2)
quadratic_b = -X
quadratic_c = Y - h + ((g * (X ** 2)) / (2 * (u ** 2)))

quadratic_u = 2 * quadratic_a

quadratic_v = - quadratic_b / quadratic_u

quadratic_w = sqrt((quadratic_b ** 2) - (4 * quadratic_a * quadratic_c)) / quadratic_u

theta_highball_rad = atan(quadratic_v + quadratic_w)

theta_lowball_rad = atan(quadratic_v - quadratic_w)

st.write(f"Highball θ: {degrees(theta_highball_rad)}°")

st.write(f"Lowball θ: {degrees(theta_lowball_rad)}°")

tan_theta_u_min = tan(theta_u_min_rad)

y_u_min = pd.Series(
    [h + (x_i * tan_theta_u_min) - ((g / (2 * (u_min ** 2))) * (1 + (tan_theta_u_min ** 2)) * (x_i ** 2)) for x_i in x]
)

tan_theta_highball = tan(theta_highball_rad)

y_highball = pd.Series(
    [h + (x_i * tan_theta_highball) - ((g / (2 * (u ** 2))) * (1 + (tan_theta_highball ** 2)) * (x_i ** 2)) for x_i in x]
)

tan_theta_lowball = tan(theta_lowball_rad)

y_lowball = pd.Series(
    [h + (x_i * tan_theta_lowball) - ((g / (2 * (u ** 2))) * (1 + (tan_theta_lowball ** 2)) * (x_i ** 2)) for x_i in x]
)

pos = pd.DataFrame(
    {
        "x / m": x,
        "y_u_min / m": y_u_min,
        "y_highball / m": y_highball,
        "y_lowball / m": y_lowball
    }
)

base = alt.Chart(pos).encode(x = "x / m")

chart = alt.layer(
    base.mark_line(
        color = "grey"
    )
    .encode(
        y = alt.Y('y_u_min / m', title = "y / m")
    ),
    base.mark_line(
        color = "blue"
    )
    .encode(
        y = 'y_highball / m'
    ),
    base.mark_line(
        color = "red"
    )
    .encode(
        y = 'y_lowball / m'
    )
)

st.altair_chart(chart, use_container_width=True)

st.subheader("Hover over each line for more info 📝")