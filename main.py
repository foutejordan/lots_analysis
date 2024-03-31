import pandas as pd
import analyse_bivarie1
import single_var_agents
import two_variables_analysis_award_dates
import cpv_single_var
import single_var_lots
import nettoyage.add_to_agents_from_siren
import nettoyage.dates

df_lots = pd.read_csv('data/Lots.csv', dtype=str)
df_lots['cpv_name'] = df_lots['cpv'].astype(str).str[:2]

df_agents = pd.read_csv('data/Agents.csv')

if __name__ == '__main__':
    analyse_bivarie1.execute_file(df_lots)
    single_var_agents.execute_file(df_agents)
    single_var_lots.execute_file(df_lots)
    cpv_single_var.execute_file(df_lots)
    two_variables_analysis_award_dates.execute_file()

    '''Nettoyage'''
    #Laisser commenter
    #df_agents_siret = nettoyage.add_to_agents_from_siren.execute_file(df_agents)
    df_lots_dates = nettoyage.dates.execute_file(df_lots)

    
