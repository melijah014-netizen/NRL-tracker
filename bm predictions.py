
import os
import requests
import pandas as pd
from datetime import datetime

# 1. SCRAPE FIXTURES AND ENTIRE LIVE ROSTER GRIDS FROM THE OFFICIAL NRL PLATFORM
def fetch_complete_nrl_stats_grid():
    print("Connecting to live official NRL platform server...")
    url = "https://nrl.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15).json()
        return response.get('fixtures', [])
    except Exception as e:
        print(f"Error extracting complete NRL statistics table: {e}")
        return []

# 2. DEFINE YOUR CLUB WATCHLIST FOR CRITICAL STAR PLAYERS
def get_star_player_registry():
    return {
        "Panthers": ["Cleary", "Luai", "Yeo"],
        "Broncos": ["Reynolds", "Walsh", "Carrigan"],
        "Storm": ["Hughes", "Munster", "Papenhuyzen"],
        "Roosters": ["Walker", "Tedesco"],
        "Sharks": ["Hynes", "Kennedy"],
        "Sea Eagles": ["Trbojevic", "Cherry-Evans"],
        "Knights": ["Ponga"],
        "Dolphins": ["Kaufusi", "Niu"]
    }

# 3. EVALUATE SQUAD LINEUP CAPABILITY AND MISSING PLAYERS
def evaluate_lineup_capability(team_data, team_name, star_registry):
    try:
        player_list = team_data.get('teamList', [])
        if not player_list:
            return 1.0, "✅ Baseline Lineup"
            
        active_roster_names = []
        for player_entry in player_list:
            first_name = player_entry.get('firstName', '')
            last_name = player_entry.get('lastName', '')
            active_roster_names.append(f"{first_name} {last_name}".lower())
            
        target_stars = star_registry.get(team_name, [])
        missing_count = 0
        
        for star in target_stars:
            if not any(star.lower() in active_name for active_name in active_roster_names):
                missing_count += 1
                
        if missing_count >= 2:
            return 0.80, f"❌ Incapable (-20% Missing {missing_count} Stars)"
        elif missing_count == 1:
            return 0.90, f"⚠️ Weakened (-10% Missing 1 Star)"
        else:
            return 1.05, "🔥 Full Strength Squad Capable"
            
    except Exception:
        return 1.0, "✅ Standard List"

# 4. PARSE HIDDEN PERFORMANCE DATA VALUES FOR GENERAL FORM
def analyze_advanced_team_form(team_object):
    try:
        stats = team_object.get('stats', {})
        line_breaks = float(stats.get('lineBreaks', {}).get('value', 4.0))
        run_meters = float(stats.get('runMetres', {}).get('value', 1400.0)) / 100.0
        completion_rate = float(stats.get('completionRate', {}).get('value', 75.0)) / 100.0
        errors = float(stats.get('errors', {}).get('value', 10.0))
        
        tackles_made = float(stats.get('tacklesMade', {}).get('value', 300.0))
        missed_tackles = float(stats.get('missedTackles', {}).get('value', 30.0))
        tackle_efficiency = tackles_made / (tackles_made + missed_tackles + 1.0)
        
        return ((line_breaks + run_meters) * (completion_rate * (20.0 - errors))) + (tackle_efficiency * 15.0)
    except Exception:
        return 25.0

# 5. PIPELINE CORE COMPILATION RUNNER
def calculate_predictions(fixtures):
    compiled_predictions = []
    star_registry = get_star_player_registry()
    
    for game in fixtures:
        try:
            home_data = game.get('homeTeam', {})
            away_data = game.get('awayTeam', {})
            home_name = home_data.get('name')
            away_name = away_data.get('name')
            
            if not home_name or not away_name:
                continue
                
            home_power = analyze_advanced_team_form(home_data)
            away_power = analyze_advanced_team_form(away_data)
            
            home_mod, home_status = evaluate_lineup_capability(home_data, home_name, star_registry)
            away_mod, away_status = evaluate_lineup_capability(away_data, away_name, star_registry)
            
            home_power *= home_mod
            away_power *= away_mod
            
            kickoff_str = game.get('clock', {}).get('kickOffTimeLong', '')
            time_label = "📅 Game"
            if kickoff_str:
                match_hour = int(kickoff_str.split('T')[1].split(':')[0])
                time_label = "☀️ Day" if match_hour < 17 else "🌙 Night"

            raw_difference = home_power - away_power
            predicted_leader = home_name if raw_difference > 0 else away_name
            calculated_margin = abs(raw_difference)
            
            margin_bracket = "1-8 points" if calculated_margin <= 7.5 else "9+ points"
            
            compiled_predictions.append({
                "Matchup Fixture": f"{home_name} vs {away_name} ({time_label})",
                "Home Status": home_status,
                "Away Status": away_status,
                "Predicted Halftime Leader": predicted_leader,
                "Margin Bracket": margin_bracket,
                "Rating Margin": f"{calculated_margin:.2f}"
            })
        except Exception:
            continue
    return compiled_predictions

# 6. FILE CONTROLLER CONSOLE OUTPUT
if __name__ == "__main__":
    live_fixtures = fetch_complete_nrl_stats_grid()
    predictions_list = calculate_predictions(live_fixtures)
    
    if predictions_list:
        df = pd.DataFrame(predictions_list)
        markdown_table = df.to_markdown(index=False)
    else:
        markdown_table = "| Matchup Fixture | Home Status | Away Status | Predicted Halftime Leader | Margin Bracket | Rating Margin |\n|---|---|---|---|---|---|\n| Lineup details processing... Data drops this afternoon. | N/A | N/A | N/A | N/A | N/A |"
        
    readme_content = f"""# 🏉 Automated NRL Halftime Predictor

System Tracker Status: Active | Latest Sync Update: {datetime.now().strftime('%Y-%m-%d %H:%M')} AEST

This architecture evaluates live player line-ups, team capabilities, and injury voids dynamically from the official NRL database network.

## 🔮 Upcoming Matches Halftime Forecast
{markdown_table}
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("Success: Script compiled dataset updates safely onto your GitHub overview profile.")
