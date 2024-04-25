import pandas as pd
import plotly.express as px
import streamlit as st

# Read the data
df = pd.read_csv("data.csv")
df = df.rename(columns={"CRIMINAL\nCASES": "Criminal", "GENERAL\nVOTES": "General_votes", "POSTAL\nVOTES": "Postal_votes", "TOTAL\nVOTES": "Total_votes"})

# Filter to include only winning politicians
winners = df[df['WINNER'] == 1]

# Streamlit UI
st.sidebar.header("General Elections In India 2019")
tab_selector = st.sidebar.radio("Select Tab", ("Graph", "Analysis"))

if tab_selector == "Graph":
    st.subheader("Graph")
    # Your graph tab code here
    num_cons = df.groupby('STATE')['CONSTITUENCY'].nunique().sort_values(ascending=False).reset_index()
    fig_num_cons = px.bar(num_cons, y='CONSTITUENCY', x='STATE', color='STATE', title='The Number of Constituencies from each State', template='plotly_dark')

    # Plotting the bar chart for each state
    st.plotly_chart(fig_num_cons)

    # Read the data and preprocess if necessary
    vote = pd.read_csv("data.csv")  # Replace "data.csv" with your actual data file name
    vote_prty = vote[vote['PARTY'] != 'NOTA']
    prty_cnt = vote_prty.groupby('PARTY')['CONSTITUENCY'].count().reset_index(name='# Constituency')
    prty_st = vote_prty.groupby('PARTY')['STATE'].nunique().reset_index(name='# State')
    prty_top_all = prty_cnt.merge(prty_st, on='PARTY').nlargest(25, '# Constituency')
    fig = px.scatter(prty_top_all, x='# Constituency', y='# State', color='# State', size='# Constituency', hover_data=['PARTY'])
    fig.update_layout(title_text='Constituency vs Statewise participation for the most contesting Political Parties', template='plotly_dark')

    # Streamlit UI
    st.plotly_chart(fig)

    # Aggregating data to get the total number of seats won by each party in each state
    seats_won_by_party_in_state = df[df['WINNER'] == 1].groupby(['STATE', 'PARTY']).size().reset_index(name='SEATS_WON')
    fig_seats_won = px.bar(seats_won_by_party_in_state, x='STATE', y='SEATS_WON', color='PARTY', title='Seats Won by Party in Each State', template='plotly_dark')

    st.plotly_chart(fig_seats_won)

    party = df['PARTY'].value_counts().reset_index().head(10)
    party.columns = ['PARTY', 'COUNT']
    fig_party = px.bar(party, x='PARTY', y='COUNT', color='PARTY', title='The number of seats contest by a party', template='plotly_dark')

    st.plotly_chart(fig_party)

    df_winners = df[df['WINNER'] == 1]
    winner = df_winners['PARTY'].value_counts().reset_index().head(10)
    winner.columns = ['PARTY', 'COUNT']
    fig_winner = px.bar(winner, x='PARTY', y='COUNT', color='PARTY', title='The number of seats winning by party', template='plotly_dark')

    st.plotly_chart(fig_winner)

    # Assuming 'vote' DataFrame is already defined
    vote_gndr = vote[vote['PARTY'] != 'NOTA']

    gndr_counts = pd.concat([
        vote_gndr.groupby('GENDER')['NAME'].count().rename('Counts').reset_index(),
        vote_gndr[vote_gndr['WINNER'] == 1].groupby('GENDER')['NAME'].count().rename('Counts').reset_index()
    ], keys=['Overall Gender Ratio', 'Winning Gender Ratio']).reset_index(level=1)

    fig = px.bar(gndr_counts, x='GENDER', y='Counts', color=gndr_counts.index, barmode='group')
    fig.update_layout(title_text='Participation vs Win Counts analysis for the Genders', template='plotly_dark')
    st.plotly_chart(fig)

    young_winner = df[df['WINNER'] == 1].sort_values('AGE').head(10)
    fig_young_winner = px.bar(young_winner, x='NAME', y='AGE', color='PARTY', hover_data=['PARTY', 'STATE', 'CONSTITUENCY'], title='Youngest Winners', template='plotly_dark')

    st.plotly_chart(fig_young_winner)

    old_winner = df[df['WINNER'] == 1].sort_values('AGE', ascending=False).head(10)
    fig_old_winner = px.bar(old_winner, x='NAME', y='AGE', color='PARTY', hover_data=['PARTY', 'STATE', 'CONSTITUENCY'], title='Oldest Winners and their Details:', template='plotly_dark')

    st.plotly_chart(fig_old_winner)

    df_winners = df[df['WINNER'] == 1]  # Filter winners
    winner_education = df_winners['EDUCATION'].value_counts().reset_index()  # Count winners' education levels
    winner_education.columns = ['EDUCATION', 'COUNT']

    # Plot the bar chart for winning candidates' educational degrees
    fig_winner_education = px.bar(winner_education, x='EDUCATION', y='COUNT', color='EDUCATION', title='Winning Candidates Educational Degree', template='plotly_dark')

    st.plotly_chart(fig_winner_education)

elif tab_selector == "Analysis":
    st.subheader("Analysis")
    # Your analysis tab code here
    a = df.STATE.unique()

    option = st.sidebar.selectbox('Select State ', a)
    df1 = df[(df['STATE'] == option)]

    b = df1.CONSTITUENCY.unique()
    option2 = st.sidebar.selectbox('Select Constituency ', b)

    df2 = df1[(df1['STATE'] == option) & (df1['CONSTITUENCY'] == option2)]
    st.write(df2)

    # Add a graph here based on the filtered data
    if not df2.empty:
        # Plot a graph based on the selected state and constituency
        party_votes = df2.groupby('PARTY')['Total_votes'].sum().reset_index()
        fig_party_votes = px.bar(party_votes, x='PARTY', y='Total_votes', color='PARTY', title=f'Total Votes for Each Party in {option2}, {option}', template='plotly_dark')
        st.plotly_chart(fig_party_votes)

    # Display winning candidates for the selected state and constituency
    st.subheader("Winning Candidates")
    winners_filter = winners[(winners['STATE'] == option) & (winners['CONSTITUENCY'] == option2)]
    st.write(winners_filter[['NAME', 'PARTY', 'AGE', 'GENDER']])

    # Age and gender selection
    age_range = st.sidebar.slider("Select Age Range", min_value=20, max_value=100, value=(20, 40), step=1)
    gender = st.sidebar.radio("Select Gender", ["Male", "Female"])

    # Filter winners based on selected age range and gender
    filtered_winners = winners[(winners['AGE'] >= age_range[0]) & (winners['AGE'] <= age_range[1]) & (winners['GENDER'] == gender)]

    # Display the filtered winners
    st.subheader("Filtered Winning Candidates")
    st.write(filtered_winners[['NAME', 'PARTY', 'AGE', 'GENDER']])
