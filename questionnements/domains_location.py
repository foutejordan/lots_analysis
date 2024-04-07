import pandas as pd
import matplotlib.pyplot as plt
import folium
import pandas as pd
from selenium import webdriver

def main_function(df_lots_domain, df_suppliers, df_agents):
    merged_on_agent_id = pd.merge(df_suppliers, df_agents[['agentId', 'longitude', 'latitude']], on='agentId', how='left')

    domain_location = pd.merge(merged_on_agent_id, df_lots_domain[['lotId', 'cpv']], on='lotId', how='left')

    def get_color(cpv):
        if cpv == '0':
            return 'blue'
        elif cpv == '1':
            return 'red'
        elif cpv == '2':
            return 'yellow'
        elif cpv == '3':
            return 'pink'
        else:
            return 'green'

    percentages = [0.05, 0.001]
    data = domain_location.dropna(subset=['latitude', 'longitude'])

    for per in percentages:
        # Sample the data
        sampled_data = data.sample(frac=per, random_state=42)

        sampled_data['latitude'] = pd.to_numeric(sampled_data['latitude'], errors='coerce')
        sampled_data['longitude'] = pd.to_numeric(sampled_data['longitude'], errors='coerce')
        sampled_data = sampled_data.dropna(subset=['latitude', 'longitude'])

        # Create a folium map centered at the mean of latitude and longitude
        map_center = [sampled_data['latitude'].mean(), sampled_data['longitude'].mean()]
        mymap = folium.Map(location=map_center, zoom_start=10)

        # Add markers for each data point with custom colors based on 'cpv'
        for index, row in sampled_data.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"Lat: {row['latitude']}, Lon: {row['longitude']}",
                icon=folium.Icon(color=get_color(row['cpv']))
            ).add_to(mymap)

        percentage_str = str(per).replace('.', '_')
        # Save the map as an HTML file
        mymap.save('questionnements/cpv/map_domains_'+percentage_str+'.html')


def execute_file(df_suppliers_cleaned, df_agents_cleaned,df_lots_new_cpv ):
    main_function(df_lots_new_cpv, df_suppliers_cleaned, df_agents_cleaned)
