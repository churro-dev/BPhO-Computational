# Imports

from math import cos, radians, sin, sqrt, tan

import altair as alt
import pandas as pd
import streamlit as st
from st_pages import add_indentation, show_pages_from_config

# Config page
PAGE_TITLE = "Task 9"
PAGE_ICON = ":memo:"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

add_indentation()

show_pages_from_config()

# Main Content

st.title("Task 9")
st.subheader("Numerical model of projectile motion with air resistance")

theta = st.slider(
    label="Launch angle from horizontal /$\ $°", # even out spacing
    min_value=0.0,
    max_value=90.0,
    value=30.0,
    step=0.1
)
theta_rad = radians(theta)

g = st.number_input(
    label="Strength of gravity$\ g$ / $ms^{-2}$", min_value=0.1, max_value=None, value=(num := 9.81), format=f"%.{len(str(num).split('.')[-1])}f"
)

u = st.number_input(
    label="Launch speed$\ u$ / $ms^{-1}$", min_value=0.1, max_value=None, value=(num := 20.0), format=f"%.{len(str(num).split('.')[-1])}f"
)

h = st.number_input(
    label="Initial height$\ h$ / $m$", min_value=0.0, max_value=None, value=(num := 2.0), format=f"%.{len(str(num).split('.')[-1])}f"
)

container = st.container(border=True)
with container:
    
    custom = st.toggle(label="Use custom drag coefficient", value=True, help="Turn on to use a custom drag coefficient rather than a preset shape.")
    
    shape = st.selectbox(
        label="Shape of projectile",
        options=["Sphere", "Half-sphere", "Cone", "Cube", "Angled Cube", "Long Cylinder", "Short Cylinder", "Streamlined Body", "Streamlined Half-body"],
        index=0,
        disabled=custom
    )
    
    drag_convert = {
        "Sphere": 0.47,
        "Half-sphere": 0.42,
        "Cone": 0.50,
        "Cube": 1.05,
        "Angled Cube": 0.80,
        "Long Cylinder": 0.82,
        "Short Cylinder": 1.15,
        "Streamlined Body": 0.04,
        "Streamlined Half-body": 0.09
    }
    
    if custom:
        default = 0.1
    else:
        default = drag_convert[shape]
    
    cD = st.number_input(
        label="Drag coefficient$\ C_D$",
        min_value=0.0,
        max_value=None,
        value=default,
        format=f"%.{len(str(num).split('.')[-1])}f",
        disabled=(not custom)
    )

A = st.number_input(
    label="Cross-sectional area$\ A$ / $m^2$", min_value=0.0, max_value=None, value=(num := 0.007854), format=f"%.{len(str(num).split('.')[-1])}f"
)

rho = st.number_input(
    label="Air density$\ \\rho$ / $kgm^{-3}$", min_value=0.0, max_value=None, value=(num := 1.0), format=f"%.{len(str(num).split('.')[-1])}f"
)

m = st.number_input(
    label="Mass$\ m$ / $kg$", min_value=0.0, max_value=None, value=(num := 0.1), format=f"%.{len(str(num).split('.')[-1])}f"
)

dt = st.number_input(
    label="Time step$\ dt$ / $s$", min_value=0.0, max_value=None, value=(num := 0.01), format=f"%.{len(str(num).split('.')[-1])}f"
)

datapoints = st.number_input(
    label="Number of datapoints", min_value=1, max_value=1000, value=200
)  # determines how many points to calculate

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

x_dragless_pos = [(distance_increment * i) for i in range(datapoints)]

x_dragless_a = ((u**2) / g) * sin_theta * cos_theta

y_dragless_a = h + (((u**2) / (2 * g)) * (sin_theta**2))

T = R / (u * cos_theta)

t_dragless = [x_pos_i / (u * cos_theta) for x_pos_i in x_dragless_pos]

y_dragless_pos = [
    h
    + (x_pos_i * tan_theta)
    - ((g / (2 * (u**2))) * (1 + (tan_theta**2)) * (x_pos_i**2))
    for x_pos_i in x_dragless_pos
]


# Initial conditions

k = (0.5 * cD * rho * A) / m

t_drag = [0]
x_drag_pos = [0]
y_drag_pos = [h]
v_drag = [u]
v_drag_x = [u * cos_theta]
v_drag_y = [u * sin_theta]

