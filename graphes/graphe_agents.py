import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def main_function(df_lots, df_agents, df_buyers, df_suppliers):

    sampled_agents_df = df_agents[df_agents['department'] == '15']

    merged_df = pd.merge(df_suppliers, df_buyers, on='lotId', suffixes=('_suppliers', '_buyers'))

    # Create a new empty graph
    G = nx.Graph()

    for index, row in sampled_agents_df.iterrows():
        G.add_node(row['agentId'])

    # Iterate through the merged dataframe and create edges between agents
    for index, row in merged_df.iterrows():
        agent_suppliers = row['agentId_suppliers']
        agent_buyers = row['agentId_buyers']
        lot_id = row['lotId']
        
        # Check if the agents are different
        if agent_suppliers != agent_buyers and G.has_node(agent_buyers) and agent_suppliers != agent_buyers: 
            # Add an edge between the agents if they are associated with the same lot
            G.add_edge(agent_suppliers, agent_buyers, lot_id=lot_id)

    # Step 4: Visualize (optional)
    pos = nx.spring_layout(G)
    # Draw only nodes with at least one connection and without labels
    nx.draw(G, pos, with_labels=False, nodelist=[node for node, degree in dict(G.degree()).items() if degree > 0], node_size=30, node_color='skyblue')

    plt.title('Graph Representation of CSV Data')
    plt.show()

def execute_file(df_lots, df_agents, df_buyers, df_suppliers):
    main_function(df_lots, df_agents, df_buyers, df_suppliers)