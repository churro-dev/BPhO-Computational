# Imports
import streamlit as st
from st_pages import show_pages_from_config, add_indentation
import pandas as pd
import altair as alt
from math import sin, asin, cos, tan, atan, degrees, radians, sqrt


# Config page
PAGE_TITLE = "Task 5"
PAGE_ICON = "📝"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

add_indentation()

show_pages_from_config()

# Main Content

st.title("Task 5")
st.subheader("Upgraded drag-free projectile motion model passing through a fixed position (X, Y)")

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

launch_speed_container = st.container(border = True)

with launch_speed_container:

    st.write(f"Minimum launch speed to reach target: {u_min} m/s")

    apply_u = st.button("Apply minimum launch speed")

    unapply_u = st.button("Unapply minimum launch speed")

    if apply_u and not unapply_u:
        u = st.number_input(
            label = "Launch speed (m/s)",
            min_value = u_min,
            max_value = None,
            value = u_min,
            disabled = True
        )
    else:
        u = st.number_input(
            label = "Launch speed (m/s)",
            min_value = u_min,
            max_value = None,
            value = u_min * 1.15,
            disabled = False
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

theta_u_min_rad = atan((Y + sqrt((X ** 2) + (Y ** 2))) / X)

sin_theta_u_min = sin(theta_u_min_rad)
cos_theta_u_min = cos(theta_u_min_rad)

R_u_min = ((u_min ** 2) / g) * ((sin_theta_u_min * cos_theta_u_min) + (cos_theta_u_min * sqrt((sin_theta_u_min ** 2) + ((2 * g * h)/(u_min ** 2)))))

delta_x_u_min = R_u_min / (datapoints - 1)

x_u_min = pd.Series(
    [(delta_x_u_min * i) for i in range(datapoints)]
)

quadratic_a = (g / (2 * (u ** 2))) * (X ** 2)
quadratic_b = -X
quadratic_c = Y - h + ((g * (X ** 2)) / (2 * (u ** 2)))

quadratic_u = 2 * quadratic_a

quadratic_v = - quadratic_b / quadratic_u

quadratic_w = sqrt((quadratic_b ** 2) - (4 * quadratic_a * quadratic_c)) / quadratic_u

theta_lowball_rad = atan(quadratic_v - quadratic_w)

theta_highball_rad = atan(quadratic_v + quadratic_w)

sin_theta_lowball = sin(theta_lowball_rad)
cos_theta_lowball = cos(theta_lowball_rad)

R_lowball = ((u ** 2) / g) * ((sin_theta_lowball * cos_theta_lowball) + (cos_theta_lowball * sqrt((sin_theta_lowball ** 2) + ((2 * g * h)/(u ** 2)))))

delta_x_lowball = R_lowball / (datapoints - 1)

x_lowball = pd.Series(
    [(delta_x_lowball * i) for i in range(datapoints)]
)

sin_theta_highball = sin(theta_highball_rad)
cos_theta_highball = cos(theta_highball_rad)

R_highball = ((u ** 2) / g) * ((sin_theta_highball * cos_theta_highball) + (cos_theta_highball * sqrt((sin_theta_highball ** 2) + ((2 * g * h)/(u ** 2)))))

delta_x_highball = R_highball / (datapoints - 1)

x_highball = pd.Series(
    [(delta_x_highball * i) for i in range(datapoints)]
)

if u_min != u:
    st.markdown(f"θ<sub>highball</sub> = {degrees(theta_highball_rad)}°", unsafe_allow_html=True)
    st.markdown(f"θ<sub>u<sub>min</sub></sub> = {degrees(theta_u_min_rad)}", unsafe_allow_html=True)
    st.markdown(f"θ<sub>lowball</sub> = {degrees(theta_lowball_rad)}°", unsafe_allow_html=True)
else:
    st.markdown(f"θ<sub>u<sub>min</sub></sub> = θ<sub>highball</sub> = θ<sub>lowball</sub> = {degrees(theta_u_min_rad)}°", unsafe_allow_html=True)

tan_theta_u_min = tan(theta_u_min_rad)

y_u_min = pd.Series(
    [h + (x_u_min_i * tan_theta_u_min) - ((g / (2 * (u_min ** 2))) * (1 + (tan_theta_u_min ** 2)) * (x_u_min_i ** 2)) for x_u_min_i in x_u_min]
)

tan_theta_highball = tan(theta_highball_rad)

y_highball = pd.Series(
    [h + (x_highball_i * tan_theta_highball) - ((g / (2 * (u ** 2))) * (1 + (tan_theta_highball ** 2)) * (x_highball_i ** 2)) for x_highball_i in x_highball]
)

tan_theta_lowball = tan(theta_lowball_rad)

y_lowball = pd.Series(
    [h + (x_lowball_i * tan_theta_lowball) - ((g / (2 * (u ** 2))) * (1 + (tan_theta_lowball ** 2)) * (x_lowball_i ** 2)) for x_lowball_i in x_lowball]
)

R_max = ((u ** 2) / g) * sqrt(1 + ((2 * h * g) / (u ** 2)))

st.markdown(f"R<sub>max</sub> = {R_max}", unsafe_allow_html=True)

theta_R_max_rad = asin(1 / sqrt(2 + ((2 * g * h) / (u ** 2))))

tan_theta_R_max = tan(theta_R_max_rad)

st.markdown(f"θ<sub>R<sub>max</sub></sub> = {degrees(theta_R_max_rad)}", unsafe_allow_html=True)

delta_x_R_max = R_max / (datapoints - 1)

x_R_max = pd.Series(
    [(delta_x_R_max * i) for i in range(datapoints)]
)

y_R_max = pd.Series(
    [h + (x_R_max_i * tan_theta_R_max) - ((g / (2 * (u ** 2))) * (1 + (tan_theta_R_max ** 2)) * (x_R_max_i ** 2)) for x_R_max_i in x_R_max]
)

x_bounding_parabola = x_R_max

y_bounding_parabola = pd.Series(
    [((u ** 2) / (2 * g)) - ((g / (2 * (u ** 2))) * (x_b_p_i ** 2)) for x_b_p_i in x_bounding_parabola]
)

pos = pd.DataFrame(
    {
        "x_u_min": x_u_min,
        "y_u_min": y_u_min,
        "x_lowball": x_lowball,
        "y_lowball": y_lowball,
        "x_highball": x_highball,
        "y_highball": y_highball,
        "x_R_max": x_R_max,
        "y_R_max": y_R_max,
        "x_bounding_parabola": x_bounding_parabola,
        "y_bounding_parabola": y_bounding_parabola,
        "0": 0
    }
)

base = alt.Chart(pos)

chart = alt.layer(
    base.mark_line(
        color = 'grey'
    )
    .encode(
        x = 'x_u_min',
        y = 'y_u_min'
    ),
    base.mark_line(
        color = 'blue'
    )
    .encode(
        x = 'x_highball',
        y = 'y_highball'
    ),
    base.mark_line(
        color = 'green'
    )
    .encode(
        x = 'x_lowball',
        y = 'y_lowball'
    ),
    base.mark_line(
        color = 'red'
    )
    .encode(
        x = 'x_R_max',
        y = 'y_R_max'
    ),
    base.mark_line(
        color = 'pink'
    )
    .encode(
        x = 'x_bounding_parabola',
        y = 'y_bounding_parabola'
    ),
    base.mark_point().encode(
        x = alt.X("0", title = "x / m"),
        y = alt.Y("0", title = "y / m")
    )
)

st.altair_chart(chart, use_container_width=True)

st.subheader("Hover over each line for more info 📝")