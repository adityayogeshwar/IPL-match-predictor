import streamlit as st
import pickle 
import pandas as pd

teams = ['Chennai Super Kings',
 'Delhi Capitals',
 'Gujarat Titans',
 'Kolkata Knight Riders',
 'Lucknow Super Giants',
 'Mumbai Indians',
 'Punjab Kings',
 'Rajasthan Royals',
 'Royal Challengers Bengaluru',
 'Sunrisers Hyderabad']


city = ['Bangalore', 'Chandigarh', 'Delhi', 'Mumbai', 'Kolkata', 'Jaipur',
       'Hyderabad', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban',
       'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Kochi', 'Indore', 'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi',
       'Abu Dhabi','Rajkot', 'Kanpur', 'Bengaluru', 'Dubai',
       'Sharjah', 'Navi Mumbai', 'Lucknow', 'Guwahati', 'Mohali']

st.title('IPL Win Predictor')
pipe = pickle.load(open('pipe.pkl','rb'))
col1, col2 = st.columns(2)
with col1:
    batting_teams = st.selectbox("Select the batting team",sorted(teams))
with col2:
    bowling_teams = st.selectbox("Select the bowling team",sorted(teams))

selected_city = st.selectbox("Select host city",sorted(city))

target = st.number_input('Target', min_value=0, max_value=300, step=1, format="%d")

col3,col4,col5 = st.columns(3)
with col3:
    score = st.number_input('Score',min_value=0, max_value=300, step=1,format="%d")
with col4:
    overs = st.number_input('Overs Completed',min_value=0, max_value=19, step=1,format="%d")
with col5:
    wicket = st.number_input('Wickets Out',min_value=0, max_value=10, step=1,format="%d")

if st.button('Predict Probability'):
    runs_left = int(target-score)
    balls_left = int(120-(overs*6))
    wickets = int(10-wicket)
    crr = round(score/overs,2)
    rrr = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'batting_team':[batting_teams],'bowling_team':[bowling_teams],'city':[selected_city],'runs_required':[runs_left],'balls_left':[balls_left],'wickets_left':[wickets],'target_runs':[target],'crr':[crr],'rrr':[rrr],'current_score':[score]})
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_teams + "-"+str(round(win*100))+"%")
    st.header(bowling_teams + "-"+str(round(loss*100))+'%')