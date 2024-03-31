import pandas as pd

def main_function(old_df_agents_copy):

    new_df_agents = old_df_agents_copy

    chunk_size = 1000  
    df_chunks = pd.read_csv('data/SIREN-StockEtablissementS4F3_utf8.csv', chunksize=chunk_size)
    for chunk in df_chunks:

        # Concatenate address columns in df_siren
        chunk['address'] = chunk['numeroVoieEtablissement'].astype(str) + ' ' + \
                                    chunk['typeVoieEtablissement'] + ' ' + \
                                    chunk['libelleVoieEtablissement']

        # Iterate over rows in df_siren
        for index, row in new_df_agents.iterrows():
            # If address is missing
            if pd.isnull(row['address']):
                matching_rows = chunk[((chunk['siret'].astype(str) == str(row['siret'])))]

                if not matching_rows.empty:
                    new_df_agents.at[index, 'address'] = matching_rows['address'].values[0]
                    new_df_agents.at[index, 'zipcode'] = matching_rows['codePostalEtablissement'].values[0]

        pass

    return new_df_agents

def execute_file(old_df_agents):
    new_agents = main_function(old_df_agents.copy())
    return new_agents