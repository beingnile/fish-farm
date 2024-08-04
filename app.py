import streamlit as st
from menu import menu

if "login" not in st.session_state:
    st.session_state.login = False
    st.rerun()
if "user" not in st.session_state:
    st.session_state.user = None
    st.rerun()

menu()
