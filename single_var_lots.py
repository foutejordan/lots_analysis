import pandas as pd
import matplotlib.pyplot as plt

def draw_graph_award_date(df_lots_copy):

    column_name = 'awardDate'

    # Convert the column to datetime type if it's not already
    df_lots_copy[column_name] = pd.to_datetime(df_lots_copy[column_name], errors='coerce')

    # Filter dates between 2008 and 2025
    df_lots_copy = df_lots_copy[(df_lots_copy[column_name] >= '2008-01-01') & (df_lots_copy[column_name] <= '2025-12-31')]

    # Sort the DataFrame by the "awardDate" column
    df_lots_copy = df_lots_copy.sort_values(by=column_name)

    # Calculate statistical measures
    mean_date = df_lots_copy[column_name].mean()
    std_dev_date = df_lots_copy[column_name].std()
    quantiles_date = df_lots_copy[column_name].quantile([0.25, 0.5, 0.75])
    min_date = df_lots_copy[column_name].min()
    max_date = df_lots_copy[column_name].max()

    # Write statistical measures to a file
    with open('figs/lots_stats/date_statistics.txt', 'w') as file:
        file.write(f"Mean: {mean_date}\n")
        file.write(f"Standard Deviation: {std_dev_date}\n")
        file.write(f"Quantiles:\n{quantiles_date}\n")
        file.write(f"Min: {min_date}\n")
        file.write(f"Max: {max_date}\n")

    # Create a histogram using matplotlib
    plt.hist(df_lots_copy[column_name], bins=30, edgecolor='black')
    plt.title(f'Distribution of {column_name}')
    plt.xlabel(column_name)
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.savefig('figs/lots_stats/date_distribution_plot.png')
    #plt.show()

def execute_file(df_lots):
    draw_graph_award_date(df_lots.copy())