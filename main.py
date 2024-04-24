import pandas as pd
import plotly.express as px
import streamlit as st

# Streamlit UI
st.sidebar.title("General Elections In India 2019")
st.sidebar.subheader("Explore Data")
tab_selector = st.sidebar.radio("Select Tab", ("Graph", "Analysis"))

if tab_selector == "Graph":
    st.subheader("Graph")
    df = pd.read_csv("data.csv")
    df = df.rename(columns={"CRIMINAL\nCASES": "Criminal", "GENERAL\nVOTES": "General_votes", "POSTAL\nVOTES": "Postal_votes", "TOTAL\nVOTES": "Total_votes"})
    
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

    # Convert 'Criminal' column to numeric
    df['Criminal'] = pd.to_numeric(df['Criminal'], errors='coerce')
    df['Criminal'] = df['Criminal'].fillna(0)

    individual_criminal_cases = df.groupby('NAME')['Criminal'].sum().reset_index()
    individual_criminal_cases = individual_criminal_cases.sort_values(by='Criminal', ascending=False).head(10)

    fig_individual_criminal_cases = px.bar(individual_criminal_cases, x='NAME', y='Criminal', color='NAME', title='Top 10 Individuals with the Most Criminal Cases', template='plotly_dark')
    st.plotly_chart(fig_individual_criminal_cases)

    # Clean up 'ASSETS' column and convert to integer
    df['ASSETS'] = df['ASSETS'].str.replace(',', '')  # Remove commas from numbers
    df['ASSETS'] = df['ASSETS'].str.extract(r'([\d.]+)').astype(float)  # Convert to float
    df['ASSETS'] = df['ASSETS'].fillna(0)  # Fill missing values with 0
    df['ASSETS'] = df['ASSETS'].astype(int)  # Convert to integer

    # Remove missing or invalid values from 'ASSETS' column
    df = df[df['ASSETS'].notna()]

    # Group by individual's name and find the maximum assets, party, state, and constituency for each individual
    individual_assets = df.groupby('NAME').agg({'ASSETS': 'max', 'PARTY': 'first', 'STATE': 'first', 'CONSTITUENCY': 'first'}).reset_index()

    # Sort by count of assets in descending order and select top 10
    individual_assets = individual_assets.sort_values(by='ASSETS', ascending=False).head(10)

    # Plot the scatter plot
    fig_individual_assets = px.scatter(individual_assets, x='NAME', y='ASSETS', color='PARTY', hover_data=['PARTY', 'STATE', 'CONSTITUENCY'], title='Top 10 Individuals with the Highest Assets', template='plotly_dark')
    st.plotly_chart(fig_individual_assets)
   

    # Filter and count overall category
    cat_overall = vote[vote['PARTY'] != 'NOTA']['CATEGORY'].value_counts().reset_index()
    cat_overall.columns = ['CATEGORY', 'Counts']
    cat_overall['Category'] = 'Overall Category Counts'

    # Filter and count winning category
    cat_winner = vote[vote['WINNER'] == 1]['CATEGORY'].value_counts().reset_index()
    cat_winner.columns = ['CATEGORY', 'Counts']
    cat_winner['Category'] = 'Winning Category Ratio'

    # Concatenate overall and winning category counts
    cat_overl_win = pd.concat([cat_winner, cat_overall])

    # Plot the bar chart
    fig = px.bar(cat_overl_win, x='CATEGORY', y='Counts', color='Category', barmode='group')
    fig.update_layout(title_text='Participation vs Win Counts for the Category in Politics', template='plotly_dark')
    st.plotly_chart(fig)

    # Filter to include only winning politicians
    winners = df[df['WINNER'] == 1]

    # Define the age ranges or bins for the histogram
    age_bins = [20, 30, 40, 50, 60, 70, 80, 90, 100]

    # Create a histogram of age distribution for winning politicians with color based on gender
    fig = px.histogram(winners, x="AGE", nbins=len(age_bins), color="GENDER", title='Age Distribution of Winning Politicians by Gender', template='plotly_dark')

    # Update the layout
    fig.update_layout(xaxis_title="Age",
                  yaxis_title="Count",
                  title_text='Age Distribution of Winning Politicians by Gender',
                  template='plotly_dark')

    # Show the figure
    st.plotly_chart(fig)

elif tab_selector == "Analysis":
    st.sidebar.subheader("Filter Data")
    df = pd.read_csv("data.csv")
    df = df.rename(columns={"CRIMINAL\nCASES": "Criminal", "GENERAL\nVOTES": "General_votes", "POSTAL\nVOTES": "Postal_votes", "TOTAL\nVOTES": "Total_votes"})

    a = df.STATE.unique()

    option = st.sidebar.selectbox('Select State ', a)
    df1 = df[(df['STATE'] == option)]

    b = df1.CONSTITUENCY.unique()
    option2 = st.sidebar.selectbox('Select Constituency ', b)

    df2 = df1[(df1['STATE'] == option) & (df1['CONSTITUENCY'] == option2)]
    st.write(df2)
