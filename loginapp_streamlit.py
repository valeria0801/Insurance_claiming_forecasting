import streamlit as st
import pandas as pd
import numpy as np
import plotly
from Insurance_claiming_forecasting import insurance
import plotly.express as px
import sqlite3

#DB Management
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')

def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password =?', (username,password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def main():
    """Simple Login App"""

    st.title("Simple Login App")
    menu = ["Home", "Login", "SignUp"]
    choise = st.sidebar.selectbox("Menu",menu)

    if choise == "Home":
        st.subheader("Welcome! this is a web application to demonstrate how to register and enter with a username and password")

    elif choise == "Login":
        st.subheader("Login Section")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type="password")
        # if we place a sidebar it is shown in the left panel if not in the center

        if st.sidebar.button("Login"):
            # if password == '123':
            # create_usertable()
            result = login_user(username,password)
            if result:

                st.success("Logged In as {}".format(username))
                task = st.selectbox("What do you want to do?",["Business Intelligence","Claiming Forecasting"])
                if task == "Business Intelligence":
                    st.subheader("Charts Dashboard")
                else:
                    st.subheader("Predictive Dashboard")
            else:
                st.warning("Incorrect Username")

    elif choise == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("SignUp"):
            create_usertable()
            add_userdata(new_user,new_password)
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")


if __name__ == '__main__':
    main()
