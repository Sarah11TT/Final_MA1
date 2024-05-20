import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Cyber Attack Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.image("image/banner5.png", use_column_width=True)
st.title("🛡️ Cyber Attack Dashboard")

# Assume df is either uploaded or the original dataset
if 'uploaded_data_filename' in st.session_state:
    filename = st.session_state['uploaded_data_filename']
    st.write(f"You are using uploaded file name: {filename}")
    df = st.session_state['uploaded_data']
else:
    df = st.session_state['original_data']
    st.write("You are using the original dataset")

# Convert 'Date' from string to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')

# Filter form
with st.form("filter-form"):
    #col1, col2 = st.columns(2)

    #with col1:
    st.write("Choose a date range")
    # Use pd.to_datetime for converting to Timestamp for accurate comparison
    start_date = pd.to_datetime(st.date_input("Start Date", value=pd.to_datetime("2023-01-01")))
    end_date = pd.to_datetime(st.date_input("End Date", value=pd.to_datetime("today")))

    #with col2:
    st.write("Choose data sources")
    source_options = df['Source'].unique().tolist()
    selected_sources = st.multiselect("Sources", options=source_options, default=source_options)

    submit_button = st.form_submit_button("Apply Filters")

# Filter the data based on selections
if submit_button:
    # Filtering by date range after converting to datetime
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    if selected_sources:
        filtered_df = filtered_df[filtered_df['Source'].isin(selected_sources)]
else:
    filtered_df = df
    

def display_metrics(df, title, column_container):
    total_incidents = df['Title'].nunique()
    total_attack_types = df['Attack_type'].nunique()
    total_industries = df['Industry'].nunique()

    column_container.markdown(f"### {title}")
    col1, col2, col3 = column_container.columns(3)
    col1.metric("Total Incidents", total_incidents)
    col2.metric("Total Attack Types", total_attack_types)
    col3.metric("Total Industries", total_industries)

# Display metrics for overall data
display_metrics(df, "Overall Data", st)

# Display metrics for filtered data
display_metrics(filtered_df, "Filtered Data", st)



st.subheader("Data Source")
    # Calculate source counts
source_counts = filtered_df.groupby('Source')['Title'].nunique()

    # Convert the Series to a DataFrame for better handling in Plotly and Streamlit
source_counts_df = source_counts.reset_index()
source_counts_df.columns = ['Source', 'Unique Titles']

#Donut Chart for Data Sources
fig1 = px.pie(source_counts_df, values='Unique Titles', names='Source',
                  hole=0.5, title="Distribution of Unique Titles by Source")
fig1.update_traces(textinfo='percent+label', pull=[0.05]*len(source_counts_df))
fig1.update_layout(autosize=True, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig1, use_container_width=True)



# Group data by year and month, and count unique titles for each period
st.subheader("Attacks Over Time")
attacks_over_time = filtered_df.groupby([filtered_df['Date'].dt.year, filtered_df['Date'].dt.month])['Title'].nunique()

# Create a formatted date string for x-axis labels
attacks_over_time.index = [pd.to_datetime(f"{year}-{month}-01").strftime('%b-%Y') for year, month in attacks_over_time.index]


fig2 = px.line(
    attacks_over_time,
    labels={'value': 'Number of Attacks', 'index': 'Month-Year'},
    markers=True  # This adds dots at each data point
)

# Update layout for better interactivity
fig2.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=list(range(len(attacks_over_time))),
        ticktext=attacks_over_time.index
    ),
    hovermode='x unified',  # Enhances tooltip visibility
    showlegend=False
)

# Enable zooming and panning
fig2.update_xaxes(rangeslider_visible=True)

# Display the plot in Streamlit
st.plotly_chart(fig2, use_container_width=True)




#Bar Chart for Attack Types
st.subheader("Attack By Types")
attack_type_counts = filtered_df.groupby('Attack_type')['Title'].nunique()

attack_type_counts_df = attack_type_counts.reset_index()
attack_type_counts_df.columns = ['Attack_type', 'Count']
fig3 = px.pie(attack_type_counts_df, values='Count', names='Attack_type', hole=0.5)
st.plotly_chart(fig3)



#Displaying bar chart for TACTIC
st.subheader("Cyber Attack Tactics")
# Sorting DataFrame by date in descending order
filtered_df_sorted = filtered_df.sort_values(by="Date", ascending=False)
tactic_counts = filtered_df_sorted.groupby('Tactic')['Title'].nunique()
    
tactic_counts_df = tactic_counts.reset_index()
tactic_counts_df.columns = ['Tactic', 'Number of Attacks']

fig4 = px.bar(tactic_counts_df, x='Tactic', y='Number of Attacks')
fig4.update_layout(autosize=True, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig4, use_container_width=True)


#Displaying top 10 industries with number of attacks in the sidebar
st.subheader("Top 10 Industries Affected by Cyber Attacks")
top_10_industries = filtered_df_sorted.groupby('Industry')['Title'].nunique().nlargest(10)
data = pd.DataFrame({'Industry': top_10_industries.index, 'Attacks': top_10_industries.values})
fig5 = px.bar(data, x='Attacks', y='Industry', orientation='h', text='Attacks', 
            color='Attacks', 
            color_discrete_sequence=px.colors.qualitative.Set1)
fig5.update_traces(opacity=0.7, textposition='outside')
fig5.update_layout(xaxis_title='Number of Attacks',
                yaxis_categoryorder='total ascending',
                height=500)
st.plotly_chart(fig5, use_container_width=True)




#Display data table
st.subheader("Filtered Data")
with st.expander("See full data table"):
    st.dataframe(filtered_df.style.format({'Date': lambda x: x.strftime('%Y-%m-%d')}))


