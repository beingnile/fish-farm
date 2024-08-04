import streamlit as st
from utilities import auth


st.session_state.user = None
st.session_state.login = False
st.rerun()
