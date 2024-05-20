import os
import streamlit as st
import constant
import pandas as pd
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI

os.environ["OPENAI_API_KEY"] = constant.APIKEY

def run_langchain_page():
    st.set_page_config(layout='wide')
    st.title("Langchain Chat Page")

    # Initialize chat history in session state if it does not exist
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Determine which dataset is available and not empty
    uploaded_data = st.session_state.get('uploaded_data')
    original_data = st.session_state.get('original_data')
    active_data = None

    if uploaded_data is not None and not uploaded_data.empty:
        active_data = uploaded_data
    elif original_data is not None and not original_data.empty:
        active_data = original_data

    if active_data is not None:
        try:
            # Preprocess the DataFrame to handle date formats
            df = active_data
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            st.session_state.active_data = df

            # Save the DataFrame to a CSV file temporarily
            temp_csv_path = "temp_loaded_data.csv"
            st.session_state.active_data.to_csv(temp_csv_path, index=False)
            
            # Load CSV through the path
            loader = CSVLoader(temp_csv_path)
            index = VectorstoreIndexCreator().from_loaders([loader])

            # Chat Interface after successful loading of data
            st.subheader("Chat Below")
            user_query = st.chat_input("Enter your query", key="query_input")

            if user_query:
                response = index.query(user_query)
                st.session_state.history.append(f"👤 You: {user_query}")
                st.session_state.history.append(f"🤖 Assistant: {response}")
                #st.rerun()

            # Display chat history
            if 'history' in st.session_state:
                for chat_entry in st.session_state.history:
                    st.info(chat_entry)

        except Exception as e:
            st.error(f"Error loading data or creating index: {str(e)}")
            import traceback
            st.text(traceback.format_exc())
            st.stop()
    else:
        st.write("No data available. Please upload or select data on the Data Management page.")

run_langchain_page()
