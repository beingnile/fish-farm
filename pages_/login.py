import streamlit as st
from firebase_admin import auth
from menu import menu
from utilities.auth import sign_in


css_styles = """
/* Style your containers */
[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
    border: 20px groove red;
    margin-top: 20px;
    padding: 20px;
}

[data-testid="stForm"] {
    width: 90%;
    margin: 0 auto;
}

@media (min-width: 768px) {
    [data-testid="stForm"] {
        width: 75%;
    }
}

@media (min-width: 1024px) {
    [data-testid="stForm"] {
        width: 60%;
    }
}

/* Style your text inputs */
[data-testid="stTextInput"] {
    width: 100%;
    padding: 10px;
    border-radius: 8px;
    font-size: 1em;
    margin-bottom: 1px;
}

/* Style your buttons */
[data-testid="baseButton-secondaryFormSubmit"] {
    width: 60%;
    margin: 0 auto;
    padding: 8px;
    border-radius: 8px;
    font-size: 1em;
    cursor: pointer;
    margin-top: 10px;
    display: flex;
    justify-content: center;
}
[data-testid="baseButton-secondaryFormSubmit"]:hover {
    border: 1px solid #25A2D4;
    color: #25A2D4;
}

.login-link {
    margin-top: 20px;
    font-size: 1em;
    color: #F63366;
    text-decoration: underline;
    cursor: pointer;
}
"""

st.markdown(f"<style>{css_styles}</style>", unsafe_allow_html=True)


def show_login_page():
    st.markdown("""
    <style>
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 15vh;
        padding: 5px;
    }
    .login-container h1 {
        font-size: 2.5em;
        margin-bottom: 5px;
        color: #3F89AB;
    }
    .login-container .form-input input {
        width: 100%;
        padding: 15px;
        border: 1px solid #d0d0d0;
        border-radius: 8px;
        font-size: 1em;
        margin-bottom: 15px;
    }
    .login-container .form-input button {
        width: 100%;
        padding: 15px;
        border: none;
        border-radius: 8px;
        font-size: 1em;
        background-color: #F63366;
        color: white;
        cursor: pointer;
        margin-top: 10px;
    }
    .login-container .form-input button:hover {
        background-color: #d02b52;
    }
    @media (max-width: 768px) {
        .login-container h1 {
            font-size: 2em;
        }
    }
    </style>
    <div class="login-container">
        <h1>Dashboard login</h1>
        <div class="form-input">
    """, unsafe_allow_html=True)

    with st.form(key='someval'):
        email = st.text_input("Email", key="email")
        password = st.text_input("Password", type="password", key="password")
        submit_button = st.form_submit_button(label='Sign In')

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

    if submit_button:
        user = sign_in(email, password)
        if "idToken" in user:
            st.session_state.token = auth.verify_id_token(user["idToken"])
            st.session_state.user = st.session_state.token.get("uid")
            with st.spinner():
                st.session_state.login = True
                st.rerun()
            st.success(f"Signed in successfully.")
        else:
            st.error("Invalid credentials")

show_login_page()
