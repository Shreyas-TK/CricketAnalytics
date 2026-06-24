import matplotlib.pyplot as plt 

def plot_top_wicket_takers(df):

    df = df.sort_values('wickets',ascending = False)

    plt.figure(figsize=(10,6))

    plt.barh(
        df['bowler'],
        df['wickets']
    )

    plt.xlabel("Wickets")

    plt.ylabel("Bowler")

    plt.title("Top IPL Wicket Takers")

    plt.tight_layout()

    plt.savefig('reports/figures/top_wicket_takers.png')

    plt.show()