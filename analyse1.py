import pandas as pd
import numpy as np
import os



import matplotlib.pyplot as plt
import seaborn as sns
# function to display histogram, boxplot and log histogram
def display_hist_box_loghist(df, column, path):
    plt.figure(figsize=(10,5))
    plt.hist(df[column], bins=30, color='green', alpha=0.7)
    plt.title(f'Histogram - {column}')
    plt.savefig(f'{path}/Histogram_{column}.png')
    # plt.show()

    df[f'{column}_log'] = np.log1p(df[column])
    plt.figure(figsize=(10,5))
    plt.hist(df[f'{column}_log'], bins=30, color='blue', alpha=0.7)
    plt.title(f'Histogram - Log of {column}')
    plt.savefig(f'{path}/Log_Histogram_{column}.png')
    # plt.show()

    plt.figure(figsize=(10,5))
    sns.boxplot(df[column])
    plt.title(f'Box plot - {column}')
    plt.savefig(f'{path}/Boxplot_{column}.png')
    # plt.show()

# function to display bar plot for categorical variables
def display_barplot(df, column, path):
    cat_counts = df[column].value_counts(dropna=False)
    # Calculez les pourcentages
    total_count = len(df[column])
    percentage_values = cat_counts / total_count * 100
    colors = ['gray','green', 'blue']
    plt.figure(figsize=(10,5))
    bars = cat_counts.plot(kind='bar', color=colors)

    # Ajoutez les pourcentages au-dessus de chaque barre
    for bar, percentage in zip(bars.patches, percentage_values):
        plt.text(bar.get_x() + bar.get_width() / 2 - 0.1, bar.get_height() + 0.05,
                 f'{percentage:.2f}%', ha='center', va='bottom', color='black', fontsize=10)
    plt.title(f'Bar plot - {column}')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.savefig(f'{path}/lots_{column}.png')



def execute_file(df_lots, univarie_path):
    # Create a list of numerical variables
    num_vars = ['awardEstimatedPrice', 'awardPrice', 'numberTenders','numberTendersSme', 'lotsNumber']

    # Create a list of categorical variables
    cat_vars = ['fraEstimated', 'typeOfContract', 'cpv_name', 'onBehalf', 'jointProcurement', 'fraAgreement', 'outOfDirectives', 'gpa', 'multipleCae', 'contractorSme']

    for col in num_vars:
        print(f'Processing {col}')
        df_lots[col] = pd.to_numeric(df_lots[col], errors='coerce')

        print(df_lots[col].describe())
        display_hist_box_loghist(df_lots, col, univarie_path)

    for col in cat_vars:
        print(f' categorical Processing {col}')
        display_barplot(df_lots, col, univarie_path)
        # metrics for categorical variables
        print(df_lots[col].value_counts(normalize=True) * 100)