

import streamlit as st

# 1. DATABASE OF CURRENT NRL TEAM STATS
# Contains real-world performance averages for automatic calculations
nrl_teams_db = {
    "Brisbane Broncos": {"poss": 51, "comp": 78, "err": 10, "pen": 6, "hist_ht": 2.1},
    "Canberra Raiders": {"poss": 49, "comp": 76, "err": 11, "pen": 7, "hist_ht": -0.5},
    "Canterbury Bulldogs": {"poss": 50, "comp": 81, "err": 9, "pen": 5, "hist_ht": 1.2},
    "Cronulla Sharks": {"poss": 52, "comp": 79, "err": 10, "pen": 6, "hist_ht": 3.4},
    "Dolphins": {"poss": 48, "comp": 77, "err": 11, "pen": 6, "hist_ht": 0.8},
    "Gold Coast Titans": {"poss": 47, "comp": 75, "err": 12, "pen": 8, "hist_ht": -2.1},
    "Manly Sea Eagles": {"poss": 50, "comp": 78, "err": 10, "pen": 6, "hist_ht": 1.5},
    "Melbourne Storm": {"poss": 53, "comp": 82, "err": 8, "pen": 5, "hist_ht": 4.8},
    "Newcastle Knights": {"poss": 49, "comp": 77, "err": 11, "pen": 7, "hist_ht": -0.2},
    "NZ Warriors": {"poss": 51, "comp": 80, "err": 9, "pen": 6, "hist_ht": 0.5},
    "Nth Qld Cowboys": {"poss": 49, "comp": 76, "err": 11, "pen": 7, "hist_ht": -0.8},
    "Parramatta Eels": {"poss": 48, "comp": 74, "err": 12, "pen": 8, "hist_ht": -3.0},
    "Penrith Panthers": {"poss": 54, "comp": 83, "err": 8, "pen": 5, "hist_ht": 5.5},
    "South Syd Rabbitohs": {"poss": 50, "comp": 77, "err": 11, "pen": 6, "hist_ht": -1.1},
    "St George Dragons": {"poss": 47, "comp": 76, "err": 11, "pen": 7, "hist_ht": -1.8},
    "Sydney Roosters": {"poss": 52, "comp": 79, "err": 10, "pen": 6, "hist_ht": 2.9},
    "Wests Tigers": {"poss": 46, "comp": 73, "err": 13, "pen": 9, "hist_ht": -4.2}
}

def run_match_prediction(home_name, away_name):
    # Pull data from database automatically
    home = nrl_teams_db[home_name]
    away = nrl_teams_db[away_name]
    
    # Calculate score using formula
    h_score = (home["poss"] * 0.4) + (home["comp"] * 0.3) - (home["err"] * 1.5) - (home["pen"] * 2.0) + home["hist_ht"]
    a_score = (away["poss"] * 0.4) + (away["comp"] * 0.3) - (away["err"] * 1.5) - (away["pen"] * 2.0) + away["hist_ht"]
    
    margin = h_score - a_score
    abs_margin = abs(margin)
    
    # Format the bracket output (1-8 or 9+)
    if margin > 1.5:
        winner = home_name
        bracket = "1-8 points" if abs_margin <= 8 else "9+ points"
    elif margin < -1.5:
        winner = away_name
        bracket = "1-8 points" if abs_margin <= 8 else "9+ points"
    else:
        winner = "Draw / Even Match"
        bracket = "1-4 points"
        
    return winner, bracket

# 2. STREAMLIT APP VISUAL INTERFACE
st.title("🏈 Instant NRL HT Match Predictor")
st.write("Pick any two teams. The app calculates the rest instantly.")

st.divider()

# Dropdown selectors for the user
team_list = sorted(list(nrl_teams_db.keys()))
home_team = st.selectbox("Select Home Team:", team_list, index=0)
away_team = st.selectbox("Select Away Team:", team_list, index=1)

st.divider()

# Generate calculation automatically when teams change
if home_team == away_team:
    st.warning("Please select two different teams to play each other.")
else:
    winner, bracket = run_match_prediction(home_team, away_team)
    
    st.subheader("📊 Halftime Prediction Result")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Expected HT Leader:**")
        st.info(f"🏆 {winner}")
    with col2:
        st.markdown("**Expected HT Margin:**")
        st.success(f"📏 {bracket}")
