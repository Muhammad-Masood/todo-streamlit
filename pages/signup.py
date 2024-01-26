import streamlit as st
import requests
from requests.models import Response
from App import API_BASE_URL

# st.set_page_config(
#     page_title="Sign Up",
#     page_icon=":rocket:",
# )

def signup(email: str, password: str):
    user_data = {"email": email, "password": password}
    response: Response = requests.post(f"{API_BASE_URL}/user/signup", json=user_data)
    return response.json()

st.title("Sign Up")

signup_email: str = st.text_input("Email" , key="signup_email")
signup_password: str = st.text_input("Password", type="password", key="signup_password")
if st.button("Sign Up"):
    try:
        signup_response = signup(signup_email, signup_password)
        st.success(signup_response.get("message", ""))
    except Exception as e:
        st.error(str(e))