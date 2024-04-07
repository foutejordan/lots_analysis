import pandas as pd
import matplotlib.pyplot as plt
import folium
import pandas as pd
from selenium import webdriver

variables = ['city', 'zipcode', 'country', 'department']

def agents_addresses(df_agents_copy, is_cleaned_data):
    for var in variables:
        count = df_agents_copy[var].value_counts()

        # Calculate Statistics
        mean_occurrences = count.mean()
        std_dev_occurrences = count.std()
        quantiles_occurrences = count.quantile([0.25, 0.5, 0.75])
        min_occurrences = count.min()
        max_occurrences = count.max()

        # Write them in file
        path = ''
        if is_cleaned_data:
            path = '../descriptive_analysis/figs/univarie/agents/'
        else:
            path = 'figs/univarie/agents/'

        with open(path+var+'_statistics.txt', 'w') as file:
            file.write(f"Mean: {mean_occurrences}\n")
            file.write(f"Standard Deviation: {std_dev_occurrences}\n")
            file.write(f"Quantiles:\n{quantiles_occurrences}\n")
            file.write(f"Min: {min_occurrences}\n")
            file.write(f"Max: {max_occurrences}\n")

        # Write each city along with its count to a file
        with open(path+var+'_count.csv', 'w') as file:
            for item, ct in count.items():
                print(f"{item}, {ct}", file=file)

        ## Draw graphs

        # All data
        df = pd.read_csv(path+var+'_count.csv', header=None, names=[var, 'Occurences'])
        occurences = df['Occurences'].tolist()
        count.plot(kind='bar', color='skyblue')
        if var not in ['city', 'zipcode']:
            plt.xticks(rotation=45, ha='right') 
        else:
            plt.xticks([])
        plt.title(var+' by Occurrence')
        plt.xlabel(var)
        plt.ylabel('Number of Occurrences')
        plt.yscale('log')
        # plt.savefig('figs/agents_stats/'+var+'_count_log.png')
        if is_cleaned_data:
            plt.savefig('../descriptive_analysis/figs/univarie/agents/'+var+'_count_log_cleaned.png')
        else:
            plt.savefig('figs/univarie/agents/'+var+'_count_log.png')

        #plt.show()
                
        # Top 20
        top_20 = count.head(20)
        plt.yscale('linear')

        plt.figure(figsize=(12, 6))
        top_20.plot(kind='bar', color='skyblue')
        plt.title('Top 20 '+var+' by Occurrence')
        plt.xlabel('Top 20 '+var)
        plt.ylabel('Number of Occurrences')
        plt.tight_layout()

        # plt.savefig('figs/agents_stats/'+var+'_count_top_20.png')

        if is_cleaned_data:
            plt.savefig('../descriptive_analysis/figs/univarie/agents/'+var+'_count_top_20_cleaned.png')
        else:
            plt.savefig('figs/univarie/agents/'+var+'_count_top_20.png')
        #plt.show()

def create_maps(df_agents_copy, is_cleaned_data):
    percentages = [0.05, 0.001]
    data = df_agents_copy.dropna(subset=['latitude', 'longitude'])

    for per in percentages:

        # Samples the data
        sampled_data = data.sample(frac=per, random_state=42)

        # Create a folium map centered at the mean of latitude and longitude
        map_center = [sampled_data['latitude'].mean(), sampled_data['longitude'].mean()]
        mymap = folium.Map(location=map_center, zoom_start=10)

        # Add markers for each data point
        for index, row in sampled_data.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"Lat: {row['latitude']}, Lon: {row['longitude']}"
            ).add_to(mymap)

        percentage_str = str(per).replace('.', '_')
        # Save the map as an HTML file
        # mymap.save('figs/agents_stats/map_with_dots_'+percentage_str+'.html')
        if is_cleaned_data:
            mymap.save('../descriptive_analysis/figs/univarie/agents/map_with_dots_'+percentage_str+'_cleaned.html')
        else:
            mymap.save('figs/univarie/agents/map_with_dots_'+percentage_str+'.html')

def execute_file(df_agents, is_cleaned_data):
    agents_addresses(df_agents.copy(), is_cleaned_data)
    create_maps(df_agents.copy(), is_cleaned_data)
