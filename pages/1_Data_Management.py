import streamlit as st
import pandas as pd
import os


st.set_page_config(
    page_title="Data Management",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Correct path to access the image from the 'pages' folder
st.image("image/banner5.png", use_column_width=True)


st.title("🗂️ Data Management Page")

radio = st.radio("Select Dataset", ["Original Dataset", "Upload New Dataset"])

# The data selection won't be processed until the user confirms their choice.
if radio == "Upload New Dataset":
    uploaded_file = st.file_uploader("Upload New Dataset", type=["csv"])
else:
    uploaded_file = None

# Button to confirm the action
if st.button('Confirm Selection'):
    if radio == "Original Dataset":
        # Define the path to the dataset
        dataset_path = "dataset/final_dataset.csv"
        # Check if the file exists
        if os.path.isfile(dataset_path):
            try:
                df = pd.read_csv(dataset_path, encoding='latin1')
                st.session_state['original_data_filename'] = "final_dataset.csv"  # Save the filename
                st.session_state['original_data'] = df  # Save the dataframe
                st.write(df.head())
                st.success("Original dataset loaded successfully.")
            except Exception as e:
                st.error(f"An error occurred while reading the file: {e}")
        else:
            st.error(f"File not found: {dataset_path}")

    elif radio == "Upload New Dataset" and uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, encoding='latin1')
            st.session_state['uploaded_data'] = df  # Save the dataframe
            st.session_state['uploaded_data_filename'] = uploaded_file.name  # Save the file name
            st.write(df.head())
            st.success(f"New dataset uploaded successfully with {df.shape[0]} rows and {df.shape[1]} columns.")
        except Exception as e:
            st.error(f"Error reading file: {e}")

    elif radio == "Upload New Dataset" and uploaded_file is None:
        st.error("Please upload a dataset before confirming.")
