import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.sidebar.header("General Elections In India 2019")
tab_selector = st.sidebar.radio("Select Tab", ("Graph", "Analysis"))

if tab_selector == "Graph":
    st.subheader("Graph")
    df = pd.read_csv("data.csv")
    df = df.rename(columns={"CRIMINAL\nCASES": "Criminal", "GENERAL\nVOTES": "General_votes", "POSTAL\nVOTES": "Postal_votes", "TOTAL\nVOTES": "Total_votes"})
    
    # Convert 'Criminal' column to numeric
    df['Criminal'] = pd.to_numeric(df['Criminal'], errors='coerce')
    df['Criminal'] = df['Criminal'].fillna(0)

    party_criminal_cases = df.groupby('PARTY')['Criminal'].sum().reset_index()
    party_criminal_cases = party_criminal_cases.sort_values(by='Criminal', ascending=False).head(10)

    fig = px.bar(party_criminal_cases, x='PARTY', y='Criminal', color='PARTY', title='Top 10 Parties with the Most Criminal Cases')
    st.plotly_chart(fig)

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

    fig = px.bar(individual_assets, x='NAME', y='ASSETS', color='PARTY', hover_data=['PARTY', 'STATE', 'CONSTITUENCY'], title='Top 10 Individuals with the Highest Assets')
    st.plotly_chart(fig)

    party = df['PARTY'].value_counts().reset_index().head(10)
    party.columns = ['PARTY', 'COUNT']
    fig = px.bar(party, x='PARTY', y='COUNT', color='PARTY', title='The number of seats contest by a party')
    st.plotly_chart(fig)

    df_winners = df[df['WINNER'] == 1]
    winner = df_winners['PARTY'].value_counts().reset_index().head(10)
    winner.columns = ['PARTY', 'COUNT']
    fig = px.bar(winner, x='PARTY', y='COUNT', color='PARTY', title='The number of seats winning by party')
    st.plotly_chart(fig)

    num_cons = df.groupby('STATE')['CONSTITUENCY'].nunique().sort_values(ascending=False).reset_index()
    fig = px.bar(num_cons, y='CONSTITUENCY', x='STATE', color='STATE', title='The Number of Constituencies from each State')
    st.plotly_chart(fig)

    young_winner = df[df['WINNER'] == 1].sort_values('AGE').head(10)
    fig = px.bar(young_winner, x='NAME', y='AGE', color='PARTY', hover_data=['PARTY', 'STATE', 'CONSTITUENCY'], title='Youngest Winners')
    st.plotly_chart(fig)

    old_winner = df[df['WINNER'] == 1].sort_values('AGE', ascending=False).head(10)
    fig = px.bar(old_winner, x='NAME', y='AGE', color='PARTY', hover_data=['PARTY', 'STATE', 'CONSTITUENCY'], title='Oldest Winners and their Details:')
    st.plotly_chart(fig)

    df['EDUCATION'] = df['EDUCATION'].replace('Post Graduate\n', 'Post Graduate')
    df['EDUCATION'] = df['EDUCATION'].replace('Not Available', 'Others')
    education = df['EDUCATION'].value_counts().reset_index()
    education.columns = ['EDUCATION', 'COUNT']
    fig = px.bar(education, x='EDUCATION', y='COUNT', color='EDUCATION', title='Education Level of the Candidates')
    st.plotly_chart(fig)

    winner = df[df['WINNER'] == 1]
    print(winner['PARTY'].unique())  # Add this line to check the unique values in the 'PARTY' column
    fig = px.bar(winner, x='EDUCATION', y='WINNER', color='PARTY', title='Winning Candidates Educational Degree')
    st.plotly_chart(fig)


    category = df['CATEGORY'].value_counts().reset_index()
    category.columns = ['CATEGORY', 'COUNT']
    fig = px.bar(category, x='CATEGORY', y='COUNT', color='CATEGORY', title='Contest from Various Categories')
    st.plotly_chart(fig)

    df = df[df['WINNER'] == 1]
    category = df['CATEGORY'].value_counts().reset_index()
    category.columns = ['CATEGORY', 'COUNT']
    fig = px.bar(category, x='CATEGORY', y='COUNT', color='CATEGORY', title='Winners from Various Categories')
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
