import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import community as comm_louvain
import numpy as np
from collections import defaultdict

def month_to_color(month):
    # Create color palette
    cmap = plt.cm.get_cmap('coolwarm')
    values = np.linspace(0, 1, 12)
    edge_colors = [cmap(value) for value in values]

    cmap = plt.cm.get_cmap('coolwarm')
    norm_month = (month - 1) / 11  # Normalize month to range [0, 1]
    return cmap(norm_month)

def main_function(df_lots, df_agents, df_buyers, df_suppliers):

    '''Prepare data'''
    # Sample lots
    sampled_lots_df = df_lots.sample(n=100000)

    # Merge
    merged_df = pd.merge(sampled_lots_df, df_buyers, on='lotId', suffixes=('', '_buyers'))
    merged_df.rename(columns={'agentId': 'buyersId'}, inplace=True)
    merged_df = pd.merge(merged_df, df_suppliers, on='lotId', suffixes=('', '_suppliers'))
    merged_df.rename(columns={'agentId': 'suppliersId'}, inplace=True)

    merged_df = merged_df[merged_df['lotId'].isin(sampled_lots_df['lotId'])]

    # Get months
    merged_df['awardDate'] = pd.to_datetime(merged_df['awardDate'])
    merged_df['awardMonth'] = merged_df['awardDate'].dt.month
    merged_df['edge_color'] = merged_df['awardMonth'].apply(month_to_color)

    # Keep only the top 20 cities
    city_counts = df_agents['city'].value_counts()
    top_cities = city_counts.head(20).index
    print(top_cities)
    sampled_df_agents = df_agents[df_agents['city'].isin(top_cities)]

    G = nx.Graph()

    for index, row in sampled_df_agents.iterrows():
        G.add_node(row['city'])

    total_months = defaultdict(int)
    connections_count = defaultdict(int)

    for index, row in merged_df.iterrows():
        agent_suppliers = row['buyersId']
        try:
            agent_suppliers_city = sampled_df_agents.loc[sampled_df_agents['agentId'] == agent_suppliers, 'city'].values[0]
        except:
            agent_suppliers_city = None
        agent_buyers = row['suppliersId']
        try:
            agent_buyers_city = sampled_df_agents.loc[sampled_df_agents['agentId'] == agent_buyers, 'city'].values[0]
        except:
            agent_buyers_city = None

        if agent_suppliers_city and agent_buyers_city and agent_suppliers_city != agent_buyers_city:
            # Calculate average month for the connected nodes
            avg_month = (row['awardMonth'])
            total_months[(agent_suppliers_city, agent_buyers_city)] += avg_month
            connections_count[(agent_suppliers_city, agent_buyers_city)] += 1

    # Calculate the average month for each pair of connected nodes
    avg_months = {}
    for connection, total_month in total_months.items():
        avg_months[connection] = total_month / connections_count[connection]

    # Assign colors based on the average month
    for connection, avg_month in avg_months.items():
        edge_color = month_to_color(avg_month)
        G.add_edge(connection[0], connection[1], color=edge_color)

    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, node_size=30, node_color='red')

    # Draw edges
    for u, v, edge_data in G.edges(data=True):
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=edge_data['color'], width=2.0)

    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=8, font_color='black')

    # Community detection using Louvain method
    best_partition = comm_louvain.best_partition(G, weight='weight', resolution=1.0)  # Weighted community detection

    plt.title('Echanges de lots entre les villes')
    with open('graphes/cities_yearly_communities.txt', 'w') as f:
        f.write("Communities:\n")
        for i, community in enumerate(best_partition):
            f.write("Community {}: {}\n".format(i+1, community))

    plt.savefig('graphes/graphe_cities_yearly.png')
    plt.show()

def execute_file(df_lots, df_agents, df_buyers, df_suppliers):
    main_function(df_lots, df_agents, df_buyers, df_suppliers)