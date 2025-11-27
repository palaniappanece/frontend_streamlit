# streamlit_receiver.py
import streamlit as st
import requests
import time
import csv
import os

st.title("Temperature Monitor with CSV Logging")

API_URL = "https://backend-streamlit-pyxs.onrender.com/data"
refresh_interval = 2  # seconds

placeholder_id = st.empty()
placeholder_temp = st.empty()

CSV_FILE = "data_log.csv"

# ----------------------------
# CREATE CSV IF NOT EXIST
# ----------------------------
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Temperature", "Timestamp"])


# ----------------------------
#  LOOP TO READ AND APPEND DATA
# ----------------------------
while True:
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()

            _id = data.get("id")
            temp = data.get("temperature")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            # Show in UI
            placeholder_id.subheader(f"ID: {_id}")
            placeholder_temp.text(f"Temperature: {temp} °C")

            # Append into CSV
            with open(CSV_FILE, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([_id, temp, timestamp])

        else:
            placeholder_id.text("Error fetching data")

    except Exception as e:
        placeholder_id.text(f"Error: {e}")

    time.sleep(refresh_interval)
