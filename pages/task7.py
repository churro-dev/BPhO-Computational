# Imports
from math import asin, cos, degrees, radians, sin, sqrt, tan, log

import altair as alt
import pandas as pd
import streamlit as st
from streamlit_tags import st_tags
from streamlit_theme import st_theme
from st_pages import add_indentation, show_pages_from_config

# Config page
PAGE_TITLE = "Task 7"
PAGE_ICON = "📝"
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="expanded"
)

add_indentation()

show_pages_from_config()

# Main Content

st.title("Task 7")
st.subheader("Range of projectile vs. time - maxima & minima")

g = st.number_input(
    label="Strength of gravity (m/s²)", min_value=0.1, max_value=None, value=9.81
)

u = st.number_input(
    label="Launch speed (m/s)", min_value=0.1, max_value=None, value=10.0
)

h = 0

datapoints = st.number_input(
    label="Number of datapoints", min_value=1, max_value=5000, value=1000
)  # determines how many points to calculate

angles = st_tags(
    label='# Enter Keywords:',
    text='Press enter to add more',
    value=['30', '45', '60', '70.5', '78', '85'],
    maxtags = 148,
    key='1'
)
theta_degs = []
for angle in angles:
    try:
        theta_degs.append(float(angle))
    except:
        pass

# Downards direction is negative, input is positive
# Gravity always acts downards, so negative g_strength to get acceleration
acceleration = -g

R_max = ((u**2) / g) * sqrt(1 + ((2 * h * g) / (u**2)))

theta_deg = degrees(asin(1 / sqrt(2 + ((2 * g * h) / (u**2)))))

# For convenience
sin_theta_R = sin(radians(theta_deg))
cos_theta_R = cos(radians(theta_deg))
tan_theta_R = tan(radians(theta_deg))

sin_thetas_R = [sin(radians(theta_deg)) for theta_deg in theta_degs]
cos_thetas_R = [cos(radians(theta_deg)) for theta_deg in theta_degs]
tan_thetas_R = [tan(radians(theta_deg)) for theta_deg in theta_degs]

R = ((u**2) / g) * ((sin_theta_R * cos_theta_R)+ (cos_theta_R * sqrt((sin_theta_R**2) + ((2 * g * h) / (u**2)))))
Rs = [((u**2) / g) * ((sin_theta_R * cos_theta_R)+ (cos_theta_R * sqrt((sin_theta_R**2) + ((2 * g * h) / (u**2)))) ) for sin_theta_R, cos_theta_R in zip(sin_thetas_R, cos_thetas_R)]

T_R = R / (u * cos_theta_R)
T_Rs = [R / (u * cos_theta_R) for R, cos_theta_R in zip(Rs, cos_thetas_R)]

distance_increment_R = R / (datapoints - 1)
distance_increment_Rs = [R / (datapoints - 1) for R in Rs]

x_pos_R = pd.Series([(distance_increment_R * i) for i in range(datapoints)])
x_pos_Rs = [pd.Series([(distance_increment_R * i) for i in range(datapoints)]) for distance_increment_R in distance_increment_Rs]
x_pos_Rs_dict = {f"x_pos_R_{i} / m": x_pos_R for i, x_pos_R in enumerate(x_pos_Rs)}


y_pos_Rs = [pd.Series(
    [
        h
        + (x_pos_R_i * tan_thetas_R[i])
        - ((g / (2 * (u**2))) * (1 + (tan_thetas_R[i]**2)) * (x_pos_R_i**2))
        for x_pos_R_i in x_pos_R
    ]
) for i, x_pos_R in enumerate(x_pos_Rs)]
y_pos_Rs_dict = {f"y_pos_R_{i} / m": y_pos_R for i, y_pos_R in enumerate(y_pos_Rs)}


t_R = pd.Series([x_pos_R_i / (u * cos_theta_R) for x_pos_R_i in x_pos_R])


pos = pd.DataFrame(
    {**{
        "t_R / s": t_R,
    },
     **x_pos_Rs_dict,
     **y_pos_Rs_dict
    }
)


theme = st_theme()
if theme != None:
    if theme['base'] == 'light':
        colors = ['black', 'silver', 'gray', 'maroon', 'red', 'purple', 'fuchsia', 'green', 'lime', 'olive', 'yellow', 'navy', 'blue', 'teal', 'aqua', 'orange', 'aliceblue', 'aquamarine', 'azure', 'beige', 'bisque', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'forestgreen', 'gainsboro', 'gold', 'goldenrod', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'limegreen', 'linen', 'magenta', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'oldlace', 'olivedrab', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'yellowgreen', 'rebeccapurple']
    else:
        colors = ['silver', 'gray', 'white', 'maroon', 'red', 'purple', 'fuchsia', 'green', 'lime', 'olive', 'yellow', 'navy', 'blue', 'teal', 'aqua', 'orange', 'aliceblue', 'antiquewhite', 'aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'limegreen', 'linen', 'magenta', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'oldlace', 'olivedrab', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'whitesmoke', 'yellowgreen', 'rebeccapurple']

    n = len(x_pos_Rs)
    if n != 0:
        n_distance = len(colors) / n
        chosen = []
        for i in range(n):
            chosen.append(colors[round(i * n_distance)])
        print(chosen)

        base = alt.Chart(pos)

        for i, color in zip(range(len(x_pos_Rs)), chosen):
            if i == 0:
                chart = alt.layer(
                    base.mark_point(color=color).encode(
                        x=alt.X(f"x_pos_R_{i} / m", title="x / m"),
                        y=alt.Y(f"y_pos_R_{i} / m", title="y / m"),
                        strokeWidth=("t_R / s"),
                    )
                )
            else:
                chart += base.mark_point(color=color).encode(
                    alt.X(f"x_pos_R_{i} / m"),
                    alt.Y(f"y_pos_R_{i} / m"),
                    strokeWidth=(f"t_R / s"),
                )

        st.altair_chart(chart, use_container_width=True)

        st.subheader("Hover over each line for more info 📝")
