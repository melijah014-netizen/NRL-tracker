
import streamlit as st

# Configure the page style
st.set_page_config(page_title="HT Edge - NRL Tracker", page_icon="🏉", layout="wide")

# App Header
st.title("🏉 HT Edge - NRL Halftime Tracker")
st.markdown("### Interactive Predictor Dashboard")
st.info("Adjust the match parameters below to view dynamic halftime predictions.")

# Comprehensive List of NRL Teams
nrl_teams = [
    "Brisbane Broncos", "Canberra Raiders", "Canterbury-Bankstown Bulldogs", 
    "Cronulla-Sutherland Sharks", "Dolphins", "Gold Coast Titans", 
    "Manly Warringah Sea Eagles", "Melbourne Storm", "Newcastle Knights", 
    "New Zealand Warriors", "North Queensland Cowboys", "Parramatta Eels", 
    "Penrith Panthers", "South Sydney Rabbitohs", "St. George Illawarra Dragons", 
    "Sydney Roosters", "Wests Tigers"
]

# --- MATCH SELECTOR AREA ---
st.markdown("---")
st.subheader("🗓️ Select Round & Teams")

# Grid layout for selection inputs
sel_col1, sel_col2, sel_col3 = st.columns(3)

with sel_col1:
    round_list = [f"Round {i}" for i in range(1, 28)]
    selected_round = st.selectbox("NRL Round", round_list, index=0)

with sel_col2:
    home_team = st.selectbox("Home Team", nrl_teams, index=7) # Defaults to Storm

with sel_col3:
    away_teams_filtered = [team for team in nrl_teams if team != home_team]
    away_team = st.selectbox("Away Team", away_teams_filtered, index=0) # Defaults to Broncos

# --- LIVE PREDICTION CALCULATOR ENGINE (MOCK LOGIC) ---
st.sidebar.header("⚙️ Match Variables")
weather = st.sidebar.selectbox("Weather Condition", ["Fine", "Rain", "Windy", "Humid"])
travel_fatigue = st.sidebar.radio("Away Team Travel Distance", ["Local / Short Travel", "Interstate", "International (NZ)"])
missing_halfback = st.sidebar.checkbox("Is a starting halfback missing/injured?", value=False)

# Adjust confidence score based on sidebar toggles
confidence = 85
prediction_winner = home_team

if missing_halfback:
    confidence -= 10
if travel_fatigue == "International (NZ)":
    confidence += 4

# --- LAYOUT TABS DISPLAY ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📈 Match Analysis", "🏅 Team Statistics", "📝 Bet Tracker"])

with tab1:
    st.markdown(f"#### Live Display for **{selected_round}**")
    
    col1, col2 = st.columns()
    with col1:
        st.write(f"### ⚡ {home_team} vs {away_team}")
        st.caption(f"Market Status: Ready | Weather: {weather} | Away Travel: {travel_fatigue}")
    with col2:
        st.metric(label="Predicted Winner", value=f"{prediction_winner} HT 9+")
        st.progress(confidence / 100, text=f"Confidence Score: {confidence}%")
        
    st.divider()

with tab2:
    st.subheader(f"Halftime Probability Matrix: {home_team} vs {away_team}")
    
    val1, val2, val3, val4 = (31, 47, 15, 7) if not missing_halfback else (21, 27, 35, 17)
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric(f"{home_team} HT 1-8", f"{val1}%")
    col_m2.metric(f"{home_team} HT 9+", f"{val2}%")
    col_m3.metric(f"{away_team} HT 1-8", f"{val3}%")
    col_m4.metric(f"{away_team} HT 9+", f"{val4}%")
    
    st.markdown("#### Key Drivers for Prediction:")
    st.success(f"✔️ Strong historical home record at venue for {home_team}.")
    if missing_halfback:
        st.error("❌ Warning: Lineup shifts due to the missing halfback have decreased overall prediction confidence.")
    else:
        st.warning(f"⚠️ {away_team} faces adjustment vectors based on: {travel_fatigue}.")

with tab3:
    st.subheader("Team First-Half Database Statistics")
    selected_stat_team = st.selectbox("View Stats for Team:", [home_team, away_team])
    
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.write("#### First Half Attack")
        st.write("- **Avg 1H Points Scored:** 14.5")
        st.write("- **Avg 1H Line Breaks:** 3.2")
        st.write("- **Avg 1H Completion %:** 81.5%")
    with sub_col2:
        st.write("#### First Half Defence")
        st.write("- **Avg 1H Points Conceded:** 6.2")
        st.write("- **Avg 1H Missed Tackles:** 8.4")
        st.write("- **Avg 1H Errors:** 4.1")

with tab4:
    st.subheader("Bet Tracker & ROI Dashboard")
    st.caption("Log your selections based on the generated predictions.")
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Total Bets Placed", "0")
    metric_col2.metric("Current Strike Rate", "0.0%")
    metric_col3.metric("Profit / Loss (Units)", "0.00")
