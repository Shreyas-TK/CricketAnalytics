from src.data_loader import load_data

from src.analytics.batting import (
    top_run_scorers,
    strike_rate,
    batting_average,
    boundary_percentage
)

from src.analytics.bowling import (
    top_wicket_takers,
    economy_rate
)

matches, deliveries = load_data()

print(top_run_scorers(deliveries))
print(top_wicket_takers(deliveries))
print(batting_average(deliveries))
print(economy_rate(deliveries))
print(boundary_percentage(deliveries))

from src.analytics.team import (team_win_percentage, toss_impact, highest_scoring_venues, toss_impact, venue_toss_impact)

print(team_win_percentage(matches))
print("match toss winner")
print(toss_impact(matches))
print ('highest scoring venue')
print(highest_scoring_venues(matches,deliveries))
print(matches["toss_decision"].value_counts())
print(matches["outcome"].value_counts())
print(toss_impact(matches))
print(venue_toss_impact(matches))

#Batting visualization test
# from src.visualization.batting_plots import(plot_top_run_scorers)

# runs = top_run_scorers(deliveries)
# plot_top_run_scorers(runs)

#Bowling visualization test 
# from src.visualization.bowling_plots import(plot_top_wicket_takers)

# wickets = top_wicket_takers(deliveries)
# plot_top_wicket_takers(wickets)

from src.visualization.team_plots import(plot_team_win_percentage)

teams = team_win_percentage(matches)
plot_team_win_percentage(teams)