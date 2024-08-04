import firebase_admin
import json
import os
import requests
import streamlit as st
from dotenv import load_dotenv, dotenv_values
from firebase_admin import credentials, auth

load_dotenv()

encoded_key = os.getenv("SECRET_KEY")

json_key = json.loads(base64.b64decode(encoded_key).decode('utf-8'))

if not firebase_admin._apps:
    cred = credentials.Certificate('servicekey.json' or json_key)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://fish-farm-ed34b-default-rtdb.firebaseio.com/'
    })

def create_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return user.uid
    except Exception as e:
        st.error(f"Error creating user: {e}")
        return None

def sign_in(email, password):
    api_key = os.getenv("API_KEY")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    return response.json()

def sign_out():
    try:
        auth.sign_out()
        print("Signed out successfully.")
    except Exception as e:
        print(f"Error signing out: {e}")

def sign_in_with_google(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return uid
    except Exception as e:
        print(f"Error signing in with Google: {e}")
        return None

def sign_in_with_apple(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return uid
    except Exception as e:
        print(f"Error signing in with Apple: {e}")
        return None
