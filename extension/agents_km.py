import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA


def find_total_buyers():
    lot_buyers = pd.read_csv("../data/LotBuyers.csv")
    # Charger les données des fournisseurs
    lot_suppliers = pd.read_csv("../data/LotSuppliers.csv")

    # Compter le nombre total d'achats par fournisseur
    total_achats_par_fournisseur = lot_buyers.groupby('agentId').size().reset_index(name='Total Achat')

    # Compter le nombre total de ventes par fournisseur
    total_ventes_par_fournisseur = lot_suppliers.groupby('agentId').size().reset_index(name='Total Vente')

    # Fusionner les deux résultats
    result = pd.merge(total_achats_par_fournisseur, total_ventes_par_fournisseur, on='agentId', how='outer')
    print(result)

    # return a dataframe
    return result


def build_dataset():
    extended_agents = pd.read_csv('../data/extended_agents.csv')
    # merge the data with the total buyers
    result = find_total_buyers()
    # merge the data with the extended agents
    result = pd.merge(result, extended_agents, on='agentId', how='inner')
    # drop the agentId column
    result = result.drop(
        columns=['agentId', 'name', 'siret', 'address', 'city', 'zipcode', 'country', 'department', 'longitude',
                 'latitude', 'siren'])
    result['etatAdministratifEtablissement'] = result['etatAdministratifEtablissement'].fillna('A')
    result['codeCommuneEtablissement'] = result['codeCommuneEtablissement'].fillna('Etr')
    result['Total Achat'] = result['Total Achat'].fillna(0)
    result['Total Vente'] = result['Total Vente'].fillna(0)

    # drop the rows with NaN values
    result = result.dropna()
    # switch object columns to string
    for column in result.columns:
        if result[column].dtype == 'object':
            result[column] = result[column].astype(str)
    # save the data to a csv file
    result.to_csv('dataset.csv', index=False)
    # return result


def _show_elbow(data):
    from R_square_clustering import r_square
    # Plot elbow graphs for KMeans using R square and purity scores
    lst_k = range(2, 11)
    lst_rsq = []
    lst_purity = []
    for k in lst_k:
        est = KMeans(n_clusters=k, n_init='auto')
        est.fit(data.values)
        lst_rsq.append(r_square(data.values, est.cluster_centers_, est.labels_, k))

    fig = plt.figure()
    plt.plot(lst_k, lst_rsq, 'bx-')
    plt.xlabel('k')
    plt.ylabel('RSQ score')
    plt.title('The Elbow Method showing the optimal k')
    plt.savefig('figs/k-means_elbow_method')
    plt.close()

def _dendogram(data):
    from scipy.cluster.hierarchy import dendrogram, linkage
    linkage_matrix = linkage(data.values, 'ward')
    fig2 = plt.figure()
    dendrogram(
        linkage_matrix,
        color_threshold=0,
    )
    plt.title('Hierarchical Clustering Dendrogram (Ward)')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    plt.tight_layout()
    plt.savefig('figs/hierarchical-clustering.png')
    plt.close()


def _kmeans(data):
    kmeans = KMeans(n_clusters=10)
    kmeans.fit(data.values)

    # Ajouter les labels de cluster aux données
    data['cluster'] = kmeans.labels_

    # Réduction de dimensionnalité avec PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(data.values)

    # Créer un DataFrame pour les données réduites
    pca_df = pd.DataFrame(data=X_pca, columns=['PC1', 'PC2'])
    pca_df['cluster'] = kmeans.labels_

    # Visualisation des clusters
    plt.figure(figsize=(10, 6))

    # Boucle à travers chaque cluster et tracer les points correspondants
    for cluster in range(6):  # Nombre de clusters
        cluster_data = pca_df[pca_df['cluster'] == cluster]
        plt.scatter(cluster_data['PC1'], cluster_data['PC2'], label=f'Cluster {cluster}')

    # Tracer les centres de cluster
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='red', marker='X',
                label='Centres de cluster')

    # Ajouter les labels, titre et légende
    plt.xlabel('pca 1')
    plt.ylabel('pca 2')
    plt.title('Visualisation des clusters')
    plt.legend()
    plt.grid(True)

    # Sauvegarder le graphique
    plt.savefig('figs/clusters.png')

    cluster_means = data.groupby('cluster').mean()
    from scipy.stats import f_oneway
    # Comparer les moyennes des variables pour chaque cluster
    for column in data.columns:
        if column != 'cluster':
            # Créer une liste de groupes pour chaque cluster
            groups = [data[data['cluster'] == i][column] for i in range(6)]
            # Effectuer le test ANOVA
            f_stat, p_value = f_oneway(*groups)
            print(f'Résultats de ANOVA pour la caractéristique: {column}, p-value: {p_value}')

    cluster_stats = data.groupby('cluster').agg(
        {'Total Achat': ['mean', 'median', 'sum'], 'Total Vente': ['mean', 'median', 'sum']})

    # Renommer les colonnes pour plus de clarté
    cluster_stats.columns = ['Mean_Achat', 'Median_Achat', 'Total_Achat', 'Mean_Vente', 'Median_Vente', 'Total_Vente']

    # Afficher les statistiques descriptives pour les achats et les ventes dans chaque cluster
    with open('cluster_stats.txt', 'w') as f:
        f.write(cluster_stats.to_string())
    # Afficher le graphique
    plt.show()


def execute():
    # build_dataset()
    data = pd.read_csv('dataset.csv')
    from sklearn.preprocessing import LabelEncoder

    # label encoding for all columns with object or bool type
    le = LabelEncoder()
    for column in data.columns:
        if data[column].dtype == 'object':
            data[column] = le.fit_transform(data[column])

    _show_elbow(data)

    _dendogram(data)

    _kmeans(data)

if __name__ == '__main__':
    execute()
