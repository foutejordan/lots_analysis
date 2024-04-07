import pandas as pd
import analyse_bivarie1
import analyse1
from nettoyage import data_cleaning
import single_var_agents
import two_variables_analysis_award_dates
import cpv_single_var
import single_var_lots
import nettoyage.dates
import analyse_bivariee_manon
import analyse_univariee_manon
import nettoyage.nettoyage_manon
import os
import descriptive_analysis.main
from questionnements import questionnement_manon
from graphes import graphes_manon
import questionnements.cpv_stats
import questionnements.distance
import questionnements.domains_location
import graphes.graphe_cities
import graphes.graphe_cities_price
import graphes.graphe_cities_date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

qualitatives_path = os.path.join(BASE_DIR, 'lots_analysis', 'figs', 'bivarie', '2qualitatives', 'Lots')
quantitatives_path = os.path.join(BASE_DIR, 'lots_analysis', 'figs', 'bivarie', '2quantitatives', 'Lots')
quantitativeVSqualitative_path = os.path.join(BASE_DIR, 'lots_analysis', 'figs', 'bivarie', 'quantitativeVSqualitative')

univarie_path = os.path.join(BASE_DIR, 'lots_analysis', 'figs', 'univarie', 'Lots')

df_lots = pd.read_csv('data/Lots.csv', dtype=str, )
for i, row in df_lots.iterrows():
    if not pd.isna(row['cpv']):
        df_lots.at[i, 'cpv_name'] = str(row['cpv'])[:2]

df_agents = pd.read_csv('data/Agents.csv')
df_suppliers = pd.read_csv('data/LotSuppliers.csv')
df_buyers = pd.read_csv('data/LotBuyers.csv')
df_criteria = pd.read_csv('data/Criteria.csv')
df_names = pd.read_csv('data/Names.csv')

if __name__ == '__main__':
    analyse_univariee_manon.execute_file(df_lots, df_buyers, df_suppliers, df_criteria, df_names, is_cleaned_data=False)
    analyse_bivariee_manon.execute_file(df_lots, is_cleaned_data=False)

    analyse_bivarie1.execute_file(df_lots, qualitatives_path, quantitatives_path)
    analyse1.execute_file(df_lots, univarie_path)
    single_var_agents.execute_file(df_agents, is_cleaned_data=False)
    single_var_lots.execute_file(df_lots, is_cleaned_data=False)
    cpv_single_var.execute_file(df_lots, is_cleaned_data=False)
    two_variables_analysis_award_dates.execute_file(df_lots, is_cleaned_data=False)

    '''Nettoyage'''
    #Laisser commenté
    #df_agents_siret = nettoyage.add_from_siren.execute_file(df_agents)

    df_lots, new_agents_df, new_criteria_df, new_lotbuyers_df, new_lotsuppliers_df, new_names_df = nettoyage.nettoyage_manon.execute_file()
    df_lots = data_cleaning.clean_data(df_lots)
    print("end imputer", df_lots['awardDate'].head(10))
    df_lots = nettoyage.dates.execute_file(df_lots.reset_index())

    df_lots.to_csv('data/Lots_cleaned.csv', index=False)
    new_agents_df.to_csv('data/Agents_cleaned.csv', index=False)
    new_criteria_df.to_csv('data/Criteria_cleaned.csv', index=False)
    new_lotbuyers_df.to_csv('data/LotBuyers_cleaned.csv', index=False)
    new_lotsuppliers_df.to_csv('data/LotSuppliers_cleaned.csv', index=False)
    new_names_df.to_csv('data/Names_cleaned.csv', index=False)

    '''Descriptive analysis'''

    descriptive_analysis.main.execute()

    '''Questionnement'''

    print("Questionnement")
    df_suppliers_cleaned = pd.read_csv('data/LotSuppliers_cleaned.csv', dtype=str)
    df_agents_cleaned = pd.read_csv('data/Agents_cleaned.csv', dtype=str)
    df_buyers_cleaned = pd.read_csv('data/LotBuyers_cleaned.csv', dtype=str)
    df_lots_cleaned = pd.read_csv('data/Lots_cleaned.csv', dtype=str)

    print("Questionnement Manon")
    # questionnement_manon.execute_file()

    print("Questionnement Maxime")
    # questionnements.cpv_stats.execute_file(df_lots_cleaned)

    print("Questionnement Domains Location")
    df_lots_new_cpv = pd.read_csv('data/Lots_cleaned_new_cpv.csv', dtype=str)
    # questionnements.domains_location.execute_file(df_suppliers_cleaned, df_agents_cleaned, df_lots_new_cpv)

    print("Questionnement Distance")
    questionnements.distance.execute_file()

    '''Graphes'''

    print("Graphes Manon")
    graphes_manon.execute_file()

    print("Graphes Maxime")
    graphes.graphe_cities.execute_file(df_lots_cleaned, df_agents_cleaned, df_buyers_cleaned, df_suppliers_cleaned)

    print("Graphes Maxime Price")
    graphes.graphe_cities_price.execute_file(df_lots_cleaned, df_agents_cleaned, df_buyers_cleaned,
                                             df_suppliers_cleaned)

    print("Graphes Maxime Date")
    graphes.graphe_cities_date.execute_file(df_lots_cleaned, df_agents_cleaned, df_buyers_cleaned, df_suppliers_cleaned)
