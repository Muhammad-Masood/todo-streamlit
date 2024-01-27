import streamlit as st
import requests
from requests.models import Response
from dotenv import load_dotenv
import os

load_dotenv()

API_BASE_URL = os.environ.get("API_BASE_URL") 

# Function to get user's todos
def get_todos():
    headers={"Authorization": f"Bearer {st.session_state["session"]}"}
    response = requests.get(f"{API_BASE_URL}/todos/get", headers=headers)
    return response.json()

def delete_todo(todo_id: str):
    headers={"Authorization": f"Bearer {st.session_state["session"]}"}
    response = requests.delete(f"{API_BASE_URL}/todo/delete/{todo_id}", headers=headers)
    return response.json()

def update_todo(todo_id: str, title: str, description: str, is_done: bool):
    headers={"Authorization": f"Bearer {st.session_state["session"]}"}
    updated_todo_data = {"title": title, "description": description, "isDone": is_done}
    response = requests.patch(f"{API_BASE_URL}/todo/update/{todo_id}", headers=headers, json=updated_todo_data)
    return response.json()

st.title("Your Todos")
if "isUpdateFormOpen" in st.session_state is None:
    st.session_state["isUpdateFormOpen"] = False

# User's Todos Section
if "session" in st.session_state:
    try:
        user_todos = get_todos()
        if user_todos.get("todos") is None:
            st.write("No todos found")
        else:
            for todo in user_todos.get("todos", []):
                st.write(f"**Title:** {todo['title']}")
                st.write(f"**Description:** {todo['description']}")
                st.write(f"**Is Done:** {todo['isDone']}")

                col1, col2 = st.columns(2)
                if col1.button(f"Delete", key=todo['id']):
                    delete_todo(todo['id'])
                    st.success("Todo deleted successfully!")
                
                if col2.button(f"Update", key=f"update_{todo['id']}") or "isUpdateFormOpen" in st.session_state and st.session_state["isUpdateFormOpen"]:
                    new_title = st.text_input("New Title", value=todo['title'])
                    new_description = st.text_input("New Description", value=todo['description'])
                    new_is_done = st.checkbox("Is Done", value=todo['isDone'])
                    st.session_state["isUpdateFormOpen"] = True

                    if st.button("Update Todo"):
                        try:
                            update_todo(todo['id'], new_title, new_description, new_is_done)
                            st.success("Todo updated successfully!")
                            st.session_state["isUpdateFormOpen"] = False
                        except Exception as e:
                            st.error(str(e))

                st.markdown("---")
    except Exception as e:
        st.error(str(e))
else:
    st.subheader("Please Login First.")