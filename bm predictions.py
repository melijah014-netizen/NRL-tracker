

import json

def calculate_halftime_prediction(live_data):
    """
    Calculates the predicted halftime winning team and margin bracket.
    Designed to trigger around the 25-30 minute mark of the first half.
    """
    # 1. Parse Live Match Stats (First 25 minutes)
    home_name = live_data["home_team"]["name"]
    away_name = live_data["away_team"]["name"]
    
    # 2. Extract Key Performance Indicators (KPIs)
    h_poss = live_data["home_team"]["possession_pct"]
    a_poss = live_data["away_team"]["possession_pct"]
    
    h_comp = live_data["home_team"]["completion_pct"]
    a_comp = live_data["away_team"]["completion_pct"]
    
    h_err = live_data["home_team"]["errors"]
    a_err = live_data["away_team"]["errors"]
    
    h_pen = live_data["home_team"]["penalties"]
    a_pen = live_data["away_team"]["penalties"]
    
    # Historical average 1st half margin (Last 5 games)
    h_hist = live_data["home_team"]["hist_first_half_avg_margin"]
    a_hist = live_data["away_team"]["hist_first_half_avg_margin"]

    # 3. Momentum Formula
    # Weightings: Possession (40%), Completion (30%), Errors (-1.5 pts), Penalties (-2.0 pts)
    h_momentum = (h_poss * 0.4) + (h_comp * 0.3) - (h_err * 1.5) - (h_pen * 2.0)
    a_momentum = (a_poss * 0.4) + (a_comp * 0.3) - (a_err * 1.5) - (a_pen * 2.0)

    # 4. Total Expected Score Layer
    h_total_score = h_momentum + h_hist
    a_total_score = a_momentum + a_hist
    
    expected_margin = h_total_score - a_total_score

    # 5. Determine Winner and Bracket Margin
    if expected_margin > 4:
        winner = home_name
        if expected_margin > 12:
            margin_bracket = "Dominant Lead (12+ points)"
        else:
            margin_bracket = "Comfortable Lead (6-10 points)"
            
    elif expected_margin < -4:
        winner = away_name
        if expected_margin < -12:
            margin_bracket = "Dominant Lead (12+ points)"
        else:
            margin_bracket = "Comfortable Lead (6-10 points)"
            
    else:
        winner = "Too Close to Call / Draw"
        margin_bracket = "Tight / Line Ball (1-4 points)"

    # 6. Return Clean Output
    return {
        "predicted_halftime_leader": winner,
        "predicted_margin_bracket": margin_bracket,
        "calculation_confidence": "High" if abs(expected_margin) > 8 else "Medium"
    }

# ==========================================
# EXAMPLE MATCH DATA (How a developer will feed data into the function)
# ==========================================
sample_match_payload = {
    "home_team": {
        "name": "Brisbane Broncos",
        "possession_pct": 58,
        "completion_pct": 82,
        "errors": 2,
        "penalties": 1,
        "hist_first_half_avg_margin": 4.2
    },
    "away_team": {
        "name": "South Sydney Rabbitohs",
        "possession_pct": 42,
        "completion_pct": 68,
        "errors": 6,
        "penalties": 4,
        "hist_first_half_avg_margin": -1.5
    }
}

# Run a test of the predictive feature
prediction = calculate_halftime_prediction(sample_match_payload)
print(json.dumps(prediction, indent=4))
