import pandas as pd


def main_function(old_df_lots_copy):
    new_df_lots = old_df_lots_copy
    prev = None

    for i, row in new_df_lots.iterrows():
        date = row['awardDate']
        if pd.isnull(date):
            new_df_lots.at[i, 'awardDate'] = prev
        else:
            prev = date

    return new_df_lots


def execute_file(old_df_lots):
    new_df_lots = main_function(old_df_lots)
    return new_df_lots
