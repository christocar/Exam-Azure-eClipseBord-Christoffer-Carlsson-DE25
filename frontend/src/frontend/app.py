import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("eClipseBord")

response = requests.get(f"{API_URL}/health")
st.write("Backend says:", response.json())