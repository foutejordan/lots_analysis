import pandas as pd

import analyse1
import analyse_bivarie1
import os

import analyse_bivariee_manon
import analyse_univariee_manon
import cpv_single_var
import single_var_agents
import single_var_lots
import two_variables_analysis_award_dates
from analyse_bivariee_manon import anova

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

qualitatives_path = os.path.join(BASE_DIR, 'lots_analysis', 'descriptive_analysis', 'figs', 'bivarie', '2qualitatives', 'Lots')
quantitatives_path = os.path.join(BASE_DIR, 'lots_analysis', 'descriptive_analysis', 'figs', 'bivarie', '2quantitatives', 'Lots')
quantitativeVSqualitative_path = os.path.join(BASE_DIR, 'lots_analysis', 'descriptive_analysis', 'figs', 'bivarie',
                                              'quantitativeVSqualitative')

univarie_path = os.path.join(BASE_DIR,'lots_analysis', 'descriptive_analysis', 'figs', 'univarie', 'Lots')

df_lots_cleaned = pd.read_csv('data/Lots_cleaned.csv')
df_agents_cleaned = pd.read_csv('data/Agents_cleaned.csv')
df_suppliers_cleaned = pd.read_csv('data/LotSuppliers_cleaned.csv')
df_buyers_cleaned = pd.read_csv('data/LotBuyers_cleaned.csv')
df_criteria_cleaned = pd.read_csv('data/Criteria_cleaned.csv')
df_names_cleaned = pd.read_csv('data/Names_cleaned.csv')


def execute():
    single_var_agents.execute_file(df_agents_cleaned, is_cleaned_data=True)
    single_var_lots.execute_file(df_lots_cleaned, is_cleaned_data=True)
    cpv_single_var.execute_file(df_lots_cleaned, is_cleaned_data=True)

    two_variables_analysis_award_dates.execute_file(df_lots_cleaned, is_cleaned_data=True)
    analyse_bivarie1.execute_file(df_lots_cleaned, qualitatives_path, quantitatives_path)
    analyse1.execute_file(df_lots_cleaned, univarie_path)

    analyse_univariee_manon.execute_file(df_lots_cleaned, df_buyers_cleaned, df_suppliers_cleaned, df_criteria_cleaned,
                                         df_names_cleaned, is_cleaned_data=True)
    analyse_bivariee_manon.execute_file(df_lots_cleaned, is_cleaned_data=True)


if __name__ == '__main__':
    execute()
