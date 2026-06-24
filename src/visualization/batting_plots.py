# Visualization of batting  
import matplotlib.pyplot as plt

def plot_top_run_scorers(df):

    df = df.sort_values('batsman_runs',ascending = False)
    
    plt.figure(figsize=(10,6))

    plt.barh(
        df['batsman'],
        df['batsman_runs']
    )
    plt.xlabel('Runs')
    plt.ylabel('Batsman')
    plt.title('Top IPL Run Scorers')

    plt.tight_layout()

    plt.savefig('reports/figures/top_run_scorers.png')
    plt.show()