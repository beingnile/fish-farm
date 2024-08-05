import streamlit as st
from utilities.auth import create_user

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
    color: #25A2D4;
    border: 1px solid #25A2D4;
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

def show_signup_page():
    st.markdown("""
    <style>
    .signup-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 15vh;
        padding: 5px;
    }
    .signup-container h1 {
        font-size: 2.5em;
        margin-bottom: 5px;
        color: #3F89AB;
    }
    @media (max-width: 768px) {
        .signup-container h1 {
            font-size: 2em;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="signup-container">
        <h1>Register for AquaSee Data</h1>
    """, unsafe_allow_html=True)

    with st.form(key='signup_form'):
        name = st.text_input("Name", key="username")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        submit_button = st.form_submit_button(label='Sign Up')

    st.markdown("</div>", unsafe_allow_html=True)

    if submit_button:
        user = create_user(email, password)
        if user:
            st.success("User created successfully. Please sign in.")
            st.switch_page("pages_/login.py")
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Error creating user")


show_signup_page()
