from data_loader import load_data

matches , deliveries = load_data()

print(matches.shape)
print(deliveries.shape)

from data_loader import load_data
from analytics import top_runs_scorers
from analytics import strike_rate
matches , deliveries = load_data()

print(top_runs_scorers(deliveries))
print("strike_rate")
print(strike_rate(deliveries))