# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 09:58:27 2024

@author: pikam
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path


    
    
def verif_path(entire_path):
    path = Path(entire_path)
    
    directory = path.parent
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)
    


def graph_plot_bar(dict_valeur, nombre_de_lignes, name_x, name_df):
    
    pourcentages = (dict_valeur / nombre_de_lignes) *100
    pourcentages.plot(kind='bar', color='skyblue')
    plt.xlabel('Catégories')
    plt.ylabel('Pourcentage')
    plt.title('Distribution des catégories de la variable '+name_x+' en pourcentage')
    
    for index, value in enumerate(pourcentages):
        plt.text(index, value, f'{value:.2f}%', ha='center', va='bottom')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    
    entire_path = 'figs/'+name_df+'/graph_plot_bar_'+name_x+'.png'
    verif_path(entire_path)
    
    
    plt.savefig(entire_path)
    
    #plt.show()



def density_curve(target_column, name_column, name_df):
    sns.kdeplot(target_column, shade=True, color='blue', label='Densité', bw_method=0.5)
    
    plt.title('Courbe de Densité')
    plt.xlabel('Valeurs de la colonne '+name_column)
    plt.ylabel('Densité')
    
    entire_path = 'figs/'+name_df+'/density_curve_'+name_column+'.png'
    verif_path(entire_path)
    plt.savefig(entire_path)

    #plt.show()

    
    
def graph_dispersion(target_column, name_column, name_df):
    y = [0] * len(target_column)
    
    plt.scatter(target_column, y, color='blue', marker='o', label=name_column)
    plt.title('Graphique de dispersion de la variable '+name_column)
    plt.xlabel(name_column)
    plt.legend()
    plt.grid(True)
    
    entire_path = 'figs/'+name_df+'/graph_dispersion_'+name_column+'.png'
    verif_path(entire_path)
    plt.savefig(entire_path)
    
    #plt.show()
    
    
def graph_count(target_column, name_column, name_df):
    plt.hist(target_column, bins=10, color='skyblue', edgecolor='black')
    
    plt.xlabel('Nombre d\'apparition d\'un '+name_column)
    plt.ylabel('Combien de '+name_column+' ont ce nombre d\'apparition')
    plt.title('Histogramme des valeurs de la variable '+name_column)
    
    plt.grid(True)
    plt.yscale('log')
    
    entire_path = 'figs/'+name_df+'/graph_counts_'+name_column+'.png'
    verif_path(entire_path)
    plt.savefig(entire_path)
    
    #plt.show()



def stats(target_column, version):
    #version 1 or 2
    
    valeur_max = target_column.max()
    print("max : ",valeur_max)
    valeur_min = target_column.min()
    print("min : ",valeur_min)
    valeur_mean = target_column.mean()
    print("mean : ",valeur_mean)
    valeur_std = target_column.std()
    print("std : ",valeur_std)
    valeur_var = target_column.var()
    print("var : ",valeur_var)
    
    if version == 1:
    
        valeur_median = target_column.median()
        print("median : ",valeur_median)
        valeur_quartiles = target_column.quantile([0.25, 0.5, 0.75])
        print("quartiles : ",valeur_quartiles)
    
    if version == 2 :
    
        valeur_median = np.median(target_column)
        print("median : ",valeur_median)
        series_data = pd.Series(target_column)
        quantiles = series_data.quantile([0.25, 0.5, 0.75])
        print("quartiles : ",quantiles)



