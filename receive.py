# streamlit_receiver.py
import streamlit as st
import requests
import time

st.title("Temperature Monitor")

#API_URL = "http://127.0.0.1:5000/data"  # URL of your API sender/receiver
API_URL = "https://backend-streamlit-pyxs.onrender.com/data"  # URL of your API sender/receiver
# Streamlit auto-refresh every few seconds
refresh_interval = 2  # seconds

placeholder_id = st.empty()
placeholder_temp = st.empty()

while True:
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            placeholder_id.subheader(f"ID: {data.get('id')}")
            placeholder_temp.text(f"Temperature: {data.get('temperature')} °C")
        else:
            placeholder_id.text("Error fetching data")
    except Exception as e:
        placeholder_id.text(f"Error: {e}")
    
    time.sleep(refresh_interval)
