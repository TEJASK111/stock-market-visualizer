import streamlit as st
from menu import menu_with_redirect

# Redirect to visualcode.py if response is no , otherwise show the navigation menu
menu_with_redirect()

st.title("This page is available to user who choose no")
st.markdown("you can close it now")
