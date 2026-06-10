import streamlit as st

def run_fully_manual_prediction(h_name, a_name, h_poss, a_poss, h_comp, a_comp, h_err, a_err, h_pen, a_pen, weather, h_injuries, a_injuries, h_turnaround, a_turnaround):
    # Adjust error severity based on weather selection
    error_weight = 2.5 if weather == "Wet / Rain" else 1.5
    
    # Mathematical Formula Processing Manual Inputs
    h_score = (h_poss * 0.4) + (h_comp * 0.3) - (h_err * error_weight) - (h_pen * 2.0)
    a_score = (a_poss * 0.4) + (a_comp * 0.3) - (a_err * error_weight) - (a_pen * 2.0)
    
    # Apply Injury Penalties (-2.5 points per missing key player)
    h_score -= (h_injuries * 2.5)
    a_score -= (a_injuries * 2.5)
    
    # Apply Turnaround Penalties (Short 5-day turnaround hurts performance)
    if h_turnaround == "Short (5 days)": h_score -= 1.5
    if a_turnaround == "Short (5 days)": a_score -= 1.5
    
    margin = h_score - a_score
    abs_margin = abs(margin)
    
    # Determine Winner and Custom 1-8 / 9+ Brackets
    if margin > 1.5:
        winner = h_name
        bracket = "1-8 points" if abs_margin <= 8 else "9+ points"
    elif margin < -1.5:
        winner = a_name
        bracket = "1-8 points" if abs_margin <= 8 else "9+ points"
    else:
        winner = "Draw / Even Match"
        bracket = "1-4 points"
        
    return winner, bracket

# STREAMLIT USER INTERFACE
st.title("🏈 Manual NRL Halftime Predictor")
st.write("Manually enter match statistics and variables to generate a prediction.")

st.divider()

# 1. Team Names Input
col_n1, col_n2 = st.columns(2)
with col_n1:
    home_team = st.text_input("Home Team Name:", value="Broncos")
with col_n2:
    away_team = st.text_input("Away Team Name:", value="Rabbitohs")

st.divider()

# 2. General Game Environment
st.subheader("☀️ Environment")
weather_cond = st.selectbox("Weather Condition:", ["Dry", "Wet / Rain"])

st.divider()

# 3. Team Statistics Sliders
col_s1, col_s2 = st.columns(2)

with col_s1:
    st.markdown(f"### 🏠 {home_team} Stats")
    h_poss = st.slider(f"{home_team} Possession %", 20, 80, 50, step=1, key="h_pos")
    h_comp = st.slider(f"{home_team} Completion %", 40, 100, 80, step=1, key="h_cm")
    h_err = st.slider(f"{home_team} Errors", 0, 20, 4, step=1, key="h_er")
    h_pen = st.slider(f"{home_team} Penalties Conceded", 0, 15, 3, step=1, key="h_pe")
    h_inj = st.slider(f"{home_team} Missing Key Players", 0, 5, 0, step=1, key="h_in")
    h_turn = st.radio(f"{home_team} Turnaround Time", ["Normal (6+ days)", "Short (5 days)"], key="h_tu")

with col_s2:
    st.markdown(f"### ✈️ {away_team} Stats")
    # Automatically keeps possession equal to 100% total
    a_poss = 100 - h_poss
    st.write(f"**{away_team} Possession %:** {a_poss}%")
    
    a_comp = st.slider(f"{away_team} Completion %", 40, 100, 80, step=1, key="a_cm")
    a_err = st.slider(f"{away_team} Errors", 0, 20, 4, step=1, key="a_er")
    a_pen = st.slider(f"{away_team} Penalties Conceded", 0, 15, 3, step=1, key="a_pe")
    a_inj = st.slider(f"{away_team} Missing Key Players", 0, 5, 0, step=1, key="a_in")
    a_turn = st.radio(f"{away_team} Turnaround Time", ["Normal (6+ days)", "Short (5 days)"], key="a_tu")

st.divider()

# 4. Result Processing
if home_team == away_team:
    st.warning("Please enter two different team names.")
else:
    winner, bracket = run_fully_manual_prediction(
        home_team, away_team, h_poss, a_poss, h_comp, a_comp, 
        h_err, a_err, h_pen, a_pen, weather_cond, h_inj, a_inj, h_turn, a_turn
    )
    
    st.subheader("📊 Generated Halftime Prediction")
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.markdown("**Predicted HT Leader:**")
        st.info(f"🏆 {winner}")
    with res_col2:
        st.markdown("**Predicted HT Margin:**")
        st.success(f"📏 {bracket}")
