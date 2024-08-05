import streamlit as st
from st_pages import add_page_title, get_nav_from_toml


def is_user_logged_in():
    return 'login' in st.session_state and st.session_state.login

def menu():
    # Show a navigation menu for authenticated users
    st.set_page_config(
        layout="wide",
        page_title='AquaSee Data',
        page_icon="💧"
    )

    st.logo('images/logo.png')

    logged_in = is_user_logged_in()

    home = st.Page("pages_/home.py", title="Home", icon=":material/home:", default=True)
    dashboard = st.Page("pages_/dashboard.py", title="Dashboard", icon=":material/dashboard:")
    login = st.Page("pages_/login.py", title="Login", icon=":material/login:")
    signup = st.Page("pages_/signup.py", title="Signup", icon=":material/person_add:")
    logout = st.Page("pages_/logout.py", title="Logout", icon=":material/logout:")

    page_dict = {}
    if logged_in:
        page_dict["Your Account"] = [dashboard, logout]
    else:
        page_dict["Welcome"] = [home, login, signup]

    pg = st.navigation(page_dict)

    pg.run()
