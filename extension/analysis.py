import pandas as pd

# Charger les données des agents
extended_agents = pd.read_csv('../data/extended_agents.csv')

# Charger les données des fournisseurs associés aux lots
lots_suppliers = pd.read_csv("../data/LotBuyers.csv")

lots = pd.read_csv("../data/Lots_cleaned.csv")

import matplotlib.pyplot as plt


def execute():
    print("begin merge to suppliers")
    merged_data = pd.merge(lots_suppliers, extended_agents, left_on='agentId', right_on='agentId', how='left')

    print("counting foreign suppliers...")
    num_foreign_suppliers = merged_data[merged_data['codeCommuneEtablissement'].isnull()].shape[
        0]  # Entreprises étrangères

    total_suppliers = merged_data.shape[0]

    # Calculer la proportion des marchés publics allant à des entreprises étrangères

    print("calculating proportion of foreign suppliers...")
    proportion_foreign_suppliers = num_foreign_suppliers / total_suppliers

    print("Proportion des marchés publics allant à des entreprises étrangères :", proportion_foreign_suppliers)

    # Proportion des marchés publics allant à des entreprises locales
    proportion_local_suppliers = 1 - proportion_foreign_suppliers

    # Étiquettes pour les secteurs du graphique
    labels = ['Entreprises Étrangères', 'Entreprises Locales']

    # Valeurs des secteurs
    sizes = [proportion_foreign_suppliers, proportion_local_suppliers]

    # Couleurs des secteurs
    colors = ['#ff9999', '#66b3ff']

    # Création du graphique en secteurs
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90)

    # Ajout d'un cercle au centre pour s'assurer d'un aspect de pie-chart
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Aspect du graphique
    plt.axis('equal')
    plt.title('Proportion des marchés publics allant à des entreprises étrangères', y=1.08)

    # Sauvegarder le graphique
    plt.show()
    plt.savefig('figs/proportion_foreign_suppliers.png')

    # Fusionner les données des lots avec les caractéristiques des lots
    merged_data = pd.merge(merged_data, lots[['lotId', 'cpv_name']], left_on='lotId', right_on='lotId', how='left')
    # Compter le nombre de fournisseurs situés à l'étranger par secteur

    foreign_suppliers_by_sector = merged_data[merged_data['codeCommuneEtablissement'].isnull()].groupby(
        'cpv_name').size()
    # total_suppliers_by_sector = merged_data.groupby('cpv_name').size()

    proportion_foreign_suppliers_by_sector = foreign_suppliers_by_sector / foreign_suppliers_by_sector.sum()

    print("Proportion des fournisseurs étrangers par secteur :", proportion_foreign_suppliers_by_sector)

    # sauvegarder les données
    proportion_foreign_suppliers_by_sector.to_csv('proportion_foreign_suppliers_by_sector.csv')

    # Trier les données par ordre décroissant de la proportion étrangère
    data = pd.DataFrame(proportion_foreign_suppliers_by_sector, columns=['Proportion étrangère'])
    data = data.sort_values(by='Proportion étrangère', ascending=False)

    # Créer le graphique
    plt.figure(figsize=(14, 8))  # Ajustement de la taille de la figure
    bars = proportion_foreign_suppliers_by_sector.plot(kind='bar', color='skyblue')

    # Titre et labels
    plt.title('Proportion des fournisseurs étrangers par secteur')
    plt.xlabel('Secteur')
    plt.ylabel('Proportion')

    # Ajouter les pourcentages sur les barres
    for index, value in enumerate(proportion_foreign_suppliers_by_sector):
        plt.text(index, value, f'{value:.1%}', ha='center', va='bottom')

    # Afficher le graphique avec tous les secteurs
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    # Sauvegarder le graphique
    plt.savefig('figs/proportion_foreign_suppliers_by_sector.png')


if __name__ == '__main__':
    execute()
