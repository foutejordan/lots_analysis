# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 09:58:27 2024

@author: pikam
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns

import statsmodels.formula.api as smf
import statsmodels.api as sm

from pathlib import Path



"""

tout dans lots : 

typeOfContract (catégorielle ) - contractDuration (ratio) : check, stats anova : 0.038 , pas de relation

cpv (catégorielle) → contractDuration (ratio) : check, stats anova : 0.084, pas de relation
	=> regarder max de chaque catégorie, faire anova plus complète pour voir si différence significative entre chaque catégorie

typeOfContract (catégorielle) - publicityDuration (ratio) : check, stats anova : 0.004, pas de relation

awardPrice (ratio) → cancelled (catégorielle) : check , stats anova : 3.84*e-10, pas de relation 
	=> normal que quand annulé valeur à 0, mais vérifier pour valeur de awardprice bizarre => puissance 20


cpv (catégorielle) → cancelled (catégorielle): 2 variables catégorielles ?

cpv (catégorielle) → contractorSme (catégorielle): pareil ?
=> heatmap cramer déjà faite par jordan, voir commentaire sur overleaf



agentID → LotID (LotsBuyers) 

agentID, → LotID (LotsSuppliers)



"""

    
def verif_path(entire_path):
    path = Path(entire_path)
    
    directory = path.parent
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)



def anova(xName, yName, allData):
    #code taken from https://openclassrooms.com/fr/courses/7410486-nettoyez-et-analysez-votre-jeu-de-donnees/7428558-analysez-une-variable-quantitative-et-une-qualitative-par-anova
    #colonne x quantitative, colonne y qualitative
    
   anova = smf.ols(xName+'~'+yName, data=allData).fit()
   #print(sm.stats.anova_lm(anova, typ=2))
   print(sm.stats.anova_lm(anova))




def graph_violin(colonne_x, colonne_y, name_x, name_y, name_df, is_cleaned_data):
    #colonne_x qualitative, colonne_y quantitative
    
    plt.figure(figsize=(10, 6))
    
    sns.violinplot(x=colonne_x, y=colonne_y)
    
    plt.title('Diagramme en violon - '+name_y+' par '+name_x)
    plt.xlabel(name_x)
    plt.ylabel(name_y)
    
    entire_path = ''
    if is_cleaned_data:
        entire_path = '../descriptive_analysis/figs/bivarie/quantitativeVSqualitative/' + name_df + '/graph_violin_' + name_x + '_' + name_y + '.png'
    else:
        entire_path = 'figs/bivarie/quantitativeVSqualitative/' + name_df + '/graph_violin_' + name_x + '_' + name_y + '.png'
    verif_path(entire_path)
    plt.savefig(entire_path)
    
    #plt.show()
    
    
    
    
def categorical_bivariate(df, att1, att2, name_df, is_cleaned_data):
    # Group by att1 and att2, count occurrences, and reset index
    df_grouped = df.groupby([att1, att2]).size().reset_index(name='count')

    # Plot the barplot with hue
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_grouped, x=att1, y='count', hue=att2, palette='viridis')
    plt.yscale('log')

    plt.ylabel('Frequency (log scale)')
    plt.title(f'{att1} vs {att2}')
    
    entire_path = ''
    if is_cleaned_data:
        entire_path = '../descriptive_analysis/figs/bivarie/2qualitatives/' + name_df + '/graph_plot_bar_' + att1 + '_' + att2 + '.png'
    else:
        entire_path = 'figs/bivarie/2qualitatives/' + name_df + '/graph_plot_bar_' + att1 + '_' + att2 + '.png'

    verif_path(entire_path)
    plt.savefig(entire_path)
    
    #plt.show()



def analyse_lots(df_lots, is_cleaned_data):
        
    nameDf = "Lots"
    
    types_de_donnees = {'typeOfContract':str, 'topType': str, 'renewal':str} #colonne 23
    
    # dataframe = pd.read_csv('data/Lots.csv', header=0, sep=',', dtype=types_de_donnees)
    colonne_typeOfContract = df_lots['typeOfContract']
    colonne_contractDuration = df_lots['contractDuration']
    colonne_publicityDuration = df_lots['publicityDuration']
    colonne_cpv = df_lots['cpv'].astype(str).str[:2]
    colonne_awardPrice = df_lots['awardPrice']
    colonne_cancelled = df_lots['cancelled']
    colonne_contractorSme = df_lots['contractorSme']
    
    graph_violin(colonne_typeOfContract, colonne_contractDuration, "typeOfContract", "contractDuration", nameDf, is_cleaned_data)
    graph_violin(colonne_cpv, colonne_contractDuration, "cpv", "contractDuration", nameDf, is_cleaned_data)
    graph_violin(colonne_typeOfContract, colonne_publicityDuration, "typeOfContract", "publicityDuration", nameDf, is_cleaned_data)
    graph_violin(colonne_cancelled, colonne_awardPrice, "cancelled", "awardPrice", nameDf, is_cleaned_data)
    
    
    nouveau_dataframe = df_lots[['typeOfContract', 'contractDuration', 'publicityDuration', 'cpv', 'awardPrice', 'cancelled', 'contractorSme']].copy()
    nouveau_dataframe.loc[:, 'cpv'] = nouveau_dataframe['cpv'].astype(str).str[:2]

    categorical_bivariate(nouveau_dataframe.copy(), "cpv", "cancelled", nameDf, is_cleaned_data)
    
    
    df_filtré = nouveau_dataframe[colonne_contractorSme.isin(['Y', 'N'])]

    categorical_bivariate(df_filtré.copy(), "cpv", "contractorSme", nameDf, is_cleaned_data)

    anova('contractDuration', 'typeOfContract', df_lots)
    anova('contractDuration', 'cpv', df_lots)
    anova('publicityDuration', 'typeOfContract', df_lots)
    anova('awardPrice', 'cancelled', df_lots)
    
    """print(anova(colonne_cpv, colonne_contractDuration))
    print(anova(colonne_typeOfContract, colonne_publicityDuration))
    print(anova(colonne_cancelled, colonne_awardPrice))"""



def analyse_lotBuyers():
    
    nameDf = "LotBuyers"
    dataframe = pd.read_csv('data/LotBuyers.csv', header=0, sep=',')

    colonne_lotId = dataframe['lotId']
    colonne_agentId = dataframe['agentId']
    
    categorical_bivariate(dataframe.copy(), "lotId", "agentId")
    
    

def analyse_lotSuppliers():
    
    nameDf = "LotSuppliers"
    dataframe = pd.read_csv('data/LotSuppliers.csv', header=0, sep=',')
    
    
    colonne_lotId = dataframe['lotId']
    colonne_agentId = dataframe['agentId']
    
    categorical_bivariate(dataframe.copy(), "lotId", "agentId", nameDf)
    
    





def execute_file(df_lots, is_cleaned_data):
    analyse_lots(df_lots, is_cleaned_data)
    
    #analyse_lotBuyers()
    #analyse_lotSuppliers()
    



