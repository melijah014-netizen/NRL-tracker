import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

# Set mobile-responsive page layout
st.set_page_config(page_title="NRL Edge Master", layout="centered")

# File path to store our archived bets locally
DATA_FILE = "nrl_betting_ledger.csv"

# Load or initialize the local ledger archive
if os.path.exists(DATA_FILE):
    ledger_df = pd.read_csv(DATA_FILE)
else:
    ledger_df = pd.DataFrame(columns=[
        "Date", "Match", "Selected_Margin", "Stake", "Status", "Profit_Loss"
    ])

# --- HELPER AUTOMATED SCRAPER ---
def try_fetch_nrl_fixtures():
    try:
        url = "https://nrl.com"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            matches = []
            for item in soup.find_all(class_="match-team__name"):
                name = item.get_text().strip()
                if name and name not in matches:
                    matches.append(name)
            
            if len(matches) >= 2:
                pairings = [f"{matches[i]} vs {matches[i+1]}" for i in range(0, len(matches)-1, 2)]
                return pairings
    except Exception:
        pass
    return ["Bulldogs vs Eels", "Panthers vs Roosters", "Storm vs Sea Eagles"]

# --- APP UI ---
st.title("🏉 NRL Half-Time Strategy & Ledger")

tab1, tab2, tab3 = st.tabs(["📊 Live Match Engine", "📁 Bet Archive Ledger", "🌐 Web Sync Status"])

with tab1:
    st.header("Match Calculator")
    
    scraped_games = try_fetch_nrl_fixtures()
    selected_fixture = st.selectbox("Select Upcoming Matchup", scraped_games + ["Custom Matchup..."])
    
    if selected_fixture == "Custom Matchup...":
        t_a = st.text_input("Home Team", "Bulldogs")
        t_b = st.text_input("Away Team", "Eels")
        match_title = f"{t_a} vs {t_b}"
    else:
        match_title = selected_fixture
        teams = selected_fixture.split(" vs ")
        t_a, t_b = teams[0], teams[1] if len(teams) > 1 else ("Home", "Away")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t_a)
        comp_a = st.number_input(f"{t_a} Completion Rate %", 0, 100, 82, key="ca")
        spine_a = st.selectbox(f"{t_a} Spine Intact?", ["Yes", "No - Playmaker Missing"], key="sa")
    with col2:
        st.subheader(t_b)
        comp_b = st.number_input(f"{t_b} Completion Rate %", 0, 100, 74, key="cb")
        spine_b = st.selectbox(f"{t_b} Spine Intact?", ["Yes", "No - Playmaker Missing"], key="sb")

    st.markdown("---")
    turnaround = st.checkbox("Is a team backed up on a short 5-day turnaround?")
    travel = st.checkbox("Did a Sydney team travel long-distance (QLD/NZ)?")
    weather = st.selectbox("Weather Track Condition", ["Dry / Fast", "Overcast", "Heavy Rain / Wet"])

    # Strategy Evaluation Logic
    recommendation = "⚠️ NO CLEAR ADVANTAGE"
    reasons = []
    
    if comp_a >= 80 and comp_b >= 80:
        recommendation = "🎯 RECOMMENDED BET: 1–8 HALF-TIME MARGIN"
        reasons.append("High structural ball completion rates favor a tight arm wrestle.")
    if spine_b == "No - Playmaker Missing" or spine_a == "No - Playmaker Missing":
        recommendation = "🎯 RECOMMENDED BET: 1–8 HALF-TIME MARGIN"
        reasons.append("Disrupted elite playmaker spine forces conservative, clunky early sets.")
    if turnaround and travel and weather != "Heavy Rain / Wet":
        recommendation = "🔥 RECOMMENDED BET: 9+ HALF-TIME MARGIN"
        reasons.append("Heavy schedule fatigue meets travel loads; vulnerable to an early blowout.")
    if weather == "Heavy Rain / Wet":
        recommendation = "🎯 RECOMMENDED BET: 1–8 HALF-TIME MARGIN"
        reasons.append("Wet weather naturally limits handling execution and drops total first half margins.")

    if "1–8" in recommendation:
        st.success(recommendation)
    elif "9+" in recommendation:
        st.warning(recommendation)
    else:
        st.info(recommendation)
        
    for r in reasons:
        st.caption(f"✓ {r}")

    st.markdown("---")
    bankroll = st.number_input("Current Bankroll ($)", min_value=1, value=1000)
    confidence = st.slider("Confidence Level Scale", 1, 3, 2)
    pcts = {1: 0.01, 2: 0.02, 3: 0.05}
    calculated_stake = bankroll * pcts[confidence]
    st.metric("Recommended Risk Stake Allocation", f"${calculated_stake:.2f}")

    st.subheader("Log Live Position to Ledger")
    if st.button("Commit This Bet to Archive"):
        new_row = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Match": match_title,
            "Selected_Margin": "1-8" if "1–8" in recommendation else "9+",
            "Stake": calculated_stake,
            "Status": "Pending",
            "Profit_Loss": 0.0
        }
        ledger_df = pd.concat([ledger_df, pd.DataFrame([new_row])], ignore_index=True)
        ledger_df.to_csv(DATA_FILE, index=False)
        st.toast("Bet logged successfully into the Ledger Archive!", icon="💾")

with tab2:
    st.header("Betting Ledger Archive")
    
    if ledger_df.empty:
        st.info("No saved tracking rows found yet.")
    else:
        total_bets = len(ledger_df)
        wins = len(ledger_df[ledger_df["Status"] == "Won"])
        losses = len(ledger_df[ledger_df["Status"] == "Lost"])
        net_pl = ledger_df["Profit_Loss"].sum()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Bets", total_bets)
        c2.metric("Win / Loss", f"{wins}W - {losses}L")
        c3.metric("Net Profit / Loss", f"${net_pl:.2f}")
        
        st.markdown("---")
        st.subheader("Manage Active Positions")
        
        for index, row in ledger_df.iterrows():
            if row["Status"] == "Pending":
                with st.expander(f"⏳ Pending: {row['Match']} (${row['Stake']})"):
                    status_update = st.radio("Outcome", ["Pending", "Won", "Lost"], key=f"status_{index}")
                    odds_hit = st.number_input("Odds Secured", min_value=1.0, value=2.10, step=0.1, key=f"odds_{index}")
                    
                    if st.button("Resolve Position", key=f"btn_{index}"):
                        if status_update == "Won":
                            ledger_df.at[index, "Status"] = "Won"
                            ledger_df.at[index, "Profit_Loss"] = row["Stake"] * (odds_hit - 1)
                        elif status_update == "Lost":
                            ledger_df.at[index, "Status"] = "Lost"
                            ledger_df.at[index, "Profit_Loss"] = -row["Stake"]
                        
                        ledger_df.to_csv(DATA_FILE, index=False)
                        st.rerun()
                        
        st.subheader("Raw History Database")
        st.dataframe(ledger_df, use_container_width=True)

with tab3:
    st.header("System & Data Verification")
    st.markdown(
        """
        ### Pre-Game Routine:
        1. Open the official [NRL Match Centre](https://nrl.com).
        2. Verify final team announcements (published 60 minutes before kickoff).
        3. Match the completion stats from your app dashboard to the team lists, then lock in your 1-8 or 9+ allocation.
        """
    )
