import streamlit as st
import requests
from requests.models import Response
from dotenv import load_dotenv
import os

load_dotenv()

API_BASE_URL = os.environ.get("API_BASE_URL") 


# st.set_page_config(
#     page_title="LogIn",
#     page_icon=":rocket:",
# )

# Function to handle user login
def login(email, password):
    user_data = {"email": email, "password": password}
    response = requests.post(f"{API_BASE_URL}/user/login", json=user_data)
    return response.json()

st.title("Login")

login_email = st.text_input("Email", key="login_email")
login_password = st.text_input("Password", type="password", key="login_password")
if st.button("Login"):
    try:
        login_result = login(login_email, login_password)
        st.session_state["session"] = login_result.get("session", "")
        st.success(login_result.get("message", ""))
    except Exception as e:
        st.error(str(e))