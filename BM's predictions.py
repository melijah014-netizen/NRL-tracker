import streamlit as st

# Page setup
st.set_page_config(page_title="BM's Halftime Predictions", page_icon="🏉", layout="wide")

# App Header updated exactly to your request
st.title("🏉 BM's Halftime Predictions")

# Navigation tabs matching your design
tab1, tab2, tab3 = st.tabs(["📊 Live Match Engine", "📁 Bet Archive Ledger", "🌐 Web Settings"])

# Full official list of 17 NRL teams
nrl_teams = [
    "Brisbane Broncos", "Canberra Raiders", "Canterbury-Bankstown Bulldogs", 
    "Cronulla-Sutherland Sharks", "Dolphins", "Gold Coast Titans", 
    "Manly Warringah Sea Eagles", "Melbourne Storm", "Newcastle Knights", 
    "New Zealand Warriors", "North Queensland Cowboys", "Parramatta Eels", 
    "Penrith Panthers", "South Sydney Rabbitohs", "St. George Illawarra Dragons", 
    "Sydney Roosters", "Wests Tigers"
]

with tab1:
    st.header("Match Calculator")
    
    # Selectors for Round, Home Team, and Away Team
    st.markdown("### 🗓️ Select Your Match Parameters")
    col_r, col_h, col_a = st.columns(3)
    
    with col_r:
        round_list = [f"Round {i}" for i in range(1, 28)]
        selected_round = st.selectbox("Select NRL Round", round_list)
        
    with col_h:
        home_team = st.selectbox("Select Home Team", nrl_teams, index=2) # Defaults to Bulldogs
        
    with col_a:
        away_teams_filtered = [team for team in nrl_teams if team != home_team]
        away_team = st.selectbox("Select Away Team", away_teams_filtered, index=10) # Defaults to Eels

    st.divider()
    st.subheader(f"⚙️ Match Setup: {home_team} vs {away_team} ({selected_round})")

    # Home Team Configuration
    st.write(f"#### {home_team} Parameters")
    home_comp = st.number_input(f"{home_team} Completion Rate %", min_value=0, max_value=100, value=82)
    home_spine = st.selectbox(f"{home_team} Spine Intact?", ["Yes", "No"])
    
    st.divider()
    
    # Away Team Configuration
    st.write(f"#### {away_team} Parameters")
    away_comp = st.number_input(f"{away_team} Completion Rate %", min_value=0, max_value=100, value=80)
    away_spine = st.selectbox(f"{away_team} Spine Intact?", ["Yes", "No"])
    
    st.divider()
    
    # Tactical Checkboxes from your layout
    turnaround = st.checkbox("Is a team backed up on a short 5-day turnaround?")
    travel_dist = st.checkbox("Did a Sydney team travel long-distance (QLD/NZ)?")
    
    weather = st.selectbox("Weather Track Condition", ["Dry / Fast", "Wet / Slow", "Windy", "Humid"])
    
    # Dynamic Advantage Message Engine
    st.markdown("### 🎯 Calculation Output")
    if home_comp > away_comp and home_spine == "Yes" and away_spine == "No":
        st.success(f"🔥 STRONG ADVANTAGE: {home_team} at Halftime")
    elif away_comp > home_comp and away_spine == "Yes" and home_spine == "No":
        st.success(f"🔥 STRONG ADVANTAGE: {away_team} at Halftime")
    else:
        st.warning("⚠️ NO CLEAR ADVANTAGE")

with tab2:
    st.header("Bet Archive Ledger")
    st.info("Your historical halftime betting tracking ledger will compile here.")

with tab3:
    st.header("Web Settings")
    st.write("System and database configurations.")

