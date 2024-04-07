import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('../')
import cpv_new_categories
import seaborn as sns

categories = cpv_new_categories.categories

new_categories = []
cpv_codes = []

categories_nb = {
    "Secteur primaire et ressources naturelles" : 0,
    "Industrie et technologie" : 1,
    "Équipement et construction": 2, 
    "Services et numérique": 3,
    "Services sociaux et culturels": 4
}

transformed_categories = {}

for category, subcategories in categories.items():
    transformed_categories[category] = list(subcategories.keys())

def create_new_csv(df_lots_copy):

    for i, row in df_lots_copy.iterrows():
        cpv = str(row['cpv'])[:2]
        #Replace cpv by cpv new category index
        for cat, cpv_codes in transformed_categories.items():
            for code in cpv_codes:
                if code == cpv:
                    df_lots_copy.at[i, 'cpv'] = categories_nb[cat]

    return df_lots_copy


def calculate_stats_and_draw_graph(df_lots_new_cpv):

    cpv_counts = df_lots_new_cpv['cpv'].value_counts()

    # Calculate statistical measures
    mean_occurrences = cpv_counts.mean()
    std_dev_occurrences = cpv_counts.std()
    quantiles_occurrences = cpv_counts.quantile([0.25, 0.5, 0.75])
    min_occurrences = cpv_counts.min()
    max_occurrences = cpv_counts.max()

    # Write statistical measures to a file
    with open('questionnements/cpv/domains_statistics.txt', 'w') as file:
        file.write(f"Mean: {mean_occurrences}\n")
        file.write(f"Standard Deviation: {std_dev_occurrences}\n")
        file.write(f"Quantiles:\n{quantiles_occurrences}\n")
        file.write(f"Min: {min_occurrences}\n")
        file.write(f"Max: {max_occurrences}\n")

    # Write each cpv along with its count to a file
    with open('questionnements/cpv/domains_nb_of_appearances.csv', 'w') as file:
        for cpv, count in cpv_counts.items():
            print(f"{cpv}, {count}", file=file)

    plt.figure(figsize=(10, 8))
    cpv_counts.plot(kind='bar', color='skyblue')
    plt.title('Domain by Occurrence')
    plt.xlabel('Domains')
    plt.ylabel('Number of Occurrences')
    plt.tight_layout()
    plt.savefig('questionnements/cpv/domains_distribution.png')
    #plt.show()

def draw_domains_by_date(df_lots_new_cpv):

    plt.figure(figsize=(12, 8))

    # Count occurrences for each category on each date
    df_counts = df_lots_new_cpv.groupby(['awardDate', 'cpv']).size().reset_index(name='count')
    df_counts = df_counts.sort_values(by='awardDate')

    palette = sns.color_palette("husl", n_colors=len(df_counts['cpv'].unique()))

    # Use Seaborn's lineplot to plot multiple lines for each category with the custom color palette
    sns.lineplot(x='awardDate', y='count', hue='cpv', data=df_counts, palette=palette)

    plt.title('Domains Over Time')
    plt.xlabel('Time')
    plt.ylabel('Domains')
    plt.grid(True)
    plt.savefig('questionnements/cpv/domains_over_time.png')
    #plt.show()

def draw_domains_by_date_over_year(df_lots_new_cpv):

    # Convert 'awardDate' to datetime if not already
    df_lots_new_cpv['awardDate'] = pd.to_datetime(df_lots_new_cpv['awardDate'])

    plt.figure(figsize=(12, 8))

    # Extract month from 'awardDate'
    df_lots_new_cpv['month'] = df_lots_new_cpv['awardDate'].dt.month

    # Count occurrences for each domain in each month
    df_counts = df_lots_new_cpv.groupby(['month', 'cpv']).size().reset_index(name='count')

    # Calculate the average count for each typeOfContract in each month
    df_avg_counts = df_counts.groupby('cpv')['count'].std().reset_index(name='average_count')

    # Merge the average counts back to the original dataframe
    df_counts = pd.merge(df_counts, df_avg_counts, on='cpv')

    # Normalize the count by the average to get percentage
    df_counts['percentage'] = (df_counts['count'] / df_counts['average_count']) * 100

    # Use Seaborn's lineplot to plot multiple lines for each domain
    sns.lineplot(x='month', y='percentage', hue='cpv', data=df_counts)

    plt.title('Average Distribution of Each Domain Across a Year')
    plt.xlabel('Months')
    plt.ylabel('Percentage')
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.savefig('questionnements/cpv/domains_distribution_in year.png')
    #plt.show()


def execute_file(df_lots):
    new_df = create_new_csv(df_lots.copy())
    new_df.to_csv('data/Lots_cleaned_new_cpv.csv', sep=",")
    calculate_stats_and_draw_graph(new_df)
    draw_domains_by_date(new_df)
    draw_domains_by_date_over_year(new_df)