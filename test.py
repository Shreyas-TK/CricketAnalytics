from src.data_loader import load_data

from src.analytics.batting import (
    top_run_scorers,
    strike_rate
)

from src.analytics.bowling import (
    top_wicket_takers
)

matches, deliveries = load_data()

print(top_run_scorers(deliveries))
print(top_wicket_takers(deliveries))