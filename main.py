import streamlit as st
import pandas as pd

# Function to show the main content

from dotenv import load_dotenv
load_dotenv()  # This loads the environment variables from .env file if present

def load_css():
    st.markdown("""
        <style>
            .css-1d391kg { padding: 0; margin: 0; } /* Adjust class name based on inspection */
        </style>
        """, unsafe_allow_html=True)
    
def main_content():
    st.title("🏡Homepage: GPT Tagger and Analyser")
    with st.expander('About this App'):
        st.markdown('**What Can This App Do?**')
        st.info('This app provides comprehensive insights into cybersecurity data, along with an interactive "Chat with Data" feature for in-depth analysis.')
        st.markdown('**How to Use the App?**')
        st.warning('To use this app, follow these steps: 1. Navigate to the "Data Management Page." 2. Choose to explore the original dataset or upload a new dataset. 3. Proceed to any feature you are interested in — the dataset will be updated throughout the app based on your selection.')

# Function to show the welcome page
def welcome_page():
    st.image("image/banner5.png", use_column_width=True)  # Adjust the path if needed
    if st.button('Go to Homepage'):
        main_content()  # Calls the function that contains the main content of the app

st.set_page_config(
    page_title="Welcome",
    page_icon="🏡",
    layout="wide",  # Change layout to wide
    initial_sidebar_state="collapsed"
)

if __name__ == "__main__":
    load_css()
    welcome_page()
