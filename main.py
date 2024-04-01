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

df_lots = pd.read_csv('data/Lots.csv', dtype=str)
#df_lots['cpv_name'] = df_lots['cpv'].astype(str).str[:2]
for i, row in df_lots.iterrows():
        if not pd.isna(row['cpv']):
            df_lots.at[i, 'cpv_name'] = str(row['cpv'])[:2]

df_agents = pd.read_csv('data/Agents.csv')

if __name__ == '__main__':
    # analyse_univariee_manon.execute_file()
    # analyse_bivariee_manon.execute_file()

    # analyse_bivarie1.execute_file(df_lots)
    # analyse1.execute_file(df_lots)
    # single_var_agents.execute_file(df_agents)
    # single_var_lots.execute_file(df_lots)
    # cpv_single_var.execute_file(df_lots)
    # two_variables_analysis_award_dates.execute_file()

    '''Nettoyage'''
    #Laisser commenter
    #df_agents_siret = nettoyage.add_from_siren.execute_file(df_agents)

    #df_lots, new_agents_df, new_criteria_df, new_lotbuyers_df, new_lotsuppliers_df, new_names_df = nettoyage.nettoyage_manon.execute_file()

    df_lots = nettoyage.dates.execute_file(df_lots)
    df_lots = data_cleaning.clean_data(df_lots)

    df_lots.to_csv('data/Lots_cleaned.csv', index=False)
    # new_agents_df.to_csv('data/Agents_cleaned.csv', index=False)
    # new_criteria_df.to_csv('data/Criteria_cleaned.csv', index=False)
    # new_lotbuyers_df.to_csv('data/LotBuyers_cleaned.csv', index=False)
    # new_lotsuppliers_df.to_csv('data/LotSuppliers_cleaned.csv', index=False)
    # new_names_df.to_csv('data/Names_cleaned.csv', index=False)

    
