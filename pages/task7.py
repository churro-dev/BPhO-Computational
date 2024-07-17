# Imports
from math import asin, cos, degrees, radians, sin, sqrt, tan

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
    label="Number of datapoints", min_value=1, max_value=1000, value=200
)  # determines how many points to calculate

angles = st_tags(
    label='Angles (type & press **enter** to add more)',
    text='Press enter to add more',
    value=['30', '45', '60', '70.53', '78', '85'],
    maxtags = 148,
    key='1'
)
thetas_deg = []
for angle in angles:
    try:
        thetas_deg.append(float(angle))
    except ValueError:
        pass
thetas_rad = [radians(theta_deg) for theta_deg in thetas_deg]

# Downards direction is negative, input is positive
# Gravity always acts downards, so negative g_strength to get acceleration
acceleration = -g

R_max = ((u**2) / g) * sqrt(1 + ((2 * h * g) / (u**2)))

theta_deg = degrees(asin(1 / sqrt(2 + ((2 * g * h) / (u**2)))))

threshold_rad = asin((2*sqrt(2))/3)
threshold_deg = degrees(threshold_rad)

# For convenience
sin_theta_R = sin(radians(theta_deg))
cos_theta_R = cos(radians(theta_deg))
tan_theta_R = tan(radians(theta_deg))

sin_thetas_R = [sin(radians(theta_deg)) for theta_deg in thetas_deg]
cos_thetas_R = [cos(radians(theta_deg)) for theta_deg in thetas_deg]
tan_thetas_R = [tan(radians(theta_deg)) for theta_deg in thetas_deg]


R = ((u**2) / g) * ((sin_theta_R * cos_theta_R)+ (cos_theta_R * sqrt((sin_theta_R**2) + ((2 * g * h) / (u**2)))))
Rs = [((u**2) / g) * ((sin_theta_R * cos_theta_R)+ (cos_theta_R * sqrt((sin_theta_R**2) + ((2 * g * h) / (u**2)))) ) for sin_theta_R, cos_theta_R in zip(sin_thetas_R, cos_thetas_R)]

T_R = R / (u * cos_theta_R)
T_Rs = [R / (u * cos_theta_R) for R, cos_theta_R in zip(Rs, cos_thetas_R)]
T_Rs_dict = {"t_R_"+(str(theta_deg).replace(".", "․")): T_R for theta_deg, T_R in zip(thetas_deg, T_Rs)}

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

rs_pos = [pd.Series([sqrt((x**2)+(y**2)) for x, y in zip(x_pos_R, y_pos_R)]) for x_pos_R, y_pos_R in zip(x_pos_Rs, y_pos_Rs)]
rs_pos_dict = {"r_"+(str(theta_deg).replace(".", "․")):R_pos for R_pos, theta_deg in zip(rs_pos, thetas_deg)}

t = pd.Series([x_pos_R_i / (u * cos_theta_R) for x_pos_R_i in x_pos_R])
ts = [pd.Series([x_pos_R_i / (u * cos_theta_R) for x_pos_R_i in x_pos_R]) for x_pos_R, cos_theta_R in zip(x_pos_Rs, cos_thetas_R)]
ts_dict = {"t_" + (str(theta_deg).replace(".", "․")): t for theta_deg, t in zip(thetas_deg, ts)}

