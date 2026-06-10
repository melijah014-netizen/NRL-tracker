import streamlit as st

# DATABASE OF BASE TEAM STATS
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

def run_advanced_prediction(home_name, away_name, weather, h_injuries, a_injuries, h_turnaround, a_turnaround):
    home = nrl_teams_db[home_name]
    away = nrl_teams_db[away_name]
    
    # Adjust error severity based on weather
    error_weight = 2.5 if weather == "Wet / Rain" else 1.5
    
    # Base Calculation
    h_score = (home["poss"] * 0.4) + (home["comp"] * 0.3) - (home["err"] * error_weight) - (home["pen"] * 2.0) + home["hist_ht"]
    a_score = (away["poss"] * 0.4) + (away["comp"] * 0.3) - (away["err"] * error_weight) - (away["pen"] * 2.0) + away["hist_ht"]
    
    # Apply Injury Penalties (-2.5 points per missing key player)
    h_score -= (h_injuries * 2.5)
    a_score -= (a_injuries * 2.5)
    
    # Apply Turnaround Penalties (Short 5-day turnaround hurts performance)
    if h_turnaround == "Short (5 days)": h_score -= 1.5
    if a_turnaround == "Short (5 days)": a_score -= 1.5
    
    margin = h_score - a_score
    abs_margin = abs(margin)
    
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

# STREAMLIT USER INTERFACE
st.title("🏈 Advanced NRL HT Predictor")
st.write("Customise match variables to generate real-time halftime predictions.")

st.divider()

# 1. Team Selection
team_list = sorted(list(nrl_teams_db.keys()))
col_t1, col_t2 = st.columns(2)
with col_t1:
    home_team = st.selectbox("Home Team:", team_list, index=0)
with col_t2:
    away_team = st.selectbox("Away Team:", team_list, index=1)

st.divider()

# 2. Advanced Game Variables
st.subheader("🛠️ Match Conditions")

weather_cond = st.selectbox("Weather Condition:", ["Dry", "Wet / Rain"])

col_v1, col_v2 = st.columns(2)
with col_v1:
    st.markdown(f"**{home_team} (Home)**")
    h_inj = st.slider("Missing Key Players:", 0, 5, 0, key="h_inj")
    h_turn = st.radio("Turnaround Time:", ["Normal (6+ days)", "Short (5 days)"], key="h_turn")

with col_v2:
    st.markdown(f"**{away_team} (Away)**")
    a_inj = st.slider("Missing Key Players :", 0, 5, 0, key="a_inj")
    a_turn = st.radio("Turnaround Time :", ["Normal (6+ days)", "Short (5 days)"], key="a_turn")

st.divider()

# 3. Output Generation
if home_team == away_team:
    st.warning("Please select two different teams.")
else:
    winner, bracket = run_advanced_prediction(home_team, away_team, weather_cond, h_inj, a_inj, h_turn, a_turn)
    
    st.subheader("📊 Halftime Prediction Result")
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.markdown("**Expected HT Leader:**")
        st.info(f"🏆 {winner}")
    with res_col2:
        st.markdown("**Expected HT Margin:**")
        st.success(f"📏 {bracket}")
