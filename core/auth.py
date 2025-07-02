# core/auth.py

import streamlit as st
from typing import Optional
import hashlib
import os
import json

USER_DB_PATH = "users.json"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

class AuthManager:
    """
    Basic file-based authentication system for development use.
    Replace with Firebase/Auth0/Supabase in production.
    """

    def __init__(self, db_path: str = USER_DB_PATH):
        self.db_path = db_path
        if not os.path.exists(db_path):
            with open(db_path, 'w') as f:
                json.dump({}, f)

    def load_users(self) -> dict:
        with open(self.db_path, 'r') as f:
            return json.load(f)

    def save_users(self, users: dict) -> None:
        with open(self.db_path, 'w') as f:
            json.dump(users, f)

    def register(self, email: str, password: str) -> bool:
        users = self.load_users()
        if email in users:
            return False  # already registered
        users[email] = hash_password(password)
        self.save_users(users)
        return True

    def authenticate(self, email: str, password: str) -> bool:
        users = self.load_users()
        return users.get(email) == hash_password(password)

    def login_ui(self) -> Optional[str]:
        st.subheader("🔐 Login or Register")
        mode = st.radio("Mode", ["Login", "Register"])
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.button("Submit")

        if submitted:
            if mode == "Login" and self.authenticate(email, password):
                st.success("Logged in successfully.")
                return email
            elif mode == "Register" and self.register(email, password):
                st.success("Registered successfully. Please login.")
            else:
                st.error("Invalid credentials or user already exists.")
        return None