def analyse_Lots():
    
    nameDf = "Lots"

    types_de_donnees = {'typeOfContract':str, 'topType': str, 'renewal':str} #colonne 23
    
    dataframe = pd.read_csv('data/Lots.csv', header=0, sep=',', dtype=types_de_donnees)
    colonne_multipleCae = dataframe['multipleCae']
    colonne_typeOfContract = dataframe['typeOfContract']
    colonne_topType = dataframe['topType']
    colonne_renewal = dataframe['renewal']
    colonne_contractDuration = dataframe['contractDuration']
    colonne_publicityDuration = dataframe['publicityDuration']
    

    nombre_de_lignes = len(dataframe)
    print("Nombre de lignes du dataset Lots :", nombre_de_lignes)
    
    
    dict_valeur_multipleCae = colonne_multipleCae.value_counts()
    dict_valeur_typeOfContract = colonne_typeOfContract.value_counts()
    dict_valeur_topType = colonne_topType.value_counts()
    dict_valeur_renewal = colonne_renewal.value_counts()
    dict_valeur_contractDuration = colonne_contractDuration.value_counts()
    dict_valeur_publicityDuration = colonne_publicityDuration.value_counts()
    
    nombre_total_occurrences = dict_valeur_multipleCae.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurrences)
    print(dict_valeur_multipleCae)
    graph_plot_bar(dict_valeur_multipleCae, nombre_de_lignes, "multipleCae", nameDf)
    print("\n")
    
    nombre_total_occurrences = dict_valeur_typeOfContract.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurrences)
    print(dict_valeur_typeOfContract)
    graph_plot_bar(dict_valeur_typeOfContract, nombre_de_lignes, "typeOfContract", nameDf)
    print("\n")

    
    nombre_total_occurrences = dict_valeur_topType.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurrences)
    print(dict_valeur_topType)
    graph_plot_bar(dict_valeur_topType, nombre_de_lignes, "topType", nameDf)
    print("\n")

    
    nombre_total_occurrences = dict_valeur_renewal.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurrences)
    print(dict_valeur_renewal)
    graph_plot_bar(dict_valeur_renewal, nombre_de_lignes, "renewal", nameDf)
    print("\n")

    
    nombre_total_occurrences = dict_valeur_contractDuration.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurrences)
    density_curve(colonne_contractDuration, "contractDuration", nameDf)
    graph_dispersion(colonne_contractDuration, "contractDuration", nameDf)
    stats(colonne_contractDuration, 1)
    print("\n")

    
    nombre_total_occurrences = dict_valeur_publicityDuration.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurrences)
    density_curve(colonne_publicityDuration, "publicityDuration", nameDf)
    stats(colonne_publicityDuration, 1)
    print("\n")






#############################"

def analyse_LotBuyers():

    nameDf = "LotBuyers"
    dataframe = pd.read_csv('data/LotBuyers.csv', header=0, sep=',')
    
    
    colonne_lotId = dataframe['lotId']
    colonne_agentId = dataframe['agentId']
    
    nombre_de_lignes = len(dataframe)
    print("Nombre de lignes du dataset LotBuyers :", nombre_de_lignes)
    print("\n")
    
    dict_valeur_lotId = colonne_lotId.value_counts()
    dict_valeur_agentId = colonne_agentId.value_counts()
    
    print("variable lotId :")
    nombre_total_occurences = dict_valeur_lotId.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurences)
    
    freq_maximale = dict_valeur_lotId.max()
    dict_valeur_lotId_freq_max = {lotId: freq for lotId, freq in dict_valeur_lotId.items() if freq == freq_maximale}
    print("lotId qui apparaissent "+str(freq_maximale)+" fois (fréquence maximale) : ",list(dict_valeur_lotId_freq_max.keys()))
    
    graph_count(dict_valeur_lotId.values, "lotId", nameDf)
    print("\n")
    
    print("variable agentId :")
    nombre_total_occurences = dict_valeur_agentId.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurences)
    
    freq_maximale = dict_valeur_agentId.max()
    dict_valeur_agentId_freq_max = {lotId: freq for lotId, freq in dict_valeur_agentId.items() if freq == freq_maximale}
    print("mode, l'agentId : "+str(list(dict_valeur_agentId_freq_max.keys())[0])+" nombre occurences : ",str(freq_maximale))
    
    graph_count(dict_valeur_agentId.values, "agentId", nameDf)
    print("\n")




#############################


def analyse_LotSuppliers():

    
    nameDf = "LotSuppliers"

    dataframe = pd.read_csv('data/LotSuppliers.csv', header=0, sep=',')
    
    colonne_lotId = dataframe['lotId']
    colonne_agentId = dataframe['agentId']
    
    nombre_de_lignes = len(dataframe)
    print("Nombre de lignes du dataset LotSuppliers :", nombre_de_lignes)
    print("\n")
    
    dict_valeur_lotId = colonne_lotId.value_counts()
    dict_valeur_agentId = colonne_agentId.value_counts()
    
    
    print("variable lotId :")
    nombre_total_occurences = dict_valeur_lotId.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurences)
    
    freq_maximale = dict_valeur_lotId.max()
    dict_valeur_lotId_freq_max = {lotId: freq for lotId, freq in dict_valeur_lotId.items() if freq == freq_maximale}
    print("mode, lotId : "+str(list(dict_valeur_lotId_freq_max.keys())[0])+" nombre occurences : ",str(freq_maximale))
    stats(dict_valeur_lotId.values, 2)
    
    graph_count(dict_valeur_lotId.values, "lotId", nameDf)
    print("\n")
    
    print("variable agentId :")
    nombre_total_occurences = dict_valeur_agentId.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurences)
    
    freq_maximale = dict_valeur_agentId.max()
    dict_valeur_agentId_freq_max = {lotId: freq for lotId, freq in dict_valeur_agentId.items() if freq == freq_maximale}
    print("mode, l'agentId : "+str(list(dict_valeur_agentId_freq_max.keys())[0])+" nombre occurences : ",str(freq_maximale))
    stats(dict_valeur_agentId.values, 2)
    
    graph_count(dict_valeur_agentId.values, "agentId", nameDf)
    print("\n")
    
    

    


    
