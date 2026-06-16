from src.data_loader import load_data

from src.analytics.batting import (
    top_run_scorers,
    strike_rate,
    batting_average
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