import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.sidebar.header("General Elections In India 2019")
tab_selector = st.sidebar.radio("Select Tab", ("Graph", "Analysis"))

if tab_selector == "Graph":
    st.subheader("Graph")
    graph_type = st.sidebar.radio("Select Graph Type", ("Bar Chart", "Pie Chart", "Line Chart"))
    df = pd.read_csv("data.csv")
    df = df.rename(columns={"CRIMINAL\nCASES": "Criminal", "GENERAL\nVOTES": "General_votes", "POSTAL\nVOTES": "Postal_votes", "TOTAL\nVOTES": "Total_votes"})
    
    if graph_type == "Bar Chart":
        st.subheader("Bar Chart")
        # Clean up 'ASSETS' column and convert to integer
        df['ASSETS'] = df['ASSETS'].str.replace(',', '')  # Remove commas from numbers
        df['ASSETS'] = df['ASSETS'].str.extract(r'([\d.]+)').astype(float)  # Convert to float

        # Fill missing values with 0
        df['ASSETS'] = df['ASSETS'].fillna(0)

        # Convert to integer
        df['ASSETS'] = df['ASSETS'].astype(int)

        # Remove missing or invalid values from 'ASSETS' column
        df = df[df['ASSETS'].notna()]

        # Group by individual's name and find the maximum assets, party, state, and constituency for each individual
        individual_assets = df.groupby('NAME').agg({'ASSETS': 'max', 'PARTY': 'first', 'STATE': 'first', 'CONSTITUENCY': 'first'}).reset_index()
        individual_assets = individual_assets.sort_values(by='ASSETS', ascending=False).head(10)

        # Sort by count of assets in descending order
        individual_assets = individual_assets.sort_values(by='ASSETS', ascending=False)

        fig = px.bar(individual_assets, x='NAME', y='ASSETS', color='PARTY', title='Top 10 Individuals with the Highest Assets')
        st.plotly_chart(fig)
    
    elif graph_type == "Pie Chart":
        st.subheader("Pie Chart")
        # Your code for pie chart
        # Example:
        fig = px.pie(...)
        st.plotly_chart(fig)
    
    elif graph_type == "Line Chart":
        st.subheader("Line Chart")
        # Your code for line chart
        # Example:
        fig = px.line(...)
        st.plotly_chart(fig)

elif tab_selector == "Analysis":
    st.subheader("Analysis")
    df = pd.read_csv("data.csv")
    df = df.rename(columns={"CRIMINAL\nCASES": "Criminal", "GENERAL\nVOTES": "General_votes", "POSTAL\nVOTES": "Postal_votes", "TOTAL\nVOTES": "Total_votes"})

    a = df.STATE.unique()

    option = st.sidebar.selectbox('Select State ', a)
    df1 = df[(df['STATE'] == option)]

    b = df1.CONSTITUENCY.unique()
    option2 = st.sidebar.selectbox('Select Constituency ', b)

    df2 = df1[(df1['STATE'] == option) & (df1['CONSTITUENCY'] == option2)]
    st.write(df2)