#############################



def analyse_Criteria():

    nameDf = "Criteria"
    dataframe = pd.read_csv('data/Criteria.csv', header=0, sep=',', encoding='utf-8')
    
    colonne_lotId = dataframe['lotId']
    colonne_name = dataframe['name']
    colonne_weight = dataframe['weight']
    colonne_type = dataframe['type']
    
    nombre_de_lignes = len(dataframe)
    print("Nombre de lignes du dataset Criteria :", nombre_de_lignes)
    print("\n")
    
    dict_valeur_lotId = colonne_lotId.value_counts()
    dict_valeur_name = colonne_name.value_counts()
    dict_valeur_weight = colonne_weight.value_counts()
    dict_valeur_type = colonne_type.value_counts()
    
    
    print("variable lotId :")
    nombre_total_occurences = dict_valeur_lotId.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurences)
    
    freq_maximale = dict_valeur_lotId.max()
    dict_valeur_lotId_freq_max = {lotId: freq for lotId, freq in dict_valeur_lotId.items() if freq == freq_maximale}
    print("lotId qui apparaissent "+str(freq_maximale)+" fois (fréquence maximale) : ",list(dict_valeur_lotId_freq_max.keys()))
    
    graph_count(dict_valeur_lotId.values, "lotId", nameDf)
    print("\n")
    
    
    print("variable name :")
    nombre_total_occurences = dict_valeur_name.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurences)
    
    freq_maximale = dict_valeur_name.max()
    dict_valeur_name_freq_max = {lotId: freq for lotId, freq in dict_valeur_name.items() if freq == freq_maximale}
    print("mode, name : "+str(list(dict_valeur_name_freq_max.keys())[0])+" nombre occurences : ",str(freq_maximale))
    
    graph_count(dict_valeur_name.values, "name", nameDf)
    print("\n")
    
    
    nombre_total_occurrences = dict_valeur_weight.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurrences)
    density_curve(colonne_weight, "weight", nameDf)
    stats(colonne_weight, 1)
    print("\n")
    
    
    nombre_total_occurrences = dict_valeur_type.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurrences)
    print(dict_valeur_type)
    graph_plot_bar(dict_valeur_type, nombre_de_lignes, "type", nameDf)
    print("\n")
    
    
    


#############################



def analyse_Names():
    
    nameDf = "Names"

    dataframe = pd.read_csv('data/Names.csv', header=0, sep=',')
    
    colonne_agentId = dataframe['agentId']
    colonne_name = dataframe['name']
    
    nombre_de_lignes = len(dataframe)
    print("Nombre de lignes du dataset Names :", nombre_de_lignes)
    print("\n")
    
    dict_valeur_agentId = colonne_agentId.value_counts()
    dict_valeur_name = colonne_name.value_counts()
    
    
    print("variable agentId :")
    nombre_total_occurences = dict_valeur_agentId.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurences)
    
    freq_maximale = dict_valeur_agentId.max()
    dict_valeur_agentId_freq_max = {lotId: freq for lotId, freq in dict_valeur_agentId.items() if freq == freq_maximale}
    print("mode, l'agentId : "+str(list(dict_valeur_agentId_freq_max.keys())[0])+" nombre occurences : ",str(freq_maximale))
    stats(dict_valeur_agentId.values, 2)
    
    graph_count(dict_valeur_agentId.values, "agentId", nameDf)
    print("\n")
    
    
    print("variable name :")
    nombre_total_occurences = dict_valeur_name.sum()
    print("nombre de vide : ", nombre_de_lignes - nombre_total_occurences)
    
    freq_maximale = dict_valeur_name.max()
    dict_valeur_name_freq_max = {lotId: freq for lotId, freq in dict_valeur_name.items() if freq == freq_maximale}
    print("mode, name : "+str(list(dict_valeur_name_freq_max.keys())[0])+" nombre occurences : ",str(freq_maximale))
    stats(dict_valeur_name.values, 2)
    
    graph_count(dict_valeur_name.values, "name", nameDf)
    print("\n")
    
    





def execute_file():
    
    analyse_Lots()
    analyse_LotBuyers()
    analyse_LotSuppliers()
    analyse_Criteria()
    analyse_Names()












