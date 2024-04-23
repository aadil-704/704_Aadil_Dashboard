import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.header("General Elections In India 2019")
tab1, tab2 = st.columns(2)

with tab1:
    st.subheader("Graph")

    df = pd.read_csv("data.csv")

    df = df.rename(columns={"CRIMINAL\nCASES": "Criminal", "GENERAL\nVOTES": "General_votes", "POSTAL\nVOTES": "Postal_votes", "TOTAL\nVOTES": "Total_votes"})

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
    fig = px.bar(young_winner, x='NAME', y='AGE', color='NAME', hover_data=['PARTY', 'STATE', 'CONSTITUENCY'], title='Youngest Winners')
    st.plotly_chart(fig)

    old_winner = df[df['WINNER'] == 1].sort_values('AGE', ascending=False).head(10)
    fig = px.bar(old_winner, x='NAME', y='AGE', color='NAME', hover_data=['PARTY', 'STATE', 'CONSTITUENCY'], title='Oldest Winners and their Details:')
    st.plotly_chart(fig)

    df['EDUCATION'] = df['EDUCATION'].replace('Post Graduate\n', 'Post Graduate')
    df['EDUCATION'] = df['EDUCATION'].replace('Not Available', 'Others')
    education = df['EDUCATION'].value_counts().reset_index()
    education.columns = ['EDUCATION', 'COUNT']
    fig = px.bar(education, x='EDUCATION', y='COUNT', color='EDUCATION', title='Education Level of the Candidates')
    st.plotly_chart(fig)

    winner = df[df['WINNER'] == 1]
    fig = px.bar(winner, x='EDUCATION', y='WINNER', color='WINNER', title='Winning Candidates Educational Degree').update_xaxes(categoryorder="total descending")
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

with tab2:
    st.subheader("Analysis")

    df = pd.read_csv("data.csv")
    df = df.rename(columns={"CRIMINAL\nCASES": "Criminal", "GENERAL\nVOTES": "General_votes", "POSTAL\nVOTES": "Postal_votes", "TOTAL\nVOTES": "Total_votes"})

    a = df.STATE.unique()

    col1, col2, col3 = st.columns(3)

    with col1:
        option = st.selectbox(
            'Select State ',
            (a))
    df1 = df[(df['STATE'] == option)]
    with col2:
        b = df1.CONSTITUENCY.unique()
        option2 = st.selectbox(
            'Select Constituency ',
            (b))

    df2 = df1[(df1['STATE'] == option) & (df1['CONSTITUENCY'] == option2)]
    st.write(df2)
