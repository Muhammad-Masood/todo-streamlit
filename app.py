import streamlit as st
import requests
from requests.models import Response
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.environ.get("API_BASE_URL") 

st.title("Welcome to My Todo App")
st.subheader("CRUD Operations, User Authentication, and More")

st.write(
    "This Todo app provides CRUD (Create, Read, Update, Delete) operations for managing your todos. "
    "It includes user authentication using JWT (JSON Web Tokens), allowing secure access to your todos. "
    "The app is designed to be easy to use and intuitive for users of all levels of experience. "
    "The app is built using FastAPI and Streamlit. It utillizes Postgres SQL with Sql Alchemy to store and manage your todos. "
    "Explore the features below and start organizing your tasks!"
)

st.header("CRUD Operations")
st.write(
    "Perform the following CRUD operations to manage your todos:"
    "- **Create Todo:** Add a new todo with a title, description, and status."
    "- **Read Todos:** View your existing todos."
    "- **Update Todo:** Modify the title, description, and status of an existing todo."
    "- **Delete Todo:** Remove a todo from your list."
)

st.header("User Authentication")
st.write(
    "To use the full features of the app, log in with your credentials. If you don't have an account, sign up to get started."
)

st.header("Connect with Me")
st.write(
    "Explore the source code, report issues, and contribute on GitHub. Connect with me on LinkedIn."
)

st.markdown("[GitHub Repository](https://github.com/Muhammad-Masood/todo-streamlit)")

st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/muhammad-masood-b9a091248/)")

st.markdown(
    "Feel free to explore and use the app. If you have any feedback or questions, "
    "reach out through GitHub or LinkedIn. Happy task managing!"
)