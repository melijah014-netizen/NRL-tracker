
import streamlit as st

# Configure the page style
st.set_page_config(page_title="HT Edge - NRL Tracker", page_icon="🏉", layout="wide")

# App Header
st.title("🏉 HT Edge - NRL Halftime Tracker")
st.markdown("### Predict NRL Halftime Winners and Margins")
st.info("System Initialized: Ready to track upcoming NRL Round statistics.")

# Sidebar Settings
st.sidebar.header("⚙️ Settings & Weights")
st.sidebar.subheader("Prediction Weights")
st.sidebar.slider("First-Half Stats (%)", 0, 100, 35)
st.sidebar.slider("Recent Form (%)", 0, 100, 20)
st.sidebar.slider("Completion Rate (%)", 0, 100, 15)
st.sidebar.selectbox("Weather Condition", ["Fine", "Rain", "Windy", "Humid"])
theme = st.sidebar.radio("UI Theme", ["Dark Mode Default", "Light Mode"])

# Create Layout Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📈 Match Analysis", "🏅 Team Statistics", "📝 Bet Tracker"])

with tab1:
    st.subheader("Upcoming NRL Matches")
    
    # Sample Match Card 1
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("### ⚡ Storm vs Broncos")
        st.caption("Venue: AAMI Park | Target: Halftime Betting Market")
    with col2:
        st.metric(label="Predicted Winner", value="Storm HT 9+")
        st.progress(0.87, text="Confidence: 87% (Strong Play)")
        
    st.divider()

with tab2:
    st.subheader("Match Outcome Probability Breakdown")
    st.write("#### Storm vs Broncos Matrix")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Storm HT 1-8", "31%")
    col2.metric("Storm HT 9+", "47%")
    col3.metric("Broncos HT 1-8", "15%")
    col4.metric("Broncos HT 9+", "7%")
    
    st.markdown("#### Key Drivers for Prediction:")
    st.success("✔️ Strong home venue form and 84% completion rate over the last 3 matches.")
    st.warning("⚠️ Opponent missing starting halfback due to late injury withdrawal.")

with tab3:
    st.subheader("Team First-Half Database Statistics")
    team_select = st.selectbox("Select NRL Team", ["Melbourne Storm", "Brisbane Broncos", "Penrith Panthers", "Sydney Roosters"])
    
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.write("#### First Half Attack")
        st.write("- **Avg 1H Points Scored:** 14.5")
        st.write("- **Avg 1H Line Breaks:** 3.2")
    with sub_col2:
        st.write("#### First Half Defence")
        st.write("- **Avg 1H Points Conceded:** 6.2")
        st.write("- **Avg 1H Missed Tackles:** 8.4")

with tab4:
    st.subheader("Bet Tracker & ROI Dashboard")
    st.caption("Track performance outcomes and calculate your live betting metrics.")
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Total Bets Placed", "0")
    metric_col2.metric("Current Strike Rate", "0.0%")
    metric_col3.metric("Profit / Loss (Units)", "0.00")
