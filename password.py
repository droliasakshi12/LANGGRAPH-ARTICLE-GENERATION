import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r"password.env")

uname = os.getenv("user")
passw = os.getenv("pass")

# taking user inputs
username1 = st.text_input("Username")
password1 = st.text_input("Password", type='password')

login_button = st.button("LOGIN", use_container_width=True)

if login_button:
    if uname == username1 and password1 == passw:
        st.success("Successfully Logged In!")
        st.session_state['login'] = True
        st.switch_page("pages/access_article.py")

    else:
        st.error("Please enter the correct username and password!")
        st.session_state = False
