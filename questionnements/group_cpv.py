import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('../figs/lots_stats/cpv_nb_of_appearances.csv', header=None, names=['CPV', 'Count'])

# Categories ordered 
categories = {
    "03": "Produits agricoles, élevage, pêche, sylviculture et connexes",
    "09": "Energie, gaz, fluides et services connexes",
    "14": "Exploitation minière et minerais",
    "15": "Produits alimentaires, boissons, tabac et produits connexes",
    "16": "Machines agricoles",
    "18": "Vêtements, articles chaussants, bagages et accessoires",
    "19": "Produits cuir et textiles, plastique, caoutchouc",
    "22": "Imprimés et produits connexes",
    "24": "Produits chimiques",
    "30": "Machines, matériel et fourniture informatique et de bureau",
    "31": "Appareils, équipements, consommables électriques et d’éclairage",
    "32": "Appareils radio, télévision, communication, télécommunication",
    "33": "Matériels médicaux, pharmaceutiques, produits de soins personnels",
    "34": "Equipement de transport et produits auxiliaires pour le transport",
    "35": "Equipement de sécurité, lutte contre l’incendie, police et défense",
    "37": "Instruments de musique, articles de sport, jeux, artisanat, arts",
    "38": "Equipements de laboratoire, d’optique et de précision",
    "39": "Meubles, aménagements, électroménager, produits de nettoyage",
    "41": "Eau collectée et purifiée",
    "42": "Machines industrielles",
    "43": "Equipement minier et carrières, matériel de construction",
    "44": "Matériaux et structures de construction, produits pour la construction",
    "45": "Travaux de construction, BTP",
    "48": "Logiciels et systèmes d’information",
    "50": "Services de réparation et d’entretien",
    "51": "Services d’installation",
    "55": "Service d’hébergement et de restauration",
    "60": "Services de transport (à l’exclusion du transport des déchets)",
    "63": "Services d’appui dans les transports, services des agences de voyage",
    "64": "Services des postes et télécommunications",
    "65": "Services publics",
    "66": "Services financiers et d’assurance",
    "70": "Services immobiliers",
    "71": "Services d’architecture, de construction, d’ingénierie et d’inspection",
    "72": "Services de technologies de l’information, conseil, développement de logiciels, internet et appui",
    "73": "Services de R&D, services de conseil connexes",
    "75": "Services de l’administration publique, défense, sécurité sociale",
    "76": "Services relatifs à l’industrie du pétrole et du gaz",
    "77": "Agriculture et espaces verts",
    "79": "Etudes, conseil, services aux entreprises",
    "80": "Education et formation",
    "85": "Services de santé et d’action sociale",
    "90": "Environnement, eau, assainissement, propreté",
    "92": "Arts, spectacle, divertissements, sport",
    "98": "Autres services communautaires, sociaux et personnels"
}

total = df['Count'].sum()

NB_CATEGORIES = 5

groups = []

sub_total = 0
sub_group = []

for key, value in categories.items():
    print(f"Processing key: {key}")
    cpv_count = df.loc[df['CPV'] == key, 'Count'].values
    print(f"cpv_count: {cpv_count}")
    if len(cpv_count) > 0:
        cpv_count = cpv_count[0]
    else:
        cpv_count = 0

    sub_group.append((key, value))
    if sub_total + cpv_count < total / NB_CATEGORIES + 1:
        sub_total += cpv_count
    else:
        groups.append(sub_group)
        sub_total = 0
        sub_group = []

# Creates the last group
if sub_group:
    groups.append(sub_group)

# Calculate the sum of values for each group
sums_per_group = []
for group in groups:
    group_sum = 0
    for key, _ in group:
        cpv_sum = df.loc[df['CPV'] == key, 'Count'].sum()
        group_sum += cpv_sum
    sums_per_group.append(group_sum)

# Print the groups and their corresponding sums
for i, (group, group_sum) in enumerate(zip(groups, sums_per_group)):
    print(f"Group {i + 1}:")
    for key, category in group:
        print(f"{key} - {category}")
    print(f"Sum: {group_sum}\n")