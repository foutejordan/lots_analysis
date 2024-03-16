import pandas as pd
import numpy as np
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

lots_path = os.path.join(BASE_DIR, 'Lots_analysis', 'figs', 'univarie', 'lots')

df_lots = pd.read_csv('data/Lots.csv')

columns = df_lots.columns

# display distinct values for each column
# for col in columns:
#     print(col, df_lots[col].unique())

# pourcentage of missing values
missing_values = df_lots.isnull().sum() / df_lots.shape[0]

# Calculez les statistiques standard, en fonction de la nature de la variable : moyenne, écart-type, quantiles, mode, min, max
for col in columns:
    if df_lots[col].dtype == 'float64':
        print(col, df_lots[col].describe())
    else:
        print(col, df_lots[col].value_counts())


import matplotlib.pyplot as plt
import seaborn as sns
#
# column = df_lots['numberTendersSme']
# # convertir la colonne en numérique et mettre les valeurs manquantes et les valeurs non numériques en NaN
# df_lots['numberTendersSme'] = pd.to_numeric(df_lots['numberTendersSme'], errors='coerce')
#
# print(df_lots['numberTendersSme'].describe())
#
# # l'histogramme
# plt.figure(figsize=(10,5))
# plt.hist(df_lots['numberTendersSme'], bins=30, color='green', alpha=0.7)
# plt.title('Histogram - numberTendersSme')
# plt.savefig('figs/Histogram_numberTendersSme.png')
# plt.show()
#
# df_lots['numberTendersSme_log'] = np.log1p(df_lots['numberTendersSme'])
#
# # Histogramme de la nouvelle variable
# plt.figure(figsize=(10,5))
# plt.hist(df_lots['numberTendersSme_log'], bins=30, color='blue', alpha=0.7)
# plt.title('Histogram - Log of numberTendersSme')
# plt.savefig('figs/Log_Histogram_numberTendersSme.png')
# plt.show()
#
# plt.figure(figsize=(10,5))
# sns.boxplot(df_lots['numberTendersSme'])
# plt.title('Box plot - numberTendersSme')
# plt.savefig('figs/Boxplot_numberTendersSme.png')
# plt.show()

# cat_counts = df_lots['accelerated'].value_counts(dropna=False)
# plt.figure(figsize=(10,5))
# cat_counts.plot(kind='bar', color=['red', 'green'])
# plt.title('Bar plot - accelerated')
# plt.xlabel('Category')
# plt.ylabel('Count')
# plt.savefig('figs/accelerated.png')
# plt.show()

cat_counts = df_lots['accelerated'].value_counts(dropna=False)
# Calculez les pourcentages
total_count = len(df_lots['accelerated'])
percentage_values = cat_counts / total_count * 100
colors = ['gray','green', 'blue']
plt.figure(figsize=(10,5))
bars = cat_counts.plot(kind='bar', color=colors)

# Ajoutez les pourcentages au-dessus de chaque barre
for bar, percentage in zip(bars.patches, percentage_values):
    plt.text(bar.get_x() + bar.get_width() / 2 - 0.1, bar.get_height() + 0.05,
             f'{percentage:.2f}%', ha='center', va='bottom', color='black', fontsize=10)
plt.title('Bar plot - accelerated')
plt.xlabel('Category')
plt.ylabel('Count')
plt.savefig(f'{lots_path}/accelerated.png')
plt.show()