angle_points = {}
for angle, angle_rad in zip(thetas_deg, thetas_rad):
    if angle >= threshold_deg:
        t_min = ((3*u)/(2*g))*(sin(radians(angle)) - sqrt((sin(radians(angle))**2) - (8/9)))
        t_max = ((3*u)/(2*g))*(sin(radians(angle)) + sqrt((sin(radians(angle))**2) - (8/9)))
        
        angle_points[(angle_str := str(angle).replace(".", "․")+"_min")+"_x"], angle_points[angle_str+"_y"] = (x:= u*t_min*cos(radians(angle))), (h + (x * tan(radians(angle))) - ((g / (2 * (u**2))) * (1 + (tan(radians(angle))**2)) * (x**2)))
        angle_points[(angle_str := str(angle).replace(".", "․")+"_max")+"_x"], angle_points[angle_str+"_y"] = (x:= u*t_max*cos(radians(angle))), (h + (x * tan(radians(angle))) - ((g / (2 * (u**2))) * (1 + (tan(radians(angle))**2)) * (x**2)))
        angle_points[(angle_str := str(angle).replace(".", "․")+"_min")+"_t"] = t_min
        angle_points[(angle_str := str(angle).replace(".", "․")+"_max")+"_t"] = t_max
        angle_points[str(angle).replace(".", "․")+"_min_r"] = sqrt(((u**2)*(t_min**2))-((g)*(t_min**3)*(u)*(sin(angle_rad)))+((1/4)*(g**2)*(t_min**4)))
        angle_points[str(angle).replace(".", "․")+"_max_r"] = sqrt(((u**2)*(t_max**2))-((g)*(t_max**3)*(u)*(sin(angle_rad)))+((1/4)*(g**2)*(t_max**4)))

plot_points = st.toggle(label="Plot points instead of line?", value=False, help="If turned on, the connected lines will instead not be connected, and you can more clearly see the individually plotted points.")

theme = st_theme()
if theme != None:
    if theme['base'] == 'light':
        colors = ['black', 'silver', 'gray', 'maroon', 'red', 'purple', 'fuchsia', 'green', 'lime', 'olive', 'yellow', 'navy', 'blue', 'teal', 'aqua', 'orange', 'aquamarine', 'azure', 'beige', 'bisque', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'forestgreen', 'gainsboro', 'gold', 'goldenrod', 'greenyellow', 'grey', 'hotpink', 'indianred', 'indigo', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'limegreen', 'linen', 'magenta', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'midnightblue', 'moccasin', 'oldlace', 'olivedrab', 'orangered', 'orchid', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'sienna', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'yellowgreen', 'rebeccapurple']
    else:
        colors = ['silver', 'gray', 'white', 'maroon', 'red', 'purple', 'fuchsia', 'green', 'lime', 'olive', 'yellow', 'navy', 'blue', 'teal', 'aqua', 'orange', 'aliceblue', 'antiquewhite', 'aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'limegreen', 'linen', 'magenta', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'oldlace', 'olivedrab', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'whitesmoke', 'yellowgreen', 'rebeccapurple']
       

    for i, line in enumerate(list(x_pos_Rs_dict)):
        new_key = f"x_{str(thetas_deg[i])}".replace(".", "․")
        x_pos_Rs_dict[new_key] = x_pos_Rs_dict.pop(line)
    
    for i, line in enumerate(list(y_pos_Rs_dict)):
        new_key = f"y_{str(thetas_deg[i])}".replace(".", "․")
        y_pos_Rs_dict[new_key] = y_pos_Rs_dict.pop(line)
    
    pos = pd.DataFrame(
        {**{
            "t / s": t,
        },
        **ts_dict,
        **x_pos_Rs_dict,
        **y_pos_Rs_dict,
        **rs_pos_dict,
        **angle_points
        }
    )

    n = len(x_pos_Rs)
    if n != 0:
        n_distance = len(colors) / n
        chosen = []
        for i in range(n):
            chosen.append(colors[round(i * n_distance)])

        base = alt.Chart(pos)

        for i, color, angle in zip(range(len(x_pos_Rs)), chosen, thetas_deg):
            x_search_str = f"x_{angle}".replace(".", "․") # SECOND CHARACTER IS (U+2024) RATHER THAN (U+002E)
            y_search_str = f"y_{angle}".replace(".", "․") # SECOND CHARACTER IS (U+2024) RATHER THAN (U+002E)
            t_search_str = f"t_{angle}".replace(".", "․") # SECOND CHARACTER IS (U+2024) RATHER THAN (U+002E)
            r_search_str = f"r_{angle}".replace(".", "․") # SECOND CHARACTER IS (U+2024) RATHER THAN (U+002E)
            if not plot_points:
                if i == 0:
                    chart_one = alt.layer(
                        base.mark_line(color=color, strokeWidth=5).encode(
                            x=alt.X(x_search_str, title="x / m"),
                            y=alt.Y(y_search_str, title="y / m"),
                        )
                    )
                    chart_two = alt.layer(
                        base.mark_line(color=color, strokeWidth=5).encode(
                            x=alt.X(t_search_str, title="t / s"),
                            y=alt.Y(r_search_str, title="range  r / m"), # double space is intentional to separate title from units
                        )
                    )
                else:
                    chart_one += base.mark_line(color=color, strokeWidth=5).encode(
                        alt.X(x_search_str),
                        alt.Y(y_search_str),
                    )
                    chart_two += base.mark_line(color=color, strokeWidth=5).encode(
                        x=alt.X(t_search_str),
                        y=alt.Y(r_search_str),
                    )
            else:
                if i == 0:
                    chart_one = alt.layer(
                        base.mark_point(color=color, size=30).encode(
                            x=alt.X(x_search_str, title="x / m"),
                            y=alt.Y(y_search_str, title="y / m"),
                        )
                    )
                    chart_two = alt.layer(
                        base.mark_point(color=color, size=30).encode(
                            x=alt.X(t_search_str, title="t / s"),
                            y=alt.Y(r_search_str, title="range r / m"),
                        )
                    )
                else:
                    chart_one += base.mark_point(color=color, size=30).encode(
                        alt.X(x_search_str),
                        alt.Y(y_search_str),
                    )
                    chart_two += base.mark_point(color=color, size=30).encode(
                        x=alt.X(t_search_str),
                        y=alt.Y(r_search_str),
                    )

            if angle >= threshold_deg:
                angle_point_min_x_search_str = f"{angle}_min_x".replace(".", "․") # SECOND CHARACTER IS (U+2024) RATHER THAN (U+002E)
                angle_point_min_y_search_str = f"{angle}_min_y".replace(".", "․") # SECOND CHARACTER IS (U+2024) RATHER THAN (U+002E)
                angle_point_max_x_search_str = f"{angle}_max_x".replace(".", "․") # SECOND CHARACTER IS (U+2024) RATHER THAN (U+002E)
                angle_point_max_y_search_str = f"{angle}_max_y".replace(".", "․") # SECOND CHARACTER IS (U+2024) RATHER THAN (U+002E)
                angle_point_min_t_search_str = f"{angle}_min_t".replace(".", "․") # SECOND CHARACTER IS (U+2024) RATHER THAN (U+002E)
                angle_point_min_r_search_str = f"{angle}_min_r".replace(".", "․") # SECOND CHARACTER IS (U+2024) RATHER THAN (U+002E)
                angle_point_max_t_search_str = f"{angle}_max_t".replace(".", "․") # SECOND CHARACTER IS (U+2024) RATHER THAN (U+002E)
                angle_point_max_r_search_str = f"{angle}_max_r".replace(".", "․") # SECOND CHARACTER IS (U+2024) RATHER THAN (U+002E)
                chart_one += base.mark_point(color="pink" if color!="pink" else "purple", shape="diamond", size=10).encode(
                    x=alt.X(angle_point_min_x_search_str),
                    y=alt.Y(angle_point_min_y_search_str),
                )
                chart_one += base.mark_point(color="black" if color!="black" else "gray", shape="diamond", size=10).encode(
                    x=alt.X(angle_point_max_x_search_str),
                    y=alt.Y(angle_point_max_y_search_str),
                )
                chart_two += base.mark_point(color="pink" if color!="pink" else "purple", shape="diamond", size=10).encode(
                    x=alt.X(angle_point_min_t_search_str),
                    y=alt.Y(angle_point_min_r_search_str),
                )
                chart_two += base.mark_point(color="black" if color!="black" else "gray", shape="diamond", size=10).encode(
                    x=alt.X(angle_point_max_t_search_str),
                    y=alt.Y(angle_point_max_r_search_str),
                )

        st.altair_chart(chart_one, use_container_width=True)
        st.altair_chart(chart_two, use_container_width=True)

        st.subheader("Hover over each line for more info 📝")
