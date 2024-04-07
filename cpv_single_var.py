import pandas as pd
import matplotlib.pyplot as plt

categories = {
    77: 'Agriculture et espaces verts',
    32: 'Appareils radio, télévision, communication, télécommunication',
    31: 'Appareils, équipements, consommables électriques et d’éclairage',
    92: 'Arts, spectacle, divertissements, sport',
    98: 'Autres services communautaires, sociaux et personnels',
    41: 'Eau collectée et purifiée',
    80: 'Education et formation',
    9: 'Energie, gaz, fluides et services connexes',
    90: 'Environnement, eau, assainissement, propreté',
    35: 'Equipement de sécurité, lutte contre l’incendie, police et défense',
    34: 'Equipement de transport et produits auxiliaires pour le transport',
    43: 'Equipement minier et carrières, matériel de construction',
    38: 'Equipements de laboratoire, d’optique et de précision',
    79: 'Etudes, conseil, services aux entreprises',
    14: 'Exploitation minière et minerais',
    22: 'Imprimés et produits connexes',
    37: 'Instruments de musique, articles de sport, jeux, artisanat, arts',
    48: 'Logiciels et systèmes d’information',
    16: 'Machines agricoles',
    42: 'Machines industrielles',
    30: 'Machines, matériel et fourniture informatique et de bureau',
    44: 'Matériaux et structures de construction, produits pour la construction',
    33: 'Matériels médicaux, pharmaceutiques, produits de soins personnels',
    39: 'Meubles, aménagements, électroménager, produits de nettoyage',
    3: 'Produits agricoles, élevage, pêche, sylviculture et connexes',
    15: 'Produits alimentaires, boissons, tabac et produits connexes',
    24: 'Produits chimiques',
    19: 'Produits cuir et textiles, plastique, caoutchouc',
    55: 'Service d’hébergement et de restauration',
    63: 'Services d’appui dans les transports, services des agences de voyage',
    71: 'Services d’architecture, de construction, d’ingénierie et d’inspection',
    75: 'Services de l’administration publique, défense, sécurité sociale',
    73: 'Services de R&D, services de conseil connexes',
    50: 'Services de réparation et d’entretien',
    85: 'Services de santé et d’action sociale',
    72: 'Services de technologies de l’information, conseil, développement de logiciels, internet et appui',
    60: 'Services de transport (à l’exclusion du transport des déchets)',
    64: 'Services des postes et télécommunications',
    51: 'Services d’installation',
    66: 'Services financiers et d’assurance',
    70: 'Services immobiliers',
    65: 'Services publics',
    76: 'Services relatifs à l’industrie du pétrole et du gaz',
    45: 'Travaux de construction, BTP',
    18: 'Vêtements, articles chaussants, bagages et accessoires'
}


def build_csv(df_lots_copy, is_cleaned_data):
    # Count the occurrences of each cpv categories (first two numbers)
    df_lots_copy['cpv'] = df_lots_copy['cpv'].astype(str).str[:2]
    cpv_counts = df_lots_copy['cpv'].value_counts()

    # Calculate statistical measures
    mean_occurrences = cpv_counts.mean()
    std_dev_occurrences = cpv_counts.std()
    quantiles_occurrences = cpv_counts.quantile([0.25, 0.5, 0.75])
    min_occurrences = cpv_counts.min()
    max_occurrences = cpv_counts.max()

    # Write statistical measures to a file
    path = ''
    if is_cleaned_data:
        path = '../descriptive_analysis/figs/univarie/Lots/'
    else:
        path = 'figs/univarie/Lots/'
    with open(path + 'cpv_statistics.txt', 'w') as file:
        file.write(f"Mean: {mean_occurrences}\n")
        file.write(f"Standard Deviation: {std_dev_occurrences}\n")
        file.write(f"Quantiles:\n{quantiles_occurrences}\n")
        file.write(f"Min: {min_occurrences}\n")
        file.write(f"Max: {max_occurrences}\n")

    # Write each cpv along with its count to a file
    with open(path + 'cpv_nb_of_appearances.csv', 'w') as file:
        for cpv, count in cpv_counts.items():
            print(f"{cpv}, {count}", file=file)


def get_nom_cpv(numero):
    try:
        numero = int(numero)
        return categories.get(numero, None)
    except ValueError:
        return None


def replace_numbers_by_names_csv(is_cleaned_data):
    path = ''
    if is_cleaned_data:
        path = '../descriptive_analysis/figs/univarie/Lots/'
    else:
        path = 'figs/univarie/Lots/'
    df = pd.read_csv(path + "cpv_nb_of_appearances.csv", header=None)
    df["cpv"] = df.iloc[:, 0].apply(get_nom_cpv)
    df = df.drop(columns=[0])
    df = df[[df.columns[-1]] + list(df.columns[:-1])]
    df = df.dropna(subset=["cpv"])

    df.to_csv(path + "cpv_categories.csv", index=False, header=False)


def draw_graph(is_cleaned_data):
    path = ''
    if is_cleaned_data:
        path = '../descriptive_analysis/figs/univarie/Lots/'
    else:
        path = 'figs/univarie/Lots/'
    df_final = pd.read_csv(path + 'cpv_categories.csv', header=None)
    plt.figure(figsize=(30, 15))
    plt.bar(df_final[0], df_final[1], color='skyblue')
    plt.title('Category from CPV by Occurrence')
    plt.xlabel('Categories')
    plt.ylabel('Number of Occurrences')
    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.savefig(path + 'cpv_categories_count.png')
    #plt.show()


def execute_file(df_lots, is_cleaned_data):
    build_csv(df_lots.copy(), is_cleaned_data)
    replace_numbers_by_names_csv(is_cleaned_data)
    draw_graph(is_cleaned_data)
