from src.analytics.batting import (
    batting_average,
    boundary_percentage,
    player_batting_summary,
    player_runs_against_teams,
    player_runs_by_season,
    player_runs_by_venue,
    strike_rate,
    top_run_scorers,
)
from src.analytics.bowling import economy_rate, top_wicket_takers
from src.analytics.team import (
    highest_scoring_venues,
    team_win_percentage,
    toss_impact,
    venue_toss_impact,
)
from src.data_loader import load_data


def main() -> None:
    """Run a lightweight smoke test for analytics outputs."""
    matches, deliveries = load_data()

    print(top_run_scorers(deliveries))
    print(top_wicket_takers(deliveries))
    print(batting_average(deliveries))
    print(strike_rate(deliveries))
    print(economy_rate(deliveries))
    print(boundary_percentage(deliveries))
    print(team_win_percentage(matches))
    print("match toss winner")
    print(toss_impact(matches))
    print("highest scoring venue")
    print(highest_scoring_venues(matches, deliveries))
    print(matches["toss_decision"].value_counts())
    print(matches["outcome"].value_counts())
    print(venue_toss_impact(matches))

    summary = player_batting_summary(deliveries, "V Kohli")
    print(summary)
    print(player_runs_by_season(deliveries, matches, "V Kohli"))
    print(deliveries.columns)
    print(matches.columns)
    print(player_runs_against_teams(deliveries, "V Kohli"))
    print(player_runs_by_venue(deliveries, matches, "V Kohli"))


if __name__ == "__main__":
    main()
