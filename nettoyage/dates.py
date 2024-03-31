import pandas as pd

def main_function(old_df_lots_copy):

    new_df_lots = old_df_lots_copy.copy()
    columns_to_parse = ['awardDate']

    new_df_lots[columns_to_parse] = new_df_lots[columns_to_parse].apply(pd.to_datetime)

    for i in range(1, len(new_df_lots)):
        if pd.isnull(new_df_lots.at[i, 'awardDate']):
            prev_date = new_df_lots.at[i-1, 'awardDate']
            next_date = new_df_lots.at[i+1, 'awardDate']
            average_date = prev_date + (next_date - prev_date) / 2
            
            # Replace the missing date with the average date
            new_df_lots.at[i, 'awardDate'] = average_date

    return new_df_lots


def execute_file(old_df_lots):
    new_df_lots = main_function(old_df_lots)
    return new_df_lots