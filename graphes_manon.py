# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 11:42:48 2024

@author: pikam
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt


def verif_path(entire_path):
    path = Path(entire_path)
    
    directory = path.parent
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)


def graphe(num_departement):
    df_extend = pd.read_csv('data/extended_categorieEntreprise_agents.csv', header=0, sep=',', dtype=str)
    df_extend = df_extend.drop_duplicates(subset=['agentId'])
        
    df_agents = pd.read_csv('data/Agents_cleaned.csv', header=0, sep=',', dtype=str)
    df_agents = df_agents.loc[(df_agents['department'] == num_departement) ] 

    df_suppliers = pd.read_csv('data/LotSuppliers_cleaned.csv', header=0, sep=',', dtype=str)

    df = df_agents.merge(df_suppliers, on='agentId', how='inner')
    df_final = df.merge(df_extend, on='agentId', how='inner')
    
    
    
    category_colors = {
        'PME': 'blue',
        'ETI': 'green',
        'GE': 'red'
    }
    
    agent_category_map = dict(zip(df_final['agentId'], df_final['categorieEntreprise']))
    
    G = nx.Graph()
    
    agents = df_final['agentId'].tolist()
    print(len(agents))
    G.add_nodes_from(agents)
    
    agent_lot = {}
    for index, row in df_final.iterrows():
        if row['agentId'] in agent_lot:
            agent_lot[row['agentId']].append(row['lotId'])
        else:
            agent_lot[row['agentId']] = [row['lotId']]
    
    for idx1, (agent1, lots1) in enumerate(agent_lot.items()):
        for idx2, (agent2, lots2) in enumerate(agent_lot.items()):
            if idx1 < idx2:
                nb_communs = sum(1 for lot in lots1 if lot in lots2)
                if nb_communs > 0:  
                    G.add_edge(agent1, agent2, weight=nb_communs)
    
    nodes_with_edges = [node for node in G.nodes() if any(weight != 0 for _, _, weight in G.edges(node, data='weight'))]
    subgraph = G.subgraph(nodes_with_edges)
    print("Nombre d'arêtes :", subgraph.number_of_edges())

    
    node_colors = [category_colors[agent_category_map[agent]] for agent in subgraph.nodes()]
    
    plt.figure(figsize=(10, 8))
    pos = nx.fruchterman_reingold_layout(subgraph, scale=1)  # Layout du sous-graphe
    nx.draw(subgraph, pos, node_color=node_colors, with_labels=False, edge_color='black', node_size=100)
    
    plt.title("Graphe des agents du "+num_departement+" liés par un même lot et coloré en fonction de la catégorie d'entreprise")
    
    entire_path = 'figs/Graphe_agents_'+num_departement+'.png'
    verif_path(entire_path)
    plt.savefig(entire_path)
    #plt.show()

    

    
    
    
    





def execute_file():
    graphe("84")
    graphe("75")
    
    
    
execute_file()