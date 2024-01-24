import streamlit as st
import requests
from requests.models import Response
import os
from dotenv import load_dotenv

load_dotenv()

st.title("My Todo App")

API_BASE_URL = os.environ.get("API_BASE_URL") 

def signup(email: str, password: str):
    user_data = {"email": email, "password": password}
    response: Response = requests.post(f"{API_BASE_URL}/user/signup", json=user_data)
    return response.json()

# Function to handle user login
def login(email, password):
    user_data = {"email": email, "password": password}
    response = requests.get(f"{API_BASE_URL}/user/login", json=user_data)
    return response.json()

# Function to create a new todo
def create_todo(title, description, is_done, user_id):
    todo_data = {"title": title, "description": description, "isDone": is_done, "user_id": user_id}
    response = requests.post(f"{API_BASE_URL}/todo/create", json=todo_data)
    return response.json()

# Function to get user's todos
def get_todos(user_id):
    response = requests.get(f"{API_BASE_URL}/todo", headers={"Authorization": f"Bearer {user_id}"})
    return response.json()

# Function to update a todo
def update_todo(todo_id, title, description, is_done):
    todo_data = {"title": title, "description": description, "isDone": is_done}
    response = requests.patch(f"{API_BASE_URL}/todo/update/{todo_id}", json=todo_data)
    return response.json()

# Function to delete a todo
def delete_todo(todo_id):
    response = requests.delete(f"{API_BASE_URL}/todo/delete/{todo_id}")
    return response.json()

# Streamlit Page for User Authentication
st.sidebar.title("User Authentication")

# User Signup Section
st.sidebar.subheader("Sign Up")
signup_email: str = st.sidebar.text_input("Email")
signup_password: str = st.sidebar.text_input("Password", type="password")
if st.sidebar.button("Sign Up"):
    try:
        signup_response = signup(signup_email, signup_password)
        print(signup_response)
        st.toast(signup_response.get("message", ""))
    except Exception as e:
        st.toast(str(e))

# # User Login Section
# st.sidebar.subheader("Login")
# login_email = st.sidebar.text_input("Email")
# login_password = st.sidebar.text_input("Password", type="password")
# if st.sidebar.button("Login"):
#     login_result = login(login_email, login_password)
#     user_id = login_result.get("access_token", "")
#     st.sidebar.text(login_result.get("message", ""))

# Streamlit Page for Todo Operations
# if user_id:
#     st.subheader("Todo Operations")

#     # Create Todo Section
#     st.subheader("Create Todo")
#     todo_title = st.text_input("Title")
#     todo_description = st.text_input("Description")
#     todo_is_done = st.checkbox("Is Done")
#     if st.button("Create Todo"):
#         create_result = create_todo(todo_title, todo_description, todo_is_done, user_id)
#         st.text(create_result.get("message", ""))

#     # Get User's Todos Section
#     st.subheader("Your Todos")
#     user_todos = get_todos(user_id)
#     for todo in user_todos.get("todos", []):
#         st.write(f"Title: {todo['title']}, Description: {todo['description']}, Is Done: {todo['isDone']}")

#     # Update Todo Section
#     st.subheader("Update Todo")
#     update_todo_id = st.text_input("Todo ID")
#     update_todo_title = st.text_input("New Title")
#     update_todo_description = st.text_input("New Description")
#     update_todo_is_done = st.checkbox("Is Done")
#     if st.button("Update Todo"):
#         update_result = update_todo(update_todo_id, update_todo_title, update_todo_description, update_todo_is_done)
#         st.text(update_result.get("message", ""))

#     # Delete Todo Section
#     st.subheader("Delete Todo")
#     delete_todo_id = st.text_input("Todo ID")
#     if st.button("Delete Todo"):
#         delete_result = delete_todo(delete_todo_id)
#         st.text(delete_result.get("message", ""))
