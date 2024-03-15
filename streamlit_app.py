""" Main Streamlit site file """

from yaml.loader import SafeLoader
import yaml

import streamlit as st
import streamlit_authenticator as stauth

# Uncomment below if you need cookies:
# import extra_streamlit_components as stx

# Config page
PAGE_TITLE = ""
PAGE_ICON = ""
st.set_page_config(
    PAGE_TITLE, PAGE_ICON, layout="wide", initial_sidebar_state="collapsed"
)
#

# Checks for empty variables
if not PAGE_TITLE:
    raise ValueError(
        "Please set the PAGE_TITLE variable to the title of your app")

if not PAGE_ICON:
    raise ValueError(
        "Please set the PAGE_ICON variable to the icon of your app")
#

with open('config.yaml', 'r', encoding="utf-8") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login()

auth_state = st.session_state["authentication_status"]
if auth_state is False or auth_state is None:
    st.error('Username/password is incorrect')
    try:
        email, username, name = authenticator.register_user(
            preauthorization=False)
        if email:
            st.success('User registered successfully')
            with open('config.yaml', 'w', encoding="utf-8") as file:
                yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)
else:
    # LOGGED IN CONTENT
    pass
