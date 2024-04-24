import pandas as pd
import plotly.express as px
import streamlit as st

@st.cache  # Cache data loading for faster app performance
def load_data(file_path):
    return pd.read_csv(file_path)

def plot_graphs(df):
    st.subheader("Graphs")

    # Plotting the number of constituencies from each state
    num_cons = df.groupby('STATE')['CONSTITUENCY'].nunique().sort_values(ascending=False).reset_index()
    fig_num_cons = px.bar(num_cons, y='CONSTITUENCY', x='STATE', color='STATE', title='Number of Constituencies from Each State', template='plotly_dark')
    st.plotly_chart(fig_num_cons)

    # Plotting constituency vs statewise participation for the most contesting political parties
    vote_prty = df[df['PARTY'] != 'NOTA']
    prty_cnt = vote_prty.groupby('PARTY')['CONSTITUENCY'].count().reset_index(name='# Constituency')
    prty_st = vote_prty.groupby('PARTY')['STATE'].nunique().reset_index(name='# State')
    prty_top_all = prty_cnt.merge(prty_st, on='PARTY').nlargest(25, '# Constituency')
    fig_prty_participation = px.scatter(prty_top_all, x='# Constituency', y='# State', color='# State', size='# Constituency', hover_data=['PARTY'])
    fig_prty_participation.update_layout(title_text='Constituency vs Statewise Participation for the Most Contested Political Parties', template='plotly_dark')
    st.plotly_chart(fig_prty_participation)

    # Add more graphs here...

def conduct_analysis(df):
    st.subheader("Analysis")
    states = df['STATE'].unique()
    selected_state = st.sidebar.selectbox('Select State:', states)
    df_state = df[df['STATE'] == selected_state]

    constituencies = df_state['CONSTITUENCY'].unique()
    selected_constituency = st.sidebar.selectbox('Select Constituency:', constituencies)
    df_selected = df_state[df_state['CONSTITUENCY'] == selected_constituency]

    st.write(df_selected)
    # Add more analysis here...

# Streamlit UI
st.set_page_config(
    page_title="General Elections Analysis",
    page_icon="📊",
    layout="wide"
)

st.sidebar.header("General Elections In India 2019")
tab_selector = st.sidebar.radio("Select Tab", ("Graph", "Analysis"))

df = load_data("data.csv")

if tab_selector == "Graph":
    plot_graphs(df)
elif tab_selector == "Analysis":
    conduct_analysis(df)
