import streamlit as st
import requests
from requests.models import Response
from App import API_BASE_URL


def create_todo(title, description, is_done):
    headers={"Authorization": f"Bearer {st.session_state["session"]}"}
    todo_data = {"title": title, "description": description, "isDone": is_done}
    response = requests.post(f"{API_BASE_URL}/todo/create", json=todo_data, headers=headers)
    return response.json()


st.title("Create Todo")

if "session" in st.session_state:
    todo_title: str = st.text_input("Title")
    todo_description:str = st.text_input("Description")
    todo_is_done:bool = st.checkbox("Is Done")
    if st.button("Create Todo"):
        try:
            create_result = create_todo(todo_title, todo_description, todo_is_done)
            st.text(create_result.get("message", ""))
        except Exception as e:
            st.error(str(e))
else:
    st.subheader("Please Login First.")