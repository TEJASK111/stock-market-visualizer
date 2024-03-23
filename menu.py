import streamlit as st   
import time, datetime
def response():
    st.sidebar.page_link("visualcode.py", label="go back to main")
    st.sidebar.page_link("pages/game.py",label="(simulator) stock market ")
    
        
def noresponse():
    st.sidebar.page_link("visualcode.py", label="choose response")
    
def menu():
    if "resp" not in st.session_state or st.session_state.resp is None:
        noresponse()
        return
    response()
    
    
def menu_with_redirect():
    if "resp" not in st.session_state or st.session_state.resp is None:
        st.switch_page("visualcode.py")
    menu()

#end