from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
import statsmodels.formula.api as smf
import statsmodels.api as sm
import seaborn as sns
from spicy import stats

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    if not pd.isnull(distance):
        return int(distance)
    return None

def verif_anova(data, xName, yName):
    #colonne x quantitative, colonne y qualitative
    
    data_anova = data[[yName, xName]].dropna()

    groupes = data_anova[yName].unique()
    variances = []
    for groupe in groupes:
        variances.append(data_anova[data_anova[yName] == groupe][xName].var())

    p_value_levene = stats.levene(*[data_anova[data_anova[yName] == groupe][xName] for groupe in groupes])[1]

    p_value_shapiro = stats.shapiro(data_anova[xName])[1]

    return p_value_levene > 0.05 and p_value_shapiro > 0.05

def anovaOrKruskal(xName, yName, allData, f):
    #code taken from https://openclassrooms.com/fr/courses/7410486-nettoyez-et-analysez-votre-jeu-de-donnees/7428558-analysez-une-variable-quantitative-et-une-qualitative-par-anova
    #colonne x quantitative, colonne y qualitative
    
   print(verif_anova(allData, yName, xName))
   if verif_anova(allData, yName, xName) :
       f.write(f"\nANOVA results for {xName}:\n")
       anova = smf.ols(xName+'~'+yName, data=allData).fit()
       #print(sm.stats.anova_lm(anova, typ=2))
       print(sm.stats.anova_lm(anova))
   else :
       f.write(f"\nKRUSKAL results for {xName}:\n")
       data = allData[[yName, xName]].dropna()
       F, p = stats.kruskal(*[group[xName].values for name, group in data.groupby(yName)])  
       f.write(f"\nF:  {F}, p : {p}:\n")
       print(F, p)
       return p 

def graph_violin(colonne_x, colonne_y, name_x, name_y):
    #colonne_x qualitative, colonne_y quantitative
    
    plt.figure(figsize=(10, 6))
    
    sns.violinplot(x=colonne_x, y=colonne_y)
    plt.ylim(0, 1000) 
    
    #plt.yscale('log')
    
    plt.title('Diagramme en violon - '+name_y+' par '+name_x)
    plt.xlabel(name_x)
    plt.ylabel(name_y)
    plt.savefig('questionnements/distance/distance_by_'+name_x+'.png')
    #plt.show()

def main_function(df_suppliers, df_buyers, df_agents, df_lots):
    df_merged = pd.merge(df_suppliers, df_buyers, on='lotId', suffixes=('_supplier', '_buyer'))

    df_merged.rename(columns={'agentId_supplier': 'agentSupplierId', 'agentId_buyer': 'agentBuyerId'}, inplace=True)

    df_suppliers_buyers = df_merged[['lotId', 'agentSupplierId', 'agentBuyerId']]

    df_locations_suppliers = pd.merge(df_suppliers_buyers, df_agents, left_on='agentSupplierId', right_on='agentId', suffixes=('_supplier', '_buyer'))

    df_locations_suppliers.rename(columns={'longitude': 'longitudeSupplier', 'latitude': 'latitudeSupplier'}, inplace=True)

    df_all_locations = pd.merge(df_locations_suppliers, df_agents, left_on='agentBuyerId', right_on='agentId', suffixes=('_supplier', '_buyer'))

    df_all_locations.rename(columns={'longitude': 'longitudeBuyer', 'latitude': 'latitudeBuyer'}, inplace=True)

    df_final = df_all_locations[['lotId', 'longitudeSupplier', 'latitudeSupplier', 'longitudeBuyer', 'latitudeBuyer']]

    df_final.loc[:, 'distance'] = df_all_locations.apply(lambda row: calculate_distance(float(row['latitudeSupplier']), float(row['longitudeSupplier']), float(row['latitudeBuyer']), float(row['longitudeBuyer'])), axis=1)
    distances = df_final['distance'].dropna()

    # Create bins with approximately 20 intervals
    bins = pd.cut(distances, bins=[0, 10, 50, 100, 200, 500, 1000, np.inf])

    # Count occurrences in each bin
    bin_counts = bins.value_counts().sort_index()

    # Plot bar graph
    plt.figure(figsize=(8, 4))
    bin_counts.plot(kind='bar', color='skyblue')
    plt.title('Distances between suppliers and buyers')
    plt.xlabel('Distance (km)')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right') 
    plt.tight_layout()
    plt.savefig('questionnements/distance/distances_distribution.png')
    #plt.show()

    df_lots_info = pd.merge(df_final, df_lots, on='lotId')

    quantitative_fields = ['awardPrice', 'numberTenders', 'lotsNumber', 
                            'contractDuration', 'publicityDuration']

    # Calculate Pearson correlation coefficient for each quantitative field
    correlations = {}
    for field in quantitative_fields:
        try:
            correlation = df_lots_info[['distance', field]].astype(float).corr().iloc[0, 1]
            correlations[field] = correlation
        except ValueError:
            print(f"Field '{field}' contains non-numeric values and cannot be converted to float. Skipping...")

    # Print correlations to file
    with open("questionnements/distance/distance_pearson_correlations.txt", "w") as file:
        file.write("Correlation between Distance and Quantitative Fields:\n")
        for field, correlation in correlations.items():
            file.write(f"{field}: {correlation}\n")

    # Select qualitative fields for ANOVA
    qualitative_fields = ['cpv', 'cancelled', 'onBehalf', 'jointProcurement', 
                        'fraAgreement', 'fraEstimated', 'outOfDirectives', 'contractorSme',
                        'subContracted', 'gpa', 'multipleCae', 'typeOfContract', 
                        'topType', 'renewal'] 

    # Make a copy of the original DataFrame
    encoded_df = df_lots_info[['distance'] + qualitative_fields].copy()

    # Handle missing values in the 'distance' column
    imputer = SimpleImputer(strategy='mean')
    encoded_df['distance'] = imputer.fit_transform(encoded_df[['distance']])

    with open("questionnements/distance_anova.txt", "w") as f:
        # Perform ANOVA for each combination of quantitative and qualitative fields
        for qualitative_field in qualitative_fields:
            kruskal_p = anovaOrKruskal(qualitative_field, 'distance', encoded_df, f)
            if kruskal_p < 0.05:
                graph_violin(encoded_df[qualitative_field], encoded_df['distance'], qualitative_field, 'Distance')

def execute_file():
    df_suppliers = pd.read_csv('data/LotSuppliers_cleaned.csv', dtype=str)
    df_agents = pd.read_csv('data/Agents_cleaned.csv', dtype=str)
    df_buyers = pd.read_csv('data/LotBuyers_cleaned.csv', dtype=str)
    df_lots = pd.read_csv('data/Lots_cleaned_new_cpv.csv', dtype=str)
    main_function(df_suppliers, df_buyers, df_agents, df_lots)