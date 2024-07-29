# Imports
from math import atan, degrees, sqrt, tan

import altair as alt
import pandas as pd
import streamlit as st
from st_pages import add_indentation, show_pages_from_config

# Config page
PAGE_TITLE = "Task 3"
PAGE_ICON = ":memo:"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

add_indentation()

show_pages_from_config()

# Main Content

st.title("Task 3")
st.subheader(
    "Drag-free projectile motion model passing through a fixed position " + r"$\left(X,Y\right)$"
)

X = st.number_input(label="Target $X$ / $m$", min_value=0.0, max_value=None, value=(num := 1000.0), format=f"%.{len(str(num).split('.')[-1])}f") # spacing different here and below to make even

Y = st.number_input(label="Target$\ Y$ / $m$", min_value=0.0, max_value=None, value=(num := 300.0), format=f"%.{len(str(num).split('.')[-1])}f") # spacing different here and above to make even

g = st.number_input(
    label="Strength of gravity$\ g$ / $ms^{-2}$", min_value=0.1, max_value=None, value=(num := 9.81), format=f"%.{len(str(num).split('.')[-1])}f"
)

u_min = sqrt(g) * sqrt(Y + sqrt((X**2) + (Y**2)))

launch_speed_container = st.container(border=True)

with launch_speed_container:
    st.markdown(f"Minimum launch speed to reach target$\ u = {u_min:.2f} " + r"ms^{-1}$")

    apply_u = st.button("Apply minimum launch speed")

    unapply_u = st.button("Unapply minimum launch speed")

    if apply_u and not unapply_u:
        u = st.number_input(
            label="Launch speed$\ u$ / $ms^{-1}$",
            min_value=u_min,
            max_value=None,
            value=u_min,
            format=f"%.{len(str(u_min).split('.')[-1])}f",
            disabled=True,
        )
    else:
        u = st.number_input(
            label="Launch speed$\ u$ / $ms^{-1}$",
            min_value=u_min,
            max_value=None,
            value=u_min * 1.15,
            format=f"%.{len(str(u_min * 1.15).split('.')[-1])}f",
            disabled=False,
        )

h = 0

datapoints = st.number_input(
    label="Number of datapoints", min_value=1, max_value=1000, value=200
)  # determines how many points to calculate

distance_increment = X / (datapoints - 1)

x = pd.Series([(distance_increment * i) for i in range(datapoints)])


theta_u_min_rad = atan((Y + sqrt((X**2) + (Y**2))) / X)


quadratic_a = (g / (2 * (u**2))) * (X**2)
quadratic_b = -X
quadratic_c = Y - h + ((g * (X**2)) / (2 * (u**2)))

quadratic_u = 2 * quadratic_a

quadratic_v = -quadratic_b / quadratic_u

quadratic_w = sqrt((quadratic_b**2) - (4 * quadratic_a * quadratic_c)) / quadratic_u

theta_highball_rad = atan(quadratic_v + quadratic_w)

theta_lowball_rad = atan(quadratic_v - quadratic_w)

if u_min != u:
    st.markdown(
        r"$\theta_{\text{highball}} = " + f"{degrees(theta_highball_rad):.2f}\degree = " + f"{theta_highball_rad:.2f}" + r"\ \text{rad}$"
    )
    st.markdown(
        r"$\theta_{u_{\text{min}}} = " + f"{degrees(theta_u_min_rad):.2f}\degree = " + f"{theta_u_min_rad:.2f}" + r"\ \text{rad}$"
    )
    st.markdown(
        r"$\theta_{\text{lowball}} = " + f"{degrees(theta_lowball_rad):.2f}\degree = " + f"{theta_lowball_rad:.2f}" + r"\ \text{rad}$"
    )
else:
    st.markdown(
        r"$\theta_{\text{highball}} = \theta_{u_{\text{min}}} = \theta_{\text{lowball}} = " + f"{degrees(theta_u_min_rad)}\degree = " + f"{theta_u_min_rad:.2f}" + r"\ \text{rad}$"
    )

tan_theta_u_min = tan(theta_u_min_rad)

y_u_min = pd.Series(
    [
        h
        + (x_i * tan_theta_u_min)
        - ((g / (2 * (u_min**2))) * (1 + (tan_theta_u_min**2)) * (x_i**2))
        for x_i in x
    ]
)

tan_theta_highball = tan(theta_highball_rad)

y_highball = pd.Series(
    [
        h
        + (x_i * tan_theta_highball)
        - ((g / (2 * (u**2))) * (1 + (tan_theta_highball**2)) * (x_i**2))
        for x_i in x
    ]
)

tan_theta_lowball = tan(theta_lowball_rad)

y_lowball = pd.Series(
    [
        h
        + (x_i * tan_theta_lowball)
        - ((g / (2 * (u**2))) * (1 + (tan_theta_lowball**2)) * (x_i**2))
        for x_i in x
    ]
)

pos = pd.DataFrame(
    {
        "x / m": x,
        "y_u_min / m": y_u_min,
        "y_highball / m": y_highball,
        "y_lowball / m": y_lowball,
    }
)

base = alt.Chart(pos).encode(x="x / m")

plot_points = st.toggle(label="Plot points instead of line?", value=False, help="If turned on, the connected lines will instead not be connected, and you can more clearly see the individually plotted points.")

if not plot_points:
    chart = alt.layer(
        base.mark_line(color="grey", strokeWidth=3).encode(y=alt.Y("y_u_min / m", title="y / m")),
        base.mark_line(color="blue", strokeWidth=3).encode(y="y_highball / m"),
        base.mark_line(color="red", strokeWidth=3).encode(y="y_lowball / m"),
    )
else:
    chart = alt.layer(
        base.mark_point(color="grey", size=10).encode(y=alt.Y("y_u_min / m", title="y / m")),
        base.mark_point(color="blue", size=10).encode(y="y_highball / m"),
        base.mark_point(color="red", size=10).encode(y="y_lowball / m"),
    )

st.altair_chart(chart, use_container_width=True)

st.subheader("Hover over each line for more info 📝")
