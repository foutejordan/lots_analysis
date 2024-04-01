import pandas as pd
import analyse_bivarie1
import analyse1
import data_cleaning

df_lots = pd.read_csv('data/Lots.csv', dtype=str)
df_lots['cpv_name'] = df_lots['cpv'].astype(str).str[:2]

#
if __name__ == '__main__':
    analyse_bivarie1.execute_file(df_lots)
    analyse1.execute_file(df_lots)

    # nettoyage des données

    df_lots = data_cleaning.clean_data(df_lots)
