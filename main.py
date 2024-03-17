import pandas as pd
import analyse_bivarie1
import single_var_agents

df_lots = pd.read_csv('data/Lots.csv', dtype=str)
df_lots['cpv_name'] = df_lots['cpv'].astype(str).str[:2]

df_agents = pd.read_csv('data/Agents.csv')

#
if __name__ == '__main__':
    analyse_bivarie1.execute_file(df_lots)
    single_var_agents.execute_file(df_agents)
