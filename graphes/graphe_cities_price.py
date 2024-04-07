import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import community as comm_louvain

def main_function(df_lots, df_agents, df_buyers, df_suppliers):

    '''Prepare data'''
    # Sample lots
    df_lots = df_lots.dropna(subset=['awardPrice'])
    sampled_lots_df = df_lots.sample(n=100000)
    sampled_lots_df['awardPrice'] = pd.to_numeric(sampled_lots_df['awardPrice'], errors='coerce')
    median_price = sampled_lots_df['awardPrice'].median()

    # Merge
    merged_df = pd.merge(sampled_lots_df, df_buyers, on='lotId', suffixes=('', '_buyers'))
    merged_df.rename(columns={'agentId': 'buyersId'}, inplace=True)
    merged_df = pd.merge(merged_df, df_suppliers, on='lotId', suffixes=('', '_suppliers'))
    merged_df.rename(columns={'agentId': 'suppliersId'}, inplace=True)

    merged_df = merged_df[merged_df['lotId'].isin(sampled_lots_df['lotId'])]

    # Keep only the top 20 cities
    city_counts = df_agents['city'].value_counts()
    top_cities = city_counts.head(20).index
    print(top_cities)
    sampled_df_agents = df_agents[df_agents['city'].isin(top_cities)]

    G = nx.Graph()

    edge_thickness = {}  # Dictionary to store edge thickness

    for index, row in sampled_df_agents.iterrows():
        G.add_node(row['city'])

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
            edge = (agent_suppliers_city, agent_buyers_city)
            if edge in edge_thickness:
                edge_thickness[edge] += 0.005*row['awardPrice']/median_price
            else:
                edge_thickness[edge] = 0.005*row['awardPrice']/median_price

    for edge, thickness in edge_thickness.items():
        G.add_edge(edge[0], edge[1], weight=thickness) 

    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, node_size=30, node_color='red')

    # Draw edges
    light_magenta = (1.0, 0.5, 1.0)
    nx.draw_networkx_edges(G, pos, width=[d['weight'] for u, v, d in G.edges(data=True)], edge_color=light_magenta)

    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=8, font_color='black')

    # Community detection using Louvain method
    best_partition = comm_louvain.best_partition(G, weight='weight', resolution=1.0)  # Weighted community detection

    with open('graphes/cities_price_communities.txt', 'w') as f:
        f.write("Communities:\n")
        for i, community in enumerate(best_partition):
            f.write("Community {}: {}\n".format(i+1, community))

    plt.title("Sommes d'argent écchangées entre les villes")
    plt.savefig('graphes/graphe_cities_price.png')
    #plt.show()

def execute_file(df_lots, df_agents, df_buyers, df_suppliers):
    main_function(df_lots, df_agents, df_buyers, df_suppliers)