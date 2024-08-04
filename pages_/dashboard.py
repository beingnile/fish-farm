import base64
import firebase_admin
import folium
import json
import pandas as pd
import plotly.express as px
import streamlit as st
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from firebase_admin import credentials, db
from streamlit_folium import st_folium


# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate('servicekey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://fish-farm-ed34b-default-rtdb.firebaseio.com/'
    })

def load_private_key(file_path):
    with open(file_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)
    return private_key

def decrypt(encrypted_text):
    try:
        encrypted = base64.b64decode(encrypted_text)
        private_key = load_private_key('private_key.pem')
        decrypted_data = private_key.decrypt(encrypted, padding.PKCS1v15())
        return decrypted_data.decode('utf-8')
    except Exception as e:
        st.error(f"Decryption failed: {e}")
        return None

def get_sensor_data(user_id):
    try:
        dict_data = {}
        ref = db.reference(f'sensorData/{user_id}')
        data = ref.get()
        return data
    except Exception as e:
        st.error(f"Error getting sensor data: {e}")
        return None

def create_map(latitude, longitude):
    m = folium.Map(location=[latitude, longitude], zoom_start=15)
    folium.Marker([latitude, longitude], tooltip="Fish Farm").add_to(m)
    return m

def show_dashboard():
    st.markdown("""
    <style>
    .dashboard-title {
        text-align: center;
        color: #F63366;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="dashboard-title">Fish Farm Monitor</h1>', unsafe_allow_html=True)

    my_id = st.session_state.user

    sensor_data = get_sensor_data(my_id)

    if sensor_data:
        st.markdown("<hr>", unsafe_allow_html=True)  # Add horizontal line for separation
        decrypted_data = []
        for key, value in sensor_data.items():
            data = decrypt(value)
            if data:
                try:
                    decrypted_data.append(eval(data))
                except Exception as e:
                    st.error(f"Error processing decrypted data: {e}")
        df = pd.DataFrame(decrypted_data).sort_values(by='timestamp')
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        st.header("Overview")
        if not df.empty:
            first_row = df.iloc[0]
            avg_temp = round(df['temperature'].mean(), 2)
            avg_ph = round(df['ph'].mean(), 2)
            temp_range = round(df['temperature'].max() - df['temperature'].min(), 2)

            col1, col2, col3 = st.columns(3, gap='large')
            with col1:
                st.info("Latest Water Temperature")
                st.metric("", f"{first_row['temperature']} °C")
            with col2:
                st.info("Average Water Temperature")
                st.metric("", f"{avg_temp} °C")
            with col3:
                st.info("Temperature Range")
                st.metric("", f"{temp_range} °C")

            st.markdown("<hr>", unsafe_allow_html=True)  # Add horizontal line for separation

            st.subheader("Filter Data by Date Range")
            start_date = st.date_input("Start date", value=pd.to_datetime("2024-08-01"))
            end_date = st.date_input("End date", value=pd.to_datetime("today"))
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            filtered_df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
            st.dataframe(filtered_df)

            st.markdown("<hr>", unsafe_allow_html=True)  # Add horizontal line for separation

            st.subheader("Summary Statistics")
            if not filtered_df.empty:
                col1, col2 = st.columns(2, gap='large')
                with col1:
                    st.write("Temperature Statistics: This section provides summary statistics for temperature, including average, standard deviation, and percentiles for the water temperature, temp1, and temp2 sensors.")
                    st.write(filtered_df[['temperature', 'temp1', 'temp2']].describe())
                with col2:
                    st.write("pH Statistics: This section provides summary statistics for pH levels.")
                    st.write(filtered_df['ph'].describe())

            st.markdown("<hr>", unsafe_allow_html=True)  # Add horizontal line for separation

            st.subheader("Temperature Over Time")
            st.write("Temperature Over Time: This line chart displays how the water temperature has changed over the selected date range.")
            fig_temp = px.line(filtered_df, x='timestamp', y=['temperature'], title='Temperature Over Time', labels={'temperature': 'Temperature (°C)'})
            st.plotly_chart(fig_temp, use_container_width=True)

            st.subheader("pH Over Time")
            st.write("pH Over Time: This line chart shows the changes in pH levels over the selected date range.")
            fig_ph = px.line(filtered_df, x='timestamp', y='ph', title='pH Over Time', labels={'ph': 'pH Level'})
            st.plotly_chart(fig_ph, use_container_width=True)

            st.subheader("Temperature Histogram")
            st.write("Temperature Histogram: This histogram shows the distribution of temperature values recorded by the sensors. It helps in understanding the frequency of different temperature ranges.")
            fig_temp_hist = px.histogram(filtered_df.melt(id_vars='timestamp', value_vars=['temperature', 'temp1', 'temp2']), x='value', nbins=20, title='Temperature Histogram', color='variable', labels={'value': 'Temperature (°C)'})
            st.plotly_chart(fig_temp_hist, use_container_width=True)

            st.subheader("pH Histogram")
            st.write("pH Histogram: This histogram displays the distribution of pH levels recorded over the selected date range.")
            fig_ph_hist = px.histogram(filtered_df, x='ph', nbins=20, title='pH Histogram', labels={'ph': 'pH Level'})
            st.plotly_chart(fig_ph_hist, use_container_width=True)

            st.subheader("Temperature vs pH Scatter Plot")
            st.write("Temperature vs pH Scatter Plot: This scatter plot helps in analyzing the relationship between temperature and pH levels.")
            fig_scatter = px.scatter_matrix(filtered_df, dimensions=['temperature', 'temp1', 'temp2', 'ph'], title='Temperature vs pH Scatter Plot', labels={'temperature': 'Temperature (°C)', 'ph': 'pH Level'})
            st.plotly_chart(fig_scatter, use_container_width=True)

            st.markdown("<hr>", unsafe_allow_html=True)  # Add horizontal line for separation

            st.subheader("Temperature Comparison")
            st.write("Temperature Comparison: This line chart compares the water temperature recorded by different sensors (temperature, temp1, temp2) over time.")
            fig_temp_comparison = px.line(df, x='timestamp', y=['temperature', 'temp1', 'temp2'], title='Water Temperature Over Time', labels={'temperature': 'Temperature (°C)', 'temp1': 'Temp1 (°C)', 'temp2': 'Temp2 (°C)'})
            fig_temp_comparison.update_layout(
                xaxis_title="Date",
                yaxis_title="Temperature (°C)"
            )
            st.plotly_chart(fig_temp_comparison, use_container_width=True)

            st.subheader("Temperature Differences")
            st.write("Temperature Differences: This line chart shows the differences in temperature readings between the main sensor and the temp1/temp2 sensors.")
            df['temp_diff1'] = df['temperature'] - df['temp1']
            df['temp_diff2'] = df['temperature'] - df['temp2']
            fig_temp_diff = px.line(df, x='timestamp', y=['temp_diff1', 'temp_diff2'], title='Temperature Differences', labels={'temp_diff1': 'Temp Diff1 (°C)', 'temp_diff2': 'Temp Diff2 (°C)'})
            fig_temp_diff.update_layout(
                xaxis_title="Date",
                yaxis_title="Temperature Difference (°C)"
            )
            st.plotly_chart(fig_temp_diff, use_container_width=True)

            st.markdown("<hr>", unsafe_allow_html=True)  # Add horizontal line for separation

            col1, col2 = st.columns(2, gap='large')
            with col1:
                st.subheader("Fish Farm Location:")
                st.write("The map below shows the location of your fish farm. You can zoom in and out to see more details.")
                latitude = 0.506680
                longitude = 35.273170
                fish_farm_map = create_map(latitude, longitude)
                st_folium(fish_farm_map, width=700, height=500)

            with col2:
                # Actionable Insights
                st.subheader("Actionable Insights")
                if avg_temp > 30:
                    st.warning("Warning: Average water temperature is high. Consider cooling the water.")
                if avg_ph < 6.0:
                    st.warning("Warning: pH level is low. Consider adding pH buffer.")
                if temp_range > 5:
                    st.warning("Temperature range is high. Check for temperature fluctuations.")

                st.info("""
                Tips to enhance data protection:

                1. **Secure Your Access Credentials:** Ensure that all access credentials, including passwords and email information, are stored securely.

                2. **Monitor Hardware:** Regularly review your hardware to detect any unusual or unauthorized access attempts. Setting up alerts for suspicious activities can help in responding quickly to potential threats.

                3. **Educate Your Team:** Ensure that everyone involved in managing your farm understand best practices for data security and hardware maintainence. Regular training and awareness programs can help in minimizing human errors that could lead to data breaches.""")

            st.markdown("<hr>", unsafe_allow_html=True)  # Add horizontal line for separation

            # Data Export
            st.subheader("Export Data")
            st.write("You can download the filtered data as a CSV file for further analysis.")
            st.download_button(
                label="Download Filtered Data as CSV",
                data=filtered_df.to_csv(index=False).encode('utf-8'),
                file_name='filtered_data.csv',
                mime='text/csv'
            )
    else:
        st.write("No data available from Firebase.")

show_dashboard()

