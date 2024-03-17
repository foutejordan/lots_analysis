import pandas as pd
import matplotlib.pyplot as plt

variables = ['city', 'zipcode', 'country', 'department']

def agents_addresses(df_agents_copy):
    for var in variables:
        count = df_agents_copy[var].value_counts()

        # Calculate Statistics
        mean_occurrences = count.mean()
        std_dev_occurrences = count.std()
        quantiles_occurrences = count.quantile([0.25, 0.5, 0.75])
        min_occurrences = count.min()
        max_occurrences = count.max()

        # Write them in file
        with open('agents_stats/'+var+'_statistics.txt', 'w') as file:
            file.write(f"Mean: {mean_occurrences}\n")
            file.write(f"Standard Deviation: {std_dev_occurrences}\n")
            file.write(f"Quantiles:\n{quantiles_occurrences}\n")
            file.write(f"Min: {min_occurrences}\n")
            file.write(f"Max: {max_occurrences}\n")

        # Write each city along with its count to a file
        with open('agents_stats/'+var+'_count.csv', 'w') as file:
            for item, ct in count.items():
                print(f"{item}, {ct}", file=file)

        ## Draw graphs

        # All data
        df = pd.read_csv('agents_stats/'+var+'_count.csv', header=None, names=[var, 'Occurences'])
        occurences = df['Occurences'].tolist()
        n, bins, patches = plt.hist(occurences, bins= 200 ,edgecolor='black')
        plt.xlabel(var)
        plt.ylabel('Number of Occurrences')
        plt.yscale('log')
        plt.savefig('agents_stats/'+var+'_count_log.png')
        #plt.show()
                
        # Top 20
        top_20 = count.head(20)

        plt.figure(figsize=(12, 6))
        top_20.plot(kind='bar', color='skyblue')
        plt.title('Top 20 '+var+' by Occurrence')
        plt.xlabel('Top 20 '+var)
        plt.ylabel('Number of Occurrences')
        plt.xticks(rotation=45, ha='right') 
        plt.tight_layout()

        plt.savefig('agents_stats/'+var+'_count_top_20.png')
        #plt.show()

def execute_file(df_agents):
    agents_addresses(df_agents.copy())
