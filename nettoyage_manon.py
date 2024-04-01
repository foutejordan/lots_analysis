# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 18:10:45 2024

@author: pikam
"""



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

import re
import csv

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer



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



def delete_rows_with_too_much_nan():
    data_paths = ["../data/Lots.csv", "../data/Agents.csv", "../data/Criteria.csv", "../data/LotBuyers.csv", "../data/LotSuppliers.csv", "../data/Names.csv"]
    new_dataframes = []
    for data_path in data_paths :
        #on enlève les lignes où il manque au moins 70% des données
        #print(data_path)
        dataframe = pd.read_csv(data_path, header=0, sep=',', dtype=str)
        count_row_to_delete = 0
        rows_to_delete = []
        count_rows = 0
        with open(data_path, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
        
            for idx, row in enumerate(csvreader):
                nan_count = sum(cell.strip() == '' for cell in row)
                num_columns = len(row)
                count_rows = count_rows +1
                
                if nan_count > (num_columns*60/100):
                    count_row_to_delete = count_row_to_delete +1
                    rows_to_delete.append(idx)
                    #print(row)
                    #print(f"Ligne {idx+1}: Nombre de colonnes = {num_columns}, Nombre de valeurs manquantes = {nan_count}")
        #print(count_row_to_delete, "/", count_rows)
        new_dataframes.append(dataframe.drop(rows_to_delete))
    return new_dataframes


 

def contains_only_alphanumeric(chaine): #false si contient que des chiffres
    if chaine == "nan":
        return False
    alphanumeric = re.compile(r'^(?=.*[a-zA-Z])[a-zA-Z0-9]+$')
    return alphanumeric.search(chaine)

def is_nan(chaine):
    return chaine == "nan"


def has_other_than_numbers(chaine):
    not_number = re.compile(r'[^0-9]')
    correspondances = not_number.search(chaine)

    return correspondances


def has_semicolon(chaine):
    semicolon = re.compile(r';')
    correspondances = semicolon.search(chaine)
    
    return correspondances

def has_point(chaine):
    result = chaine.find(".")
    if result != -1 :
        return True
    else :
        return False
    
def has_hyphen_minus(chaine):
    hyphen = re.compile(r'-')
    return hyphen.search(chaine)

def has_space(chaine):
    space = re.compile(r'\s')
    return space.search(chaine)


def has_ET(chaine):
    ET = re.compile(r'ET|&')
    correspondances = ET.search(chaine)
    return correspondances

def has_A(chaine):
    A = re.compile(r'(?<![a-zA-Z])A(?![a-zA-Z])') #A not followed with other letters
    correspondances = A.search(chaine)
    return correspondances

def remove_LOTS_NO(chaine):
    if chaine.startswith("LOTS NO"):
        chaine = chaine.replace("LOTS NO", "")
    if chaine.startswith("LOTS N"):
        chaine = chaine.replace("LOTS N", "")
    if chaine.startswith("LOTS"):
        chaine = chaine.replace("LOTS", "")
    return chaine


def analyse_lotsNumber(colonne_lotsNumber):
    
    clean_values = []
    old_values = []
    count = 0
    for value in colonne_lotsNumber :
        """if has_semicolon(str(value)[-1]):
            print(value)"""
        old_values.append(value)
        value = remove_LOTS_NO(str(value))
        
        if contains_only_alphanumeric(value):
            clean_values.append("1")
        
        elif has_semicolon(value):
            
            number = value.split(";")
            for i in range(len(number)):
                if not has_other_than_numbers(number[i]):
                    count = count +1
                else :
                    temp = number[i].strip() #enlève espace au début et à la fin
                    if not has_other_than_numbers(temp):
                        count= count +1
                    else :
                        if has_ET(temp):
                            count = count+2
                        elif has_A(temp) and len(temp) != 1:
                            temp = temp.split("A")
                            num1 = temp[0]
                            if has_point(num1):
                                count = 0
                                break
                            else :
                                num1 = int(temp[0])
                            num2 = temp[1]
                            if has_point(num2):
                                count = 0
                                break
                            else :
                                num2 = int(temp[1])
                            count = count + (num2-num1 +1)
                        else :
                            count = 0
                            break
            if count == 0:
                clean_values.append(value)
            else :
                clean_values.append(count)
            count= 0
            
        elif has_hyphen_minus(value) and not has_semicolon(value):
            number = value.split("-")
            if len(number) > 2:
                for i in range(len(number)):
                    temp = number[i].strip()
                    if not has_other_than_numbers(temp):
                        count = count +1
                    else : 
                        count = 0
                        break
                if count == 0:
                    clean_values.append(value)
                else :
                    clean_values.append(count)
            else :
                clean_values.append(value)
                
        elif has_space(value) and not has_hyphen_minus(value) and not has_semicolon(value):
            number = value.split()
            if len(number) == 3 and has_ET(number[1]):
                count = 2
            elif len(number) == 3 and has_A(number[1]):
                if has_other_than_numbers(number[0]):
                    count = 0
                elif has_other_than_numbers(number[2]):
                    count = 0
                else :
                    num1 = int(number[0])
                    num2 = int(number[2])
                    count = (num2-num1 +1)
            else :
                for i in range(len(number)):
                    if not has_other_than_numbers(number[i]):
                        count = count +1
                    else : 
                        count = 0
                        break
            if count == 0:
                clean_values.append(value)
            else :
                clean_values.append(count)
            
            
            
        else :
            clean_values.append(value)
        
            
    """count = 0
    for i in range(len(clean_values)) :
        #if is_nan(clean_values[i]):
        #if has_space(str(clean_values[i])) and not has_hyphen_minus(str(clean_values[i])) and not has_semicolon(str(clean_values[i])):
        if has_other_than_numbers(str(clean_values[i])) and not is_nan(str(clean_values[i])):
        #if contains_only_alphanumeric(str(clean_values[i])):
        #if has_hyphen_minus(str(clean_values[i])) and not has_semicolon(str(clean_values[i])):
            count = count +1
            print(clean_values[i], "old : ",old_values[i])
    print(count)"""
    
    return clean_values
    
    



def analyse_Lots(dataframe):
        
    #dataframe = pd.read_csv('data/Lots.csv', header=0, sep=',', dtype=str)
    
    colonne_lotsNumber = dataframe['lotsNumber']
    colonne_numberTenders = dataframe['numberTenders']
    colonne_numberTendersSme = dataframe['numberTendersSme']
    
    colonnes = [colonne_lotsNumber, colonne_numberTenders, colonne_numberTendersSme]
    
    """for colonne in colonnes :
    
        dict_valeur = colonne.value_counts()
        print(dict_valeur)
    
        nombre_de_lignes = len(dataframe)
        print("Nombre de lignes du dataset Lots :", nombre_de_lignes)
    
        nombre_total_occurrences = dict_valeur.sum()
        print("nombre de vide : ", nombre_de_lignes - nombre_total_occurrences)
        
        
        for valeur, occurences in dict_valeur.items():
            print(valeur, occurences)"""

    clean_values = analyse_lotsNumber(colonne_lotsNumber)
        
    dataframe = dataframe.drop('lotsNumber', axis=1)
    nouveau_dataframe = dataframe.copy()
    nouveau_dataframe['lotsNumber'] = clean_values
    
    nouveau_dataframe['publicityDuration'] = nouveau_dataframe['publicityDuration'].apply(lambda x: float(x) if isinstance(x, str) and float(x) >= 0 else np.nan)

    nouveau_dataframe['numberTendersSme'] = nouveau_dataframe['contractDuration'].fillna(0)

    nouveau_dataframe['contractDuration'] = nouveau_dataframe['contractDuration'].apply(lambda x: 720.0 if float(x) == 999.0 else float(x))


    
    colonne_contractDuration = nouveau_dataframe['contractDuration'].astype(float)
    colonne_publicityDuration = nouveau_dataframe['publicityDuration']
    colonne_numberTendersSme = nouveau_dataframe['numberTendersSme'].astype(float)
    
    colones = [colonne_contractDuration, colonne_publicityDuration, colonne_numberTendersSme]
    
    for colonne in colones :
        
    
        dict_valeur = colonne.value_counts()
    
        nombre_de_lignes = len(dataframe)
        print("Nombre de lignes du dataset Lots :", nombre_de_lignes)
    
        nombre_total_occurrences = dict_valeur.sum()
        print("nombre de vide : ", nombre_de_lignes - nombre_total_occurrences)
        
        stats(colonne, 1)
    
    return nouveau_dataframe
    
    
    #suivant article : https://towardsdatascience.com/iterative-imputation-with-scikit-learn-8f3eb22b1a38
        
    """columns = ['tedCanId', 'correctionsNb', 'cancelled', 'awardPrice', 'cpv', 'numberTenders', 'numberTendersSme', 'contractDuration', 'publicityDuration']
    
    
    iter_imputer = IterativeImputer(max_iter = 10, random_state=42)    
    
    # Ajuster l'imputeur en utilisant toutes les colonnes sauf la colonne cible
    iter_imputer.fit(nouveau_dataframe[columns])
    
    # Imputer les valeurs manquantes dans la colonne cible en utilisant toutes les colonnes
    nouveau_dataframe['numberTenders'] = iter_imputer.transform(nouveau_dataframe[columns])[:, columns.index('numberTenders')]
    

    
    nouveau_dataframe['numberTendersSme'] = iter_imputer.transform(nouveau_dataframe[columns])[:, columns.index('numberTendersSme')]


    
    nouveau_dataframe['contractDuration'] = iter_imputer.transform(nouveau_dataframe[columns])[:, columns.index('contractDuration')]


    
    nouveau_dataframe['publicityDuration'] = iter_imputer.transform(nouveau_dataframe[columns])[:, columns.index('publicityDuration')]

    print("enf")

    colonne_numberTenders = nouveau_dataframe['numberTenders']
    colonne_numberTendersSme = nouveau_dataframe['numberTendersSme']
    colonne_contractDuration = nouveau_dataframe['contractDuration']
    colonne_publicityDuration = nouveau_dataframe['publicityDuration']
    
    colones = [colonne_numberTenders, colonne_numberTendersSme, colonne_contractDuration, colonne_publicityDuration]
    
    for colonne in colones :
        
    
        dict_valeur = colonne.value_counts()
        print(dict_valeur)
    
        nombre_de_lignes = len(dataframe)
        print("Nombre de lignes du dataset Lots :", nombre_de_lignes)
    
        nombre_total_occurrences = dict_valeur.sum()
        print("nombre de vide : ", nombre_de_lignes - nombre_total_occurrences)
        
        stats(colonne, 1)"""

    



        
    

def analyse_criteria(dataframe):
    #criterionId : id, clé primaire
    #lotId : clé étrangère
    #weight et type : pas de vide, ni de valeurs aberrantes
    #name : 6 vide et pas de valeurs aberrantes, utilisation du mode pour remplacer les nan : PRIX
        
    #dataframe = pd.read_csv('data/Criteria.csv', header=0, sep=',')
    
    old_values = []
    clean_values = []
    colonne_name = dataframe['name']
    dict_colonne = {}
    
    
    for value in colonne_name :
        if pd.isna(value) :
            clean_values.append("PRIX")
            old_values.append(value)
        else :
            clean_values.append(value)
            old_values.append(value)
    
            
    dataframe = dataframe.drop('name', axis=1)
    nouveau_dataframe = dataframe[['criterionId', 'lotId', 'weight', 'type']].copy()
    nouveau_dataframe['name'] = clean_values
    
    
    return nouveau_dataframe



    


            


#2622 valeurs avec des ; dedans 
# -> après 1ere passe : reste 988 (split par ; si rien d autre que des chiffres, compte le nombre de lots)
# -> 2e passe : 675 (enlève les espace dans les split par ; si rien d autre que des chiffres, compte le nombre de lots)
# -> 3e passe : 253 (repère en plus si il y a un "ET", compte 2 lots en plus)
# -> 4e passe : 220 (enlève "LOTS NO", "LOTS N", "LOTS" en début de chaine)
# -> 5e passe : 196 (prend en compte les A entre deux int : compte le nombre de lots en tout)
# -> 6e passe : 192 (prend en plus des "ET" en compte, les "&")

#4079 valeurs avec des - et sans : dedans
#les "LOTS NO", "LOTS N", "LOTS" en début de chaine sont enlevés
# -> 1ere passe : 2714 (si que des nombres séparés par des - et qu'il y a plus de deux nombres, on compte combien il y a de numéros
#                 pas pris quand moins de deux numéros car ambiguité par ex 6-1 peut etre un seul numéro ou 3-11 peut etre les lots numéro 3 à 11)
# -> 2e passe : 2665 (enlève espaces dans les split par -)

#2420 valeurs avec des espaces, sans - et ; dedans
# -> 1 ere passe : 2012 (split par les espaces, si rien d autre que des chiffres, compte le nb de lots)
# -> 2e passe : 1364 (prend en compte les ET entre deux lots)
# -> 3e passe : 1136 (prend en compte les A entre deux numéro)


#312 138 valeurs avec autre chose que des chiffre dedans dont 295 428 valeurs nan, 16 710 autres
            
#6099 chaine de caractères qui contient que lettre ou mix de lettre/chiffres
#-> les remplace par 1 (on considère que c est un seul lot)
        
#après tout ces traitements sur les 16 710 en reste 5 478

    
    
   
    #délimitateur : ; GP - / ET
    #chaine de caractères, numéro trop grand, "8 ET 25", 
    
    
    
#pour numberTenders :
#424 099 vide

   
    
    
def execute_file():
    
    #ordre : lots, agents, criteria, lotbuyers, lotsuppliers, names
    new_dataframes = delete_rows_with_too_much_nan() 
    new_lots_df = new_dataframes[0]
    new_agents_df = new_dataframes[1]
    new_criteria_df = new_dataframes[2]
    new_lotbuyers_df = new_dataframes[3]
    new_lotsuppliers_df = new_dataframes[4]
    new_names_df = new_dataframes[5]
    
    new_lots_df = analyse_Lots(new_lots_df)
    new_criteria_df = analyse_criteria(new_criteria_df)
    

    





execute_file()

    

