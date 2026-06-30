# 🏏 IPL Cricket Analytics Dashboard

A comprehensive, interactive cricket analytics platform built with **Python and Streamlit**. Analyze IPL (Indian Premier League) statistics from 2008-2025 with detailed insights on players, bowlers, teams, and venues.

## 🎯 Overview

This project provides an interactive web-based dashboard for exploring extensive IPL cricket analytics. With over **1,169 matches** and **278,000+ deliveries** analyzed, it offers deep insights into player performance, team statistics, and venue-specific trends.

**Live Dashboard:** Run the Streamlit app to explore real-time analytics

## ✨ Features

### 🏏 Player Analytics
- **Career Overview**: Runs scored across seasons with progression tracking
- **Performance Analysis**: Runs against specific teams and venue breakdowns
- **Advanced Insights**: Dismissal type distribution and scoring patterns
- **Key Metrics**: Highest scores, 50s, and 100s count
- **Data Tables**: Expandable season-by-season breakdowns

### 🎯 Bowler Analytics
- **Career Statistics**: Matches, wickets, economy rate, and bowling average
- **Performance Tracking**: Wicket progression by season
- **Opponents Analysis**: Wickets against each batting team
- **Venue Performance**: Bowling statistics at different venues
- **Achievements**: Best bowling figures, 3-wicket and 5-wicket hauls

### 🏆 Team Analytics
- **Career Overview**: Total matches, wins, losses, and win percentage
- **Season Performance**: Win rate trends across all seasons
- **Team Composition**: Top run scorers and wicket takers
- **Head-to-Head**: Comparative analysis against other teams
- **Performance Summary**: Season statistics and career metrics

### 🏟️ Venue Analytics
- **Venue Statistics**: Total matches hosted and seasons covered
- **Team Performance**: Win records at specific venues
- **Venue Insights**: First/last matches and most active teams
- **Performance Metrics**: Average runs, wicket rates, and trends
- **Recent Matches**: Historical match data at each venue

## 📊 Dashboard Pages

| Page | Description | Key Features |
|------|-------------|--------------|
| **Home** | Main dashboard overview | Quick stats, module guide, feature overview |
| **1_Player_Analytics** | Individual player statistics | Career, performance, and advanced insights tabs |
| **2_Bowler_Analytics** | Bowler performance metrics | Career, performance, and venue insights tabs |
| **3_Team_Analytics** | Team-level statistics | Season performance, team composition, head-to-head |
| **4_Venue_Analytics** | Venue-specific trends | Statistics, team performance, insights |

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/CricketAnalytics.git
   cd CricketAnalytics
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
CricketAnalytics/
├── dashboard/
│   ├── app.py                          # Main Streamlit app
│   └── pages/
│       ├── 1_Player_Analytics.py       # Player statistics page
│       ├── 2_Bowler_Analytics.py       # Bowler statistics page
│       ├── 3_Team_Analytics.py         # Team statistics page
│       └── 4_Venue_Analytics.py        # Venue statistics page
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py                  # Data loading utilities
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── batting.py                  # Batting analysis functions
│   │   ├── bowling.py                  # Bowling analysis functions
│   │   └── team.py                     # Team analysis functions
│   ├── services/
│   │   └── dashboard_data.py           # Dashboard data services
│   ├── utils/
│   │   └── team_names.py               # Team name utilities
│   └── visualizations/
│       ├── __init__.py
│       ├── batting_plots.py            # Batting visualizations
│       ├── bowling_plots.py            # Bowling visualizations
│       ├── plotly_charts.py            # Interactive Plotly charts
│       └── team_plots.py               # Team visualizations
│
├── data/
│   ├── raw/
│   │   ├── deliveries_updated_ipl_upto_2025.csv
│   │   ├── deliveries_updated_mens_ipl.csv
│   │   ├── IPL_ball_by_ball_updated.csv
│   │   ├── matches_updated_ipl_upto_2025.csv
│   │   └── matches_updated_mens_ipl.csv
│   └── processed/
│
├── notebooks/
│   ├── batting_analysis.ipynb
│   ├── bowling_analysis.ipynb
│   ├── data_exploration.ipynb
│   └── team_analysis.ipynb
│
├── models/
├── reports/
│   └── figures/
│
├── requirements.txt
├── README.md
└── test.py
```

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python 3.13** | Core programming language |
| **Streamlit** | Interactive web dashboard framework |
| **Pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computations |
| **Plotly** | Interactive data visualizations |
| **Matplotlib** | Statistical plotting |
| **Git & GitHub** | Version control |

## 📊 Dataset Overview

**Source:** IPL Ball-by-Ball Dataset (2008-2025)

**Coverage:**
- 1,169+ matches
- 278,000+ deliveries
- 18 seasons
- 14 teams
- Complete match and delivery-level data

**Key Data Files:**
- `deliveries_updated_ipl_upto_2025.csv` - Ball-by-ball delivery data
- `matches_updated_ipl_upto_2025.csv` - Match summary data
- Historical data from 2008 to 2025

## 💻 How to Use

### Navigating the Dashboard

1. **Launch the app** - Run `streamlit run dashboard/app.py`
2. **Explore modules** - Use the left sidebar to navigate between analytics pages
3. **Select filters** - Choose a player, bowler, team, or venue from dropdowns
4. **View visualizations** - Interactive charts update based on your selections
5. **Interact with charts** - Hover for details, zoom, pan, and download charts

### Example Workflows

**Analyze a specific player:**
1. Go to Player Analytics
2. Select player from dropdown
3. Browse through Career Overview, Performance, and Advanced tabs
4. Check highest scores, milestones, and performance against teams

**Compare teams:**
1. Go to Team Analytics
2. Select a team
3. Check season performance, top players, and head-to-head records

**Explore venues:**
1. Go to Venue Analytics
2. Select a venue
3. View team performance and historical trends at that venue

## 🔍 Key Functions

### Analytics Functions
- `player_runs_by_season()` - Player runs progression
- `player_runs_against_teams()` - Runs scored against specific teams
- `bowler_summary()` - Complete bowler statistics
- `team_win_by_season()` - Team win percentage trends
- And more...

### Visualization Functions
- `horizontal_bar()` - Plotly bar charts
- `line_chart()` - Line progression charts
- `pie_chart()` - Distribution charts

## 📈 Future Enhancements

- [ ] Player comparison tool
- [ ] Match prediction model
- [ ] Advanced filtering options
- [ ] Export functionality (PDF, CSV)
- [ ] Real-time data updates
- [ ] Player injury impact analysis
- [ ] Advanced statistics (runs per over, dot ball percentage)
- [ ] Trend analysis and forecasting

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue for bugs and feature requests.

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

Shreyas TK

## 📞 Support

For questions or issues, please open an issue on GitHub or contact the project maintainer.

---

**Last Updated:** 2025 IPL Season | Data Coverage: 2008-2025