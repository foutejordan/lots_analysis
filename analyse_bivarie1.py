import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import seaborn as sns
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

qualitatives = os.path.join(BASE_DIR, 'Lots_analysis', 'figs', 'bivarie', '2qualitatives')
quantitatives = os.path.join(BASE_DIR, 'Lots_analysis', 'figs', 'bivarie', '2quantitatives')

def bool_switch(row):
    if row == 'N' or row == '0' or row == 0:
        return 0
    elif row == 'Y' or row == '1' or row == 1:
        return 1
    elif pd.isna(row):
        return 2
    else:
        return 2


def switch(row):
    if row == 'N' or row == '0' or row == 0:
        return 'False'
    elif row == 'Y' or row == '1' or row == 1:
        return 'True'
    elif pd.isna(row):
        return 'NAN'
    elif row == 'W':
        return 'W'
    elif row == 'U':
        return 'U'
    elif row == 'S':
        return 'S'
    else:
        return 'NAN'


def bool_categorical_bivariate(df, att1, att2):
    bool_list = ('N', 'Y', 'NAN')
    df[att1] = df[att1].apply(bool_switch).astype(int)
    df[att2] = df[att2].apply(bool_switch).astype(int)

    # select only numeric values

    # for each row, select numeric values and put them in a new dataframe
    df = df.select_dtypes(include=[np.number])

    print(df[att1].value_counts())

    value_counts_att1 = df[att1].value_counts()
    value_counts_att2 = df[att2].value_counts()

    for value in [0, 1, 2]:
        if value not in value_counts_att1.index:
            value_counts_att1[value] = 0
        if value not in value_counts_att2.index:
            value_counts_att2[value] = 0
    data = {
        att1: (value_counts_att1[0], value_counts_att1[1], value_counts_att1[2]),
        att2: (value_counts_att2[0], value_counts_att2[1], value_counts_att2[2])
    }
    x = np.arange(len(bool_list))
    width = 0.35
    multiplier = 0
    fig, ax = plt.subplots()

    for attribute, measurement in data.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    ax.set_ylabel('Frequency (mm)')
    ax.set_title('attributes')
    ax.set_xticks(x + width, bool_list)
    ax.legend(loc='upper left', ncols=2)
    ax.set_yscale('log')
    ax.set_ylim(0, max(max(value_counts_att1), max(value_counts_att2)) * 100)
    # plt.show()
    # save the plot
    plt.savefig(f'{qualitatives}/bool_{att1}_{att2}.png')

    return ax


def categorical_bivariate(df, att1, att2):
    # Group by att1 and att2, count occurrences, and reset index
    df_grouped = df.groupby([att1, att2]).size().reset_index(name='count')

    # Plot the barplot with hue
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_grouped, x=att1, y='count', hue=att2, palette='viridis')
    plt.yscale('log')

    plt.ylabel('Frequency (log scale)')
    plt.title(f'{att1} vs {att2}')
    # plt.show()
    # save the plot
    plt.savefig(f'{qualitatives}/{att1}_{att2}.png')


def cramers_v(confusion_matrix):
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))


def calculate_cramer_v(df, att1, att2):
    # Create a contingency table
    contingency_table = pd.crosstab(df[att1], df[att2])

    # Calculate Cramér's V
    v = cramers_v(contingency_table.values)

    return v


def create_cramer_v_heatmap(df, variables):
    correlations = pd.DataFrame(index=variables, columns=variables)

    for i in range(len(variables)):
        for j in range(i, len(variables)):
            att1, att2 = variables[i], variables[j]
            correlation_measure = calculate_cramer_v(df, att1, att2)
            correlations.loc[att1, att2] = correlation_measure
            correlations.loc[att2, att1] = correlation_measure

    # Create a square heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlations.astype(float), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Cramér's V Correlation Heatmap")
    # plt.show()
    # save the plot
    plt.savefig(f'{qualitatives}/cramer_v_heatmap.png')

def numeric_bivariate_scatter(df, num_var1, num_var2, num_bins=20):
    df_filtered = df[[num_var1, num_var2]].dropna()

    plt.figure(figsize=(10, 6))

    sns.scatterplot(data=df_filtered, x=num_var1, y=num_var2,
                    alpha=0.4)
    plt.title(f'Scatter Plot (log scale): {num_var1} vs {num_var2}')
    plt.xlabel(f'Log({num_var1})')
    plt.ylabel(f'Log({num_var2})')
    # plt.show()
    # save the plot
    plt.savefig(f'{quantitatives}/scatter_{num_var1}_{num_var2}.png')


def correlation_heatmap(df, num_vars):
    plt.figure(figsize=(10, 6))
    corr_matrix = df[num_vars].corr(method='spearman')  # You can change 'spearman' to 'pearson' for Pearson correlation
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Correlation Heatmap')
    # plt.show()
    # save the plot
    plt.savefig(f'{quantitatives}/num_correlation_heatmap.png')

