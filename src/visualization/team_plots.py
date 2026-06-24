import matplotlib.pyplot as plt 

def plot_team_win_percentage(df):

    df = df.head(10)

    plt.figure(figsize=(12,6))

    plt.bar(
        df['team'],
        df['win_pct']
    )


    plt.xticks(rotation=45)

    plt.ylabel('win percentage')

    plt.title('IPL Team Win Percentage')

    plt.tight_layout()

    plt.show()
