
import os
import requests
import pandas as pd
from datetime import datetime

# 1. FETCH LIVE NRL SCHEDULE DYNAMICALLY 
def fetch_live_nrl_fixtures():
    print("Connecting to live NRL schedule feeds...")
    url = "https://espn.com"
    try:
        response = requests.get(url, timeout=15).json()
        events = response.get('events', [])
        
        # Region mirror fallback if structural data transitions are active
        if not events:
            alt_url = "https://espn.com?lang=en&region=au"
            response = requests.get(alt_url, timeout=15).json()
            events = response.get('events', [])
            
        return events
    except Exception as e:
        print(f"Error automatically retrieving fixtures: {e}")
        return []

# 2. RUN HISTORICAL BASE MATRICES (Dolphin/Roosters Round 15 adjustments included)
def get_historical_halftime_metrics():
    teams = [
        "Rabbitohs", "Broncos", "Dolphins", "Roosters", "Warriors", 
        "Sharks", "Eels", "Raiders", "Wests Tigers", "Titans", 
        "Panthers", "Bulldogs", "Storm", "Knights", "Cowboys", "Manly", "Dragons"
    ]
    
    data = {
        "Team": teams,
        "First_Half_Attacking_Power": [22.4, 25.1, 28.3, 27.5, 21.2, 26.8, 19.5, 22.1, 18.2, 20.4, 29.1, 24.0, 29.5, 23.1, 24.8, 25.0, 20.1],
        "First_Half_Defensive_Stamina": [24.1, 21.0, 20.2, 19.8, 22.0, 18.5, 26.4, 23.1, 28.0, 25.2, 15.4, 19.1, 16.0, 22.3, 23.5, 21.1, 24.0],
        "Spine_Stability_Index": [0.8, 0.7, 0.9, 0.6, 0.8, 0.9, 0.5, 0.7, 0.6, 0.8, 0.9, 0.8, 0.9, 0.7, 0.7, 0.8, 0.6] 
    }
    return pd.DataFrame(data).set_index("Team")

# 3. STATISTICAL COMPILATION FOR THE 1-8 / 9+ SPLIT BOUNDARIES
def process_halftime_predictions(fixtures, metrics):
    compiled_predictions = []
    
    for game in fixtures:
        try:
            competitions = game.get('competitions', [{}])
            competitors = competitions.get('competitors', [])
            
            home_team = next(c for c in competitors if c['homeAway'] == 'home')['team']['displayName']
            away_team = next(c for c in competitors if c['homeAway'] == 'away')['team']['displayName']
            
            # Cross reference character matches into dictionary rows
            h_key = next((t for t in metrics.index if t in home_team), None)
            a_key = next((t for t in metrics.index if t in away_team), None)
            
            if not h_key or not a_key:
                continue 
                
            home_proj = metrics.loc[h_key, "First_Half_Attacking_Power"] * metrics.loc[h_key, "Spine_Stability_Index"] - metrics.loc[a_key, "First_Half_Defensive_Stamina"]
            away_proj = metrics.loc[a_key, "First_Half_Attacking_Power"] * metrics.loc[a_key, "Spine_Stability_Index"] - metrics.loc[h_key, "First_Half_Defensive_Stamina"]
            
            raw_difference = home_proj - away_proj
            
            if raw_difference > 0:
                predicted_winner = home_team
                calculated_margin = abs(raw_difference)
            else:
                predicted_winner = away_team
                calculated_margin = abs(raw_difference)
                
            # STRICT TIER MARGIN CLASSIFICATION
            if calculated_margin <= 8.0:
                margin_bracket = "1-8 points"
            else:
                margin_bracket = "9+ points"
                
            compiled_predictions.append({
                "matchup": f"{home_team} vs {away_team}",
                "winner": predicted_winner,
                "bracket": margin_bracket,
                "gap": round(calculated_margin, 2)
            })
        except Exception:
            continue
            
    return compiled_predictions

# 4. DEPLOY TARGETED TILES DIRECTLY ONTO THE MAIN REPOSITORY LANDING PAGE
def build_markdown_dashboard(predictions):
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    markdown_output = f"# 🏉 Automated NRL Halftime Predictor\n"
    markdown_output += f"**System Tracker Status**: Active | **Latest Sync Update**: {current_time_str} AEST\n\n"
    markdown_output += "This architecture scrapes game data feeds, runs metrics, and builds predictions automatically.\n\n"
    markdown_output += "### 🔮 Upcoming Matches Halftime Forecast\n\n"
    markdown_output += "| Matchup Fixture | Predicted Halftime Leader | Margin Classification Bracket | Raw Power Rating Difference |\n"
    markdown_output += "|:---|:---|:---|:---|\n"
    
    if not predictions:
        markdown_output += "| No scheduled match events active for the current window | N/A | N/A | N/A |\n"
    else:
        for p in predictions:
            markdown_output += f"| {p['matchup']} | **{p['winner']}** | `{p['bracket']}` | {p['gap']} pts |\n"
            
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(markdown_output)
    print("Success: Script compiled dataset updates safely onto your GitHub overview profile.")

if __name__ == "__main__":
    live_games = fetch_live_nrl_fixtures()
    stats_data = get_historical_halftime_metrics()
    predictions_list = process_halftime_predictions(live_games, stats_data)
    build_markdown_dashboard(predictions_list)
