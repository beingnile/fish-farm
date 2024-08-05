import streamlit as st


def wspace(num=5):
    for _ in range(num):
        st.write("")


def main_page():
    st.image("images/logo.png", width=200)
    st.markdown("""
    <style>
    h1 {
        color: #3F89AB;
        padding: 0;
    }

    [data-testid="stImage"] {
        display: block;
        text-align: center;
        margin-left: auto;
        margin-right: auto;
    }

    .landing-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 40vh;
        text-align: center;
        padding: 15px;
        padding-top: 20px;
    }
    .hero-section {
        padding-top: 15px;
        margin-bottom: 5px;
    }
    .hero-section h1 {
        width: 50%
        font-size: 3em;
        margin: 0;
    }
    .hero-section p {
        font-size: 1.5em;
        margin: 0;
    }
    @media (max-width: 768px) {
        .hero-section h1 {
            font-size: 2.5em;
        }
        .hero-section p {
            font-size: 1.2em;
        }
    }
    @media (max-width: 480px) {
        .hero-section h1 {
            font-size: 2em;
        }
        .hero-section p {
            font-size: 1em;
            margin-bottom: 0;
        }
        .hero-section {
            width: 50%;
        }
    }
    .row-widget.stButton {
        text-align: center;
    }
    [data-testid="baseButton-secondary"]:hover {
        color: #25A2D4;
        border: 1px solid #25A2D4;
    }
    </style>
    <div class="landing-container">
        <div class="hero-section">
            <h1>Securely Manage Your Fish Farm With Our Advanced Platform</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Get Started"):
        st.switch_page("pages_/login.py")

    wspace(17)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("About Us")
    wspace(3)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.image("images/undraw_analysis_dq08.svg", use_column_width=True)

    with col2:
        st.write("""
        At AquaSee, we are dedicated to revolutionizing the way you manage your fish farm.
        Our platform offers cutting-edge technology to monitor and maintain the health of your fish with ease and securely.
        """)

    wspace()

    st.subheader("Features")
    wspace(3)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.write("""
        - **Real-time Monitoring**: Get live updates on water temperature, pH levels, and other crucial parameters.

        - **Historical Data Analysis**: Analyze trends over time to make informed decisions.

        - **Encrypted Data Storage**: Your data is secured so you don't have to worry about that.

        - **User-Friendly Interface**: Our intuitive dashboard is designed for ease of use.
        """)

    with col2:
        st.image("images/undraw_fish_bowl_uu88.svg", use_column_width=True)

    wspace()

    st.subheader("How to Get Your Own AquaSee Data Fish Farm Sensor Pack")
    wspace(3)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.image("images/undraw_undraw_undraw_undraw_sign_up_ln1s_-1-_s4bc_-1-_ee41_-1-_kf4d.svg")

    with col2:
        st.write("""
        1. **Sign Up**: Create an account to start using our platform.

        2. **Set Up Sensor**: Receive the sensor pack with an easy-to-follow installation guide.

        2. **Log In**: Access your personal dashboard with your credentials once everything is up.

        3. **Monitor Your Farm**: Use the dashboard to keep an eye on your fish farm's health and performance.
        """)

    wspace()

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.header("Our Mission")
        wspace(3)
        st.info("""
        At AquaSee, our mission is to empower fish farmers with the tools they need to optimize their operations and maximize productivity securely.
        We believe that by leveraging technology, we can create a sustainable future for the aquaculture industry.
        We aim to reduce data breaches in the aquaculture industry by 14% by the next 5 years.
        """)

    with col2:
        st.header("Why Choose Us?")
        wspace(3)
        st.info("""
        - **Industry Expertise**: With years of experience in the aquaculture sector, our team understands the unique security challenges faced by fish farmers.

        - **Innovative Solutions**: Our platform is built with the latest technology to ensure reliable and accurate and secure monitoring of your fish farm.

        - **Customer Support**: We provide 24/7 customer support to assist you with any questions or issues you may have.

        - **Affordable Pricing**: Our solutions are designed to be cost-effective, offering great value without compromising on quality.
        """)

    with col3:
        st.header("Contact Us")
        wspace(3)
        st.info("""
        **Phone**: +254 721-311-522\n
        **Email**: support@aquadata.com\n
        **Address**: 123 Fish Farm Road, Aquatic City, Fishland\n
        """)

    wspace()


main_page()