def execute_file(df_lots):
    bool_couples = [
        ('outOfDirectives', 'onBehalf'),
        ('outOfDirectives', 'jointProcurement'),
        ('outOfDirectives', 'fraAgreement'),
        ('outOfDirectives', 'accelerated'),
        ('outOfDirectives', 'contractorSme'),
        ('outOfDirectives', 'subContracted'),
        ('outOfDirectives', 'gpa'),
        ('outOfDirectives', 'jointProcurement'),
        ('outOfDirectives', 'cancelled'),
        ('onBehalf', 'jointProcurement'),
        ('onBehalf', 'fraAgreement'),
        ('onBehalf', 'accelerated'),
        ('onBehalf', 'contractorSme'),
        ('onBehalf', 'subContracted'),
        ('onBehalf', 'gpa'),
        ('onBehalf', 'jointProcurement'),
        ('onBehalf', 'cancelled'),
        ('jointProcurement', 'fraAgreement'),
        ('jointProcurement', 'accelerated'),
        ('jointProcurement', 'contractorSme'),
        ('jointProcurement', 'subContracted'),
        ('jointProcurement', 'subContracted'),
        ('jointProcurement', 'gpa'),
        ('jointProcurement', 'cancelled'),
        ('fraAgreement', 'accelerated'),
        ('fraAgreement', 'fraEstimated'),
        ('fraAgreement', 'contractorSme'),
        ('fraAgreement', 'subContracted'),
        ('fraAgreement', 'gpa'),
        ('fraAgreement', 'jointProcurement'),
        ('fraAgreement', 'cancelled'),
        ('accelerated', 'contractorSme'),
        ('accelerated', 'subContracted'),
        ('accelerated', 'gpa'),
        ('accelerated', 'jointProcurement'),
        ('accelerated', 'cancelled'),
        ('contractorSme', 'subContracted'),
        ('contractorSme', 'gpa'),
        ('contractorSme', 'jointProcurement'),
        ('contractorSme', 'cancelled'),
        ('subContracted', 'gpa'),
        ('subContracted', 'jointProcurement'),
        ('subContracted', 'cancelled'),
        ('gpa', 'jointProcurement'),
        ('gpa', 'cancelled'),
        ('jointProcurement', 'cancelled')
    ]

    couples = [
        ('typeOfContract', 'cancelled'),
        ('typeOfContract', 'outOfDirectives'),
        ('typeOfContract', 'onBehalf'),
        ('typeOfContract', 'jointProcurement'),
        ('typeOfContract', 'fraAgreement'),
        ('typeOfContract', 'accelerated'),
        ('typeOfContract', 'contractorSme'),
        ('typeOfContract', 'subContracted'),
        ('typeOfContract', 'gpa'),
        ('cpv_name', 'typeOfContract'),
        ('cpv_name', 'cancelled'),
        ('cpv_name', 'subContracted'),
        ('topType', 'outOfDirectives'),
        ('topType', 'gpa'),
        ('cpv_name', 'renewal'),
        ('renewal', 'typeOfContract'),
        ('multipleCae', 'jointProcurement'),
        ('multipleCae', 'onBehalf'),
    ]

    numeric_pairs = [
        ('awardEstimatedPrice', 'awardPrice'),
        ('awardEstimatedPrice', 'contractDuration'),
        ('awardEstimatedPrice', 'publicityDuration'),
        ('awardPrice', 'contractDuration'),
        ('awardPrice', 'publicityDuration'),
        ('contractDuration', 'publicityDuration'),
        ('numberTendersSme', 'numberTenders')
    ]

    for couple in bool_couples:
        bool_categorical_bivariate(df_lots.copy(), couple[0], couple[1])
    for couple in couples:
        categorical_bivariate(df_lots.copy(), couple[0], couple[1])
    variables = ['cancelled', 'outOfDirectives', 'onBehalf', 'jointProcurement', 'fraAgreement', 'fraEstimated', 'topType', 'renewal',
                 'accelerated', 'contractorSme', 'subContracted', 'gpa', 'typeOfContract', 'cpv_name', 'multipleCae']
    create_cramer_v_heatmap(df_lots.copy(), variables)

    # Scatter plots for numeric variable pairs
    for pair in numeric_pairs:
        numeric_bivariate_scatter(df_lots, pair[0], pair[1])

    # Correlation heatmap for all numeric variables
    numeric_vars = ['awardEstimatedPrice', 'awardPrice', 'contractDuration', 'publicityDuration', 'numberTendersSme', 'numberTenders', 'correctionsNb']
    correlation_heatmap(df_lots, numeric_vars)
