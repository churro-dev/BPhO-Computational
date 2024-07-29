# Imports
from math import asin, atan, cos, degrees, sin, sqrt, tan

import altair as alt
import pandas as pd
import streamlit as st
from st_pages import add_indentation, show_pages_from_config

# Config page
PAGE_TITLE = "Task 5"
PAGE_ICON = ":memo:"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

add_indentation()

show_pages_from_config()

# Main Content

st.title("Task 5")
st.subheader(
    "Upgraded drag-free projectile motion model passing through a fixed position (X, Y)"
)

X = st.number_input(label="Target $X$ / $m$", min_value=0.0, max_value=None, value=(num := 1000.0), format=f"%.{len(str(num).split('.')[-1])}f") # spacing different here and below to make even

Y = st.number_input(label="Target$\ Y$ / $m$", min_value=0.0, max_value=None, value=(num := 300.0), format=f"%.{len(str(num).split('.')[-1])}f") # spacing different here and above to make even

g = st.number_input(
    label="Strength of gravity$\ g$ / $ms^{-2}$", min_value=0.1, max_value=None, value=(num := 9.81), format=f"%.{len(str(num).split('.')[-1])}f"
)


h = st.number_input(
    label="Initial height$\ h$ / $m$", min_value=0.0, max_value=None, value=(num := 0.0), format=f"%.{len(str(num).split('.')[-1])}f"
)

u_min = (sqrt(g) * sqrt(Y + sqrt((X**2) + (Y**2))))+0.0000000000001 # accounts for accuracy limitation causing domain error in theta_u_min_rad calculation

launch_speed_container = st.container(border=True)

with launch_speed_container:
    st.markdown(f"Minimum launch speed to reach target$\ u = {u_min:.2f} " + r"ms^{-1}$")

    apply_u = st.toggle("Apply minimum launch speed")

    if apply_u:
        u = st.number_input(
            label="Launch speed$\ u$ / $ms^{-1}$",
            min_value=u_min,
            max_value=None,
            value=u_min,
            format=f"%.{len(str(u_min).split('.')[-1])}f"
            disabled=True,
        )
    else:
        u = st.number_input(
            label="Launch speed$\ u$ / $ms^{-1}$",
            min_value=u_min,
            max_value=None,
            value=u_min * 1.15,
            format=f"%.{len(str(u_min * 1.15).split('.')[-1])}f"
            disabled=False,
        )

datapoints = st.number_input(
    label="Number of datapoints", min_value=1, max_value=1000, value=200
)  # determines how many points to calculate

# theta_u_min_rad = atan((Y + sqrt((X**2) + (Y**2))) / X)
# theta_u_min_rad = atan(((u_min**2)-(sqrt((u_min**4)-(g*((g*(X**2))+(2*Y*(u_min**2)))))))/(g*X))1
theta_u_min_rad = atan(((u_min**2)/(g*X))-sqrt((((u_min**2)*((u_min**2)-(2*g*(Y-h))))/((g**2)*(X**2)))-1))
# thank you to John Alexiou on the forum:
# https://physics.stackexchange.com/questions/56265/how-to-get-the-angle-needed-for-a-projectile-to-pass-through-a-given-point-for-t
# for having a working equation, as the challenge creators did not include the necessary equation for when you vary height

sin_theta_u_min = sin(theta_u_min_rad)
cos_theta_u_min = cos(theta_u_min_rad)

R_u_min = ((u_min**2) / g) * (
    (sin_theta_u_min * cos_theta_u_min)
    + (cos_theta_u_min * sqrt((sin_theta_u_min**2) + ((2 * g * h) / (u_min**2))))
)

delta_x_u_min = R_u_min / (datapoints - 1)

x_u_min = pd.Series([(delta_x_u_min * i) for i in range(datapoints)])

quadratic_a = (g / (2 * (u**2))) * (X**2)
quadratic_b = -X
quadratic_c = Y - h + ((g * (X**2)) / (2 * (u**2)))

quadratic_u = 2 * quadratic_a

quadratic_v = -quadratic_b / quadratic_u

quadratic_w = sqrt((quadratic_b**2) - (4 * quadratic_a * quadratic_c)) / quadratic_u

theta_lowball_rad = atan(quadratic_v - quadratic_w)

theta_highball_rad = atan(quadratic_v + quadratic_w)

sin_theta_lowball = sin(theta_lowball_rad)
cos_theta_lowball = cos(theta_lowball_rad)

R_lowball = ((u**2) / g) * (
    (sin_theta_lowball * cos_theta_lowball)
    + (cos_theta_lowball * sqrt((sin_theta_lowball**2) + ((2 * g * h) / (u**2))))
)

delta_x_lowball = R_lowball / (datapoints - 1)

x_lowball = pd.Series([(delta_x_lowball * i) for i in range(datapoints)])

sin_theta_highball = sin(theta_highball_rad)
cos_theta_highball = cos(theta_highball_rad)

R_highball = ((u**2) / g) * (
    (sin_theta_highball * cos_theta_highball)
    + (cos_theta_highball * sqrt((sin_theta_highball**2) + ((2 * g * h) / (u**2))))
)

delta_x_highball = R_highball / (datapoints - 1)

x_highball = pd.Series([(delta_x_highball * i) for i in range(datapoints)])

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
        + (x_u_min_i * tan_theta_u_min)
        - ((g / (2 * (u_min**2))) * (1 + (tan_theta_u_min**2)) * (x_u_min_i**2))
        for x_u_min_i in x_u_min
    ]
)
# # the above is equivalent to the below if you shift the below up by $h$:
# y_u_min = pd.Series(
#     [
#         (
#             (x_u_min_i * ((Y + sqrt((X**2)+(Y**2)))/(X)))
#             - ((x_u_min_i**2) * ((sqrt((X**2)+(Y**2)))/(X**2)))
#         )
#         for x_u_min_i in x_u_min
#     ]
# )

tan_theta_highball = tan(theta_highball_rad)

y_highball = pd.Series(
    [
        h
        + (x_highball_i * tan_theta_highball)
        - ((g / (2 * (u**2))) * (1 + (tan_theta_highball**2)) * (x_highball_i**2))
        for x_highball_i in x_highball
    ]
)

tan_theta_lowball = tan(theta_lowball_rad)

y_lowball = pd.Series(
    [
        h
        + (x_lowball_i * tan_theta_lowball)
        - ((g / (2 * (u**2))) * (1 + (tan_theta_lowball**2)) * (x_lowball_i**2))
        for x_lowball_i in x_lowball
    ]
)

R_max = ((u**2) / g) * sqrt(1 + ((2 * h * g) / (u**2)))

st.markdown(r"$R_{\text{max}} = " + f"{R_max:.2f}m$")

theta_R_max_rad = asin(1 / sqrt(2 + ((2 * g * h) / (u**2))))

tan_theta_R_max = tan(theta_R_max_rad)

st.markdown(r"$\theta_{R_{\text{max}}} = " + f"{degrees(theta_R_max_rad):.2f}\degree = " + f"{theta_R_max_rad:.2f}" + r"\ \text{rad}$")

delta_x_R_max = R_max / (datapoints - 1)

x_R_max = pd.Series([(delta_x_R_max * i) for i in range(datapoints)])

y_R_max = pd.Series(
    [
        h
        + (x_R_max_i * tan_theta_R_max)
        - ((g / (2 * (u**2))) * (1 + (tan_theta_R_max**2)) * (x_R_max_i**2))
        for x_R_max_i in x_R_max
    ]
)

x_bounding_parabola = x_R_max

y_bounding_parabola = pd.Series(
    [
        (h + ((u**2) / (2 * g)) - ((g / (2 * (u**2))) * (x_b_p_i**2)))
        for x_b_p_i in x_bounding_parabola
    ]
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
        "0": 0,
    }
)

base = alt.Chart(pos)

plot_points = st.toggle(label="Plot points instead of line?", value=False, help="If turned on, the connected lines will instead not be connected, and you can more clearly see the individually plotted points.")

if not plot_points:
    chart = alt.layer(
        base.mark_line(color="pink", strokeDash=[5, 5], strokeWidth=3).encode(
            x="x_bounding_parabola", y="y_bounding_parabola"
        ),
        base.mark_line().encode(x=alt.X("0", title="x / m"), y=alt.Y("0", title="y / m")), # ensures this point is not actually plotted as it's just for titling axis
        base.mark_line(color="grey", strokeWidth=3).encode(x="x_u_min", y="y_u_min"),
        base.mark_line(color="blue", strokeWidth=3).encode(x="x_highball", y="y_highball"),
        base.mark_line(color="green", strokeWidth=3).encode(x="x_lowball", y="y_lowball"),
        base.mark_line(color="red", strokeDash=[5, 5], strokeWidth=3).encode(x="x_R_max", y="y_R_max"),
    )
else:
    chart = alt.layer(
        base.mark_point(color="pink", size=5).encode(
            x="x_bounding_parabola", y="y_bounding_parabola"
        ),
        base.mark_line().encode(x=alt.X("0", title="x / m"), y=alt.Y("0", title="y / m")), # ensures this point is not actually plotted as it's just for titling axis
        base.mark_point(color="grey", size=5).encode(x="x_u_min", y="y_u_min"),
        base.mark_point(color="blue", size=5).encode(x="x_highball", y="y_highball"),
        base.mark_point(color="green", size=5).encode(x="x_lowball", y="y_lowball"),
        base.mark_point(color="red", size=5).encode(x="x_R_max", y="y_R_max"),
    )

st.altair_chart(chart, use_container_width=True)

st.subheader("Hover over each line for more info 📝")
