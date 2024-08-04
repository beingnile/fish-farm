import base64
import folium
import pandas as pd
import plotly.express as px
import streamlit as st
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from firebase_admin import credentials, db
from menu import menu
from streamlit_folium import st_folium

if "login" not in st.session_state:
    st.session_state.login = False
    st.rerun()
if "user" not in st.session_state:
    st.session_state.user = None
    st.rerun()

menu()
