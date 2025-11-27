# streamlit_receiver.py
import streamlit as st
import requests
import time
import csv
import os
import pandas as pd

st.title("Temperature Monitor with CSV Logging")

API_URL = "https://backend-streamlit-pyxs.onrender.com/data"
refresh_interval = 2  # seconds

placeholder_id = st.empty()
placeholder_temp = st.empty()

CSV_FILE = "data_log.csv"


# ----------------------------
# CREATE CSV IF NOT EXISTS
# ----------------------------
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Temperature", "Timestamp"])


# ----------------------------
# STREAMLIT DOWNLOAD BUTTON
# ----------------------------
st.subheader("Download Logged Data")

def show_download_button():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        st.download_button(
            label="Download CSV File",
            data=df.to_csv(index=False),
            file_name="data_log.csv",
            mime="text/csv"
        )

show_download_button()
st.write("---")


# ----------------------------
# MAIN LOOP: FETCH + LOG DATA
# ----------------------------
while True:
    try:
        response = requests.get(API_URL)

        if response.status_code == 200:
            data = response.json()

            _id = data.get("id")
            temp = data.get("temperature")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            # 1. Show in UI
            placeholder_id.subheader(f"ID: {_id}")
            placeholder_temp.text(f"Temperature: {temp} °C")

            # 2. Append to CSV
            with open(CSV_FILE, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([_id, temp, timestamp])

        else:
            placeholder_id.text("Error fetching data")

    except Exception as e:
        placeholder_id.text(f"Error: {e}")

    time.sleep(refresh_interval)
