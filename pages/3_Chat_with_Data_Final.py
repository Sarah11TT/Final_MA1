import streamlit as st
import os
import pandas as pd
from pandasai import Agent
from pandasai.llm import OpenAI
import openai

# Setup environment variables
#os.environ["PANDASAI_API_KEY"] = os.getenv("PANDASAI_API_KEY")

#os.environ["PANDASAI_API_KEY"] = os.getenv("PANDASAI_API_KEY", "$2a$10$HB6/RbpWSVdrZADUF8op9eFdcowttwQQIu.rULm0UNST3YMG6SK9a")
#openai_api_key = os.getenv("OPENAI_API_KEY")

# Accessing secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]
pandasai_api_key = st.secrets["PANDASAI_API_KEY"]
os.environ["PANDASAI_API_KEY"]=pandasai_api_key
# Function to chat with CSV data
def chat_with_csv(df, user_query):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("The input data must be a pandas DataFrame.")
    llm = OpenAI()
    agent = Agent(dfs=[df],config={"llm": llm})
    agent_result = agent.chat(user_query)
    return str(agent_result)

def extract_keywords(df):
    # Extract keywords from DataFrame, such as column names or unique values
    keywords = set(df.columns.tolist())  # Start with column names
    for col in df.columns:
        if df[col].dtype == 'object':  # Assuming object type columns contain categorical data
            keywords.update(df[col].astype(str).unique())
    return keywords

# Parse user query for keywords
def extract_query_keywords(query):
    # This is a basic implementation, consider using NLP libraries for better keyword extraction from user queries
    query_words = set(query.lower().split())
    return query_words

# Function to handle general questions
def general_question(user_query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Your assistant is here to help."}, {"role": "user", "content": user_query}],
        api_key=openai_api_key
    )
    return response.choices[0].message['content']

st.set_page_config(layout='wide')
st.image("image/banner5.png", use_column_width=True)
st.title("CSV ChatApp powered by LLMs")

# Load the dataset
if 'uploaded_data' not in st.session_state and 'original_data' not in st.session_state:
    st.error("No data is currently loaded. Please go to the Data Management page to load data.")
    st.stop()

df = st.session_state.get('uploaded_data', st.session_state.get('original_data'))

# Initialize or load messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Define error messages
error_messages = [
    "No code found in the response", "No information available",
    "Unfortunately, I was not able to answer your question", "No result returned",
    "Not found", "An error occurred: ufunc 'add' did not contain a loop with signature matching types (dtype('<U16'), dtype('int64')) -> None",
    "An error occurred: argument of type 'int' is not iterable", "...", "\n"
]

# Chat Interface
st.subheader("Chat Below")
user_query = st.chat_input("Enter your query", key="query_input")

if user_query:
    with st.spinner(f'Processing your query...'):
        try:
            
            query_keywords = extract_query_keywords(user_query)
            if query_keywords:
                response = chat_with_csv(df, user_query)
                model_used = "pandasAI"
                if any(error_message in response for error_message in error_messages):
                    response = general_question(user_query)
                    model_used = "gpt-3.5-turbo"
           
            # Append both the user query and the response to the chat history with model info
            st.session_state.messages.append(f"👤 You: {user_query}")
            st.session_state.messages.append(f"🤖 {model_used}: {response}")
            #st.rerun()  # Rerun the script to clear the chat input
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Display chat history
for idx, message in enumerate(st.session_state.messages):
    st.info(message)
