

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

tab1, tab2 = st.tabs(["Graph", "Analysis"])
with tab1:
  st.header("General Elections In India 2019")
  df=pd.read_csv("data.csv")
  
  
  
  df = df.rename(columns={"CRIMINAL\nCASES": "Criminal", "GENERAL\nVOTES": "Genral_votes","POSTAL\nVOTES":"Postal_votes","TOTAL\nVOTES":"Total_votes"})
  df
  
  
  
  
  
  party= df['PARTY'].value_counts().reset_index().head(10)
  party.columns= ['PARTY','COUNT']
  ax = px.bar(party,x = 'PARTY', y = 'COUNT', color = 'PARTY',title='The number of seats contest by a party')
  ax
  
  
  
  
  df_winners = df[df['WINNER']==1]
  winner = df_winners['PARTY'].value_counts().reset_index().head(10)
  winner.columns=['PARTY','COUNT']
  ax=px.bar(winner,x='PARTY',y='COUNT',color='PARTY',title='The number of seats wining by party')
  ax
  
  
  
  
  
  num_cons = df.groupby('STATE')['CONSTITUENCY'].nunique().sort_values(ascending = False).reset_index()
  
  ax = px.bar(num_cons,y='CONSTITUENCY',x='STATE',color = 'STATE', title='The Number of Constituencies from each State')
  ax
  
  
  young_winner = df[df['WINNER']==1]
  young_winner = young_winner.sort_values('AGE').head(10)
  ax = px.bar(young_winner,x = 'NAME',y = 'AGE',color = 'NAME',hover_data = ['PARTY','STATE','CONSTITUENCY'], title='Youngest Winners')
  ax
  
  
  
  old_winner = df[df['WINNER']==1]
  old_winner = old_winner.sort_values('AGE',ascending = False).head(10)
  ax = px.bar(old_winner,x = 'NAME',y = 'AGE',color = 'NAME',hover_data = ['PARTY','STATE','CONSTITUENCY'], title = 'Oldest Winners and their Details:')
  ax
  
  
  
  
  df['EDUCATION'] = df['EDUCATION'].replace('Post Graduate\n','Post Graduate')
  df['EDUCATION'] = df['EDUCATION'].replace('Not Available','Others')
  education = df['EDUCATION'].value_counts().reset_index()
  education.columns = ['EDUCATION','COUNT']
  ax = px.bar(education,x = 'EDUCATION', y = 'COUNT',color = 'EDUCATION', title= 'Education Level of the Candidates')
  ax
  
  
  
  winner = df[df['WINNER']==1]
  ax = px.bar(winner,x = 'EDUCATION',y = 'WINNER', color='WINNER',title='Winning Candidates Educational Degree').update_xaxes(categoryorder = "total descending")
  ax
  
  
  
  category = df['CATEGORY'].value_counts().reset_index()
  category.columns= ['CATEGORY','COUNT']
  ax = px.bar(category,x = 'CATEGORY', y = 'COUNT', color = 'CATEGORY')
  ax
  
  
  
  df = df[df['WINNER']==1]
  category = df['CATEGORY'].value_counts().reset_index()
  category.columns= ['CATEGORY','COUNT']
  ax = px.bar(category,x = 'CATEGORY', y = 'COUNT', color = 'CATEGORY', title='Winners from Various Categories')
  ax

with tab2:
 
  df=pd.read_csv("data.csv")
  df = df.rename(columns={"CRIMINAL\nCASES": "Criminal", "GENERAL\nVOTES": "Genral_votes","POSTAL\nVOTES":"Postal_votes","TOTAL\nVOTES":"Total_votes"})
  # df
  a=df.STATE.unique()
  
  
  col1,col2,col3=st.columns(3)
  
  with col1:
    option = st.selectbox(
      'How would you like to be contacted?',
      (a))
  df1=df[(df['STATE'] == option)]
  with col2:
    b=df1.CONSTITUENCY.unique()
    option2 = st.selectbox(
      'How would you ',
      (b))
  
  df2=df1[(df1['STATE'] == option) & (df1['CONSTITUENCY'] == option2)]
  df2
  df3=df1[(df1['STATE'] == option) & (df1['CONSTITUENCY'] == option2) & (df1['WINNER'] == 1)]
  df3

