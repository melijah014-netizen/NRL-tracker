#PROJECT NAME: HT Edge

#OVERVIEW

#Build a complete Android mobile application called HT Edge.

#Purpose:
#Predict NRL halftime winners and halftime margins (1-8 or 9+) using first-half statistics, team news, venue information, weather conditions, travel fatigue and historical data.

#Target users:
#Sports bettors who specialize in NRL halftime betting.

Platform:
Android first.

Framework:
Flutter (latest stable version).

Backend:
FastAPI (Python).

Database:
SQLite for local storage.
Allow future migration to PostgreSQL.

Architecture:
Clean architecture.
Separate UI, Services, Models, Database and Prediction Engine.

====================================

MAIN FEATURES

====================================

1. DASHBOARD

Display:

- Upcoming NRL matches
- Round number
- Match date and time
- Venue
- Home team
- Away team

Each match card should display:

- Predicted halftime winner
- Predicted halftime margin
- Confidence score

Example:

Storm vs Broncos

Prediction:
Storm HT 9+

Confidence:
87%

====================================

2. MATCH ANALYSIS SCREEN

Display complete prediction breakdown.

Show:

Predicted outcomes:

- Home Team HT 1-8
- Home Team HT 9+
- Away Team HT 1-8
- Away Team HT 9+

Example:

Storm HT 1-8 = 31%
Storm HT 9+ = 47%
Broncos HT 1-8 = 15%
Broncos HT 9+ = 7%

Display:

Confidence Score

Display:

Reasons for prediction

Example:

+ Strong recent form
+ Better completion rate
+ Opponent missing halfback
+ Strong record at venue

====================================

3. TEAM STATISTICS SCREEN

Store and display:

FIRST HALF ATTACK

- Average first-half points scored
- Average first-half tries scored
- Average first-half line breaks
- Average first-half tackle breaks
- Average first-half run metres

FIRST HALF DEFENCE

- Average first-half points conceded
- Average first-half tries conceded
- Average first-half line breaks conceded
- Average first-half missed tackles

DISCIPLINE

- First-half completion percentage
- First-half errors
- First-half penalties conceded
- First-half six-again concessions

POSSESSION

- First-half possession %
- First-half territory %

GAME STARTING STRENGTH

- Points scored in first 10 minutes
- Points scored in first 20 minutes
- Points conceded in first 10 minutes
- Points conceded in first 20 minutes

HALFTIME RECORD

- Wins
- Losses
- Draws

====================================

4. TEAM NEWS SCREEN

Store:

- Injuries
- Suspensions
- Late withdrawals
- Debutants
- Positional changes

Allow manual entry.

Each change should trigger prediction recalculation.

====================================

5. BET TRACKER

User can enter:

- Match
- Selection
- Stake
- Odds
- Result

Track:

- Total bets
- Wins
- Losses
- Strike rate
- ROI
- Profit/Loss

Show graphs.

====================================

6. SETTINGS SCREEN

Allow:

- Weight adjustment
- Dark mode
- Light mode
- Backup database
- Restore database

====================================

PREDICTION ENGINE

====================================

Create a scoring engine.

Factors and weights:

First-half statistics = 35%

Recent form = 20%

Completion rate = 15%

Injuries and lineup changes = 10%

Venue performance = 7%

Travel fatigue = 5%

Weather = 3%

Head-to-head history = 3%

Market movement = 2%

Total = 100%

====================================

RECENT FORM

====================================

Calculate:

Last 3 matches

Weight = 50%

Last 5 matches

Weight = 30%

Season average

Weight = 20%

====================================

VENUE FACTOR

====================================

Store:

- Home record
- Away record
- Venue-specific halftime record
- Average halftime margin at venue

====================================

TRAVEL FACTOR

====================================

Store:

- Travel distance
- Interstate travel
- International travel
- Days since last game

====================================

WEATHER FACTOR

====================================

Allow manual input:

- Fine
- Rain
- Windy
- Humid

====================================

MATCH TIMING FACTOR

====================================

Store:

- Afternoon
- Evening
- Night

Include in prediction calculations.

====================================

HEAD TO HEAD

====================================

Store:

Last 5 meetings

Last 10 meetings

Venue-specific meetings

Only use halftime results.

====================================

CONFIDENCE SCORE

====================================

Generate:

0-100 score

Classification:

90-100 = Elite Play

80-89 = Strong Play

70-79 = Moderate Play

60-69 = Risky Play

Below 60 = Avoid

====================================

DATABASE TABLES

====================================

Teams

Matches

Players

Injuries

VenueData

WeatherData

TravelData

TeamStatistics

HeadToHead

Predictions

BetTracker

Settings

====================================

UI DESIGN

====================================

Modern betting-style interface.

Dark theme default.

Use cards.

Use charts.

Use team logos.

Responsive layout.

Fast loading.

====================================

FUTURE FEATURES

====================================

Build architecture to support future APIs:

- NRL statistics API
- Odds API
- Weather API
- Injury API
- News API

Create placeholders for future integration.

====================================

DELIVERABLES

====================================

Generate:

1. Complete Flutter project
2. All source code
3. Database models
4. Prediction engine
5. Sample data
6. Android build instructions
7. APK build instructions
8. README.md
9. Installation guide

The application must compile successfully without errors.