while True:
    
    t = t_drag[-1] + dt
    t_drag.append(t)
    
    a_x = - (v_drag_x[-1] * k * v_drag[-1])
    a_y = - g - (v_drag_y[-1] * k * v_drag[-1])
    
    x = x_drag_pos[-1] + (v_drag_x[-1] * dt) + (0.5 * a_x * (dt**2))
    x_drag_pos.append(x)
    
    y = y_drag_pos[-1] + (v_drag_y[-1] * dt) + (0.5 * a_y * (dt**2))
    y_drag_pos.append(y)
    
    v_x = v_drag_x[-1] + (a_x * dt)
    v_drag_x.append(v_x)
    
    v_y = v_drag_y[-1] + (a_y * dt)
    v_drag_y.append(v_y)
    
    v = sqrt((v_drag_x[-1]**2) + (v_drag_y[-1]**2))
    v_drag.append(v)
    
    if y <= 0:
        break

if y_drag_pos[-1] < 0:
    y_drag_pos.pop(-1)
    x_drag_pos.pop(-1)

y_drag_a = max(y_drag_pos)
x_drag_a = x_drag_pos[y_drag_pos.index(y_drag_a)]

len_x_dragless_pos = len(x_dragless_pos)
len_x_drag_pos = len(x_drag_pos)

if len_x_dragless_pos < len_x_drag_pos:
    diff = len_x_drag_pos - len_x_dragless_pos
    x_dragless_pos += ([0]*diff)
    y_dragless_pos += ([h]*diff)
elif len_x_dragless_pos > len_x_drag_pos:
    diff = len_x_dragless_pos - len_x_drag_pos
    x_drag_pos += ([0]*diff)
    y_drag_pos += ([h]*diff)
else:
    pass

format_val = len(str(k).split('.')[-1])
st.markdown(r"Air resistance factor$\ k = " + f"{round(k, format_val)}$")

pos = pd.DataFrame(
    {
        "x_drag-free / m": x_dragless_pos,
        "y_drag-free / m": y_dragless_pos,
        "x_drag-free_a / m": x_dragless_a,
        "y_drag-free_a / m": y_dragless_a,
        "drag-free": "drag-free",
        
        "x_drag / m": x_drag_pos,
        "y_drag / m": y_drag_pos,
        "x_drag_a / m": x_drag_a,
        "y_drag_a / m": y_drag_a,
        "with drag": "with drag"
    }
)

plot_points = st.toggle(label="Plot points instead of line?", value=False, help="If turned on, the connected lines will instead not be connected, and you can more clearly see the individually plotted points.")

if not plot_points:
    chart_dragless = (
        alt.Chart(pos)
        .mark_line(strokeWidth=4)
        .encode(
            x=alt.X("x_drag-free / m", title="x / m"), y=alt.Y("y_drag-free / m", title="y / m"),
            tooltip=alt.Tooltip(["x_drag-free / m", "y_drag-free / m", "drag-free"])
        )
    )
    chart_drag = (
        alt.Chart(pos)
        .mark_line(strokeWidth=4)
        .encode(
            x=alt.X("x_drag / m"), y=alt.Y("y_drag / m"),
            tooltip=alt.Tooltip(["x_drag / m", "y_drag / m", "with drag"])
        )
    )
else:
    chart_dragless = (
        alt.Chart(pos)
        .mark_circle(size=15)
        .encode(
            x=alt.X("x_drag-free / m", title="x / m"), y=alt.Y("y_drag-free / m", title="y / m"),
            tooltip=alt.Tooltip(["x_drag-free / m", "y_drag-free / m", "drag-free"])
        )
    )
    chart_drag = (
        alt.Chart(pos)
        .mark_circle(size=15)
        .encode(
            x=alt.X("x_drag / m"), y=alt.Y("y_drag / m"),
            tooltip=alt.Tooltip(["x_drag / m", "y_drag / m", "with drag"])
        )
    )

point_dragless = (
    alt.Chart(pos)
    .mark_point(color="red", size=50, shape="diamond").encode(x="x_drag-free_a / m", y="y_drag-free_a / m")
)

point_drag = (
    alt.Chart(pos)
    .mark_point(color="red", size=50, shape="diamond").encode(x="x_drag_a / m", y="y_drag_a / m")
)

# Combine the chart and the point
st.altair_chart(chart_dragless + chart_drag + point_dragless + point_drag, use_container_width=True)

st.subheader("Hover over the line and apogee for more info 📝")
