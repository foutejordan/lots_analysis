# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:03:34 2024

@author: pikam
"""




import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist
import seaborn as sns
from R_square_clustering import r_square



def verif_path(entire_path):
    path = Path(entire_path)
    
    directory = path.parent
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)





def analyse_Lots_not_cleaned():
    dataframe = pd.read_csv('data/Lots.csv', header=0, sep=',', dtype=str)
    
    print("-------------- version non nettoyée --------------")
        
    colonne_numberTendersSme = dataframe['numberTendersSme']
    colonne_contractorSme = dataframe['contractorSme']
    
    
    colonnes = [colonne_numberTendersSme, colonne_contractorSme]
    
    nombre_de_lignes = len(dataframe)
    print("Nombre de lignes du dataset Lots :", nombre_de_lignes)
    
    nombre_total_occurrences_tenders = colonne_numberTendersSme.value_counts().sum()
    print("nombre de vide numberTendersSme: ", nombre_de_lignes - nombre_total_occurrences_tenders)
    
    nombre_total_occurrences_contractor = colonne_contractorSme.value_counts().sum()
    print("nombre de vide contractorSme : ", nombre_de_lignes - nombre_total_occurrences_contractor)

    
    count_nb_pme_winner = 0
    count_nb_pme_offer = 0
    
    
    for index, row in dataframe.iterrows():
        if float(row['numberTendersSme']) > 0 and (row['contractorSme'] == "Y" or row['contractorSme'] == "N"):
            count_nb_pme_offer = count_nb_pme_offer +1
            if (row['contractorSme']) == "Y" :
                count_nb_pme_winner = count_nb_pme_winner +1
    print("Nombre de lots qui contient une offre réalisé par une PME : ",count_nb_pme_offer)
    print("en % : ", count_nb_pme_offer*100/(nombre_de_lignes - (nombre_de_lignes-nombre_total_occurrences_tenders)))

    print("Nombre de lots gagné par une PME : ",count_nb_pme_winner)
    print("en % : ", count_nb_pme_winner*100/(nombre_de_lignes - (nombre_de_lignes-nombre_total_occurrences_contractor)))



    
    
def analyse_Lots_cleaned():
    
    
    dataframe = pd.read_csv('data/Lots_cleaned.csv', header=0, sep=',', dtype=str)
    
    print("-------------- version nettoyée --------------")
        
    colonne_numberTendersSme = dataframe['numberTendersSme']
    colonne_contractorSme = dataframe['contractorSme']
    
    
    colonnes = [colonne_numberTendersSme, colonne_contractorSme]
    
    nombre_de_lignes = len(dataframe)
    print("Nombre de lignes du dataset Lots :", nombre_de_lignes)
    
    nombre_total_occurrences_tenders = colonne_numberTendersSme.value_counts().sum()
    print("nombre de vide numberTendersSme: ", nombre_de_lignes - nombre_total_occurrences_tenders)
    
    nombre_total_occurrences_contractor = colonne_contractorSme.value_counts().sum()
    print("nombre de vide contractorSme : ", nombre_de_lignes - nombre_total_occurrences_contractor)

    count_nb_pme_winner = 0
    count_nb_pme_offer = 0

    for valeur in colonne_numberTendersSme :
        if float(valeur) > 0 :
            count_nb_pme_offer = count_nb_pme_offer +1
    print("Nombre de lots qui contient une offre réalisé par une PME : ",count_nb_pme_offer)
    print("en % : ", count_nb_pme_offer*100/nombre_de_lignes)
    
    for valeur in colonne_contractorSme :
        if valeur == "Y" :
            count_nb_pme_winner = count_nb_pme_winner +1
    print("Nombre de lots gagné par une PME : ",count_nb_pme_winner)
    print("en % : ", count_nb_pme_winner*100/nombre_de_lignes)
    
    
    cpv_numberTendersSme = {}
    cpv_contractorSme = {}
    for index, row in dataframe.iterrows():
        cpv = str(row['cpv_name'])
        numberTendersSme = row['numberTendersSme']
        contractorSme = row['contractorSme']
        
        if contractorSme == "Y":
            contractorSme = 1
        else : 
            contractorSme = 0
            
        if cpv in cpv_numberTendersSme :
            cpv_numberTendersSme[cpv] = cpv_numberTendersSme[cpv] + float(numberTendersSme)
        else :
            cpv_numberTendersSme[cpv] = 0
            
        if cpv in cpv_contractorSme :
            cpv_contractorSme[cpv] = cpv_contractorSme[cpv] + contractorSme
        else :
            cpv_contractorSme[cpv] = 0
                        
        
    cpv_numberTendersSme = sorted(cpv_numberTendersSme.items(), key=lambda x: x[1], reverse=True)
    cpv_contractorSme_bis = sorted(cpv_contractorSme.items(), key=lambda x: x[1], reverse=True)
    
    print("top 3 nombre d'offres PME par secteur d'activité")
    i = 0
    for cpv, count in cpv_numberTendersSme:
        i = i +1
        if i == 3 :
            break
        else :
            print(f"Nombre d'offres pour {cpv} : {count}")
        
    print("-------------------------")
    
    print("top 3 nombre de gagnants PME par secteur d'activité")
    i = 0
    for cpv, count in cpv_contractorSme_bis:
        i = i +1
        if i == 3:
            break
        else :
            print("Nombre de gagnants ", cpv, " : ", count)
            

    categories = [item[0] for item in cpv_numberTendersSme]
    count = [item[1] for item in cpv_numberTendersSme]
    
    tailles_bulles = [cpv_contractorSme.get(cpv) for cpv in categories]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(categories, count, s=[t/100 for t in tailles_bulles], alpha=0.5)
    
    plt.yscale('log')
    plt.title("Graphique Bubble du nombre d'offres de PME par cpv, taille des bulles selon le nombre de gagnants")
    plt.xlabel("Cpv")
    plt.ylabel("NumberTendersSme")
    
    entire_path = 'figs/Lots_cleaned/bubble_graph_contractorSme_numberTendersSme_cpvName.png'
    verif_path(entire_path)
    plt.savefig(entire_path)




def clustering_Lots():
        
    """
    
    
-pas mettre les id (lotId et tedCanId) car pas intéressant, n'apporte pas d'information pour créer des classes de similarité, valeurs différentes pour chaque ligne
-correctionsNb, awardEstimatedPrice, awardPrice, numberTenders, lotsNumber, numberTendersSme, contractDuration, publicityDuration
-les booléens ? cancelled, onBehalf, jointProcurement, fraAgreement, accelerated, outOfDirectives, contractorSme, subContracted, gpa, multipleCae, renewal
-les dates ? awardDate
-catégorielles : cpv, fraEstimated, typeOfContract, topType

    
    """
    
    #aucune colonne numérique détiens plus de 70% de valeurs manquantes après nettoyage
    #-> supprimer les lignes où valeurs manquantes pour effectuer kmeans
    #tous les booléens restant ont aucune valeur manquante
    #dans les autres, aucune valeur manquante aussi
    
    #convertir variable booléenne en numérique pour qu au lieu d avoir Y/N avoir 1/0
    #remplacer award date par colonne avec année, colonne avec mois et colonne avec jour
    #one hot des variables avec plusieurs catégories

    
    dataframe = pd.read_csv('data/Lots_cleaned.csv', header=0, sep=',', dtype=str)
    dataframe.dropna(inplace=True)
    
    dataframe = pd.get_dummies(dataframe, columns=['cpv_name', 'fraEstimated', 'typeOfContract', 'topType'])
    
    dataframe['onBehalf'] = dataframe['onBehalf'].replace({'N':0, 'Y':1})
    dataframe['jointProcurement'] = dataframe['jointProcurement'].replace({'N':0, 'Y':1})
    dataframe['fraAgreement'] = dataframe['fraAgreement'].replace({'N':0, 'Y':1})
    dataframe['contractorSme'] = dataframe['contractorSme'].replace({'N':0, 'Y':1})
    dataframe['subContracted'] = dataframe['subContracted'].replace({'N':0, 'Y':1})
    dataframe['gpa'] = dataframe['gpa'].replace({'N':0, 'Y':1})
    dataframe['multipleCae'] = dataframe['multipleCae'].replace({'N':0, 'Y':1})
    dataframe['renewal'] = dataframe['renewal'].replace({'N':0, 'Y':1})
    
    colonne_awardDate = dataframe['awardDate']
    
    colonne_awardDate = pd.to_datetime(dataframe['awardDate'])
    dataframe['year'] = colonne_awardDate.dt.year
    dataframe['month'] = colonne_awardDate.dt.month
    dataframe['day'] = colonne_awardDate.dt.day
    dataframe = dataframe.drop(columns=['awardDate', 'lotId', 'tedCanId', 'cpv'])
    dataframe = dataframe.drop(columns=['awardEstimatedPrice']) #très corrélé à awardPrice, ne change pas résultat kmeans

    
    # Convertir les valeurs en nombres (les non-numériques seront converties en NaN) 
    #-> à faire pour la variable lotNumber
    dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
    
    # Supprimer les lignes contenant des NaN
    dataframe = dataframe.dropna()
    

    
    

    """colonnes = [colonne_correctionsNb, colonne_awardEstimatedPrice, 
                colonne_awardPrice, 
                colonne_lotsNumber, colonne_numberTenders, colonne_numberTendersSme,
                colonne_contractDuration, colonne_publicityDuration]
    
    bools = [colonne_cancelled, colonne_onBehalf, colonne_jointProcurement, colonne_fraAgreement,
                        colonne_outOfDirectives
             , colonne_contractorSme, colonne_subContracted,
             colonne_gpa, colonne_multipleCae, colonne_renewal]
    
    #autres = [colonne_awardDate, colonne_year, colonne_month, colonne_day, 
    #          colonne_cpv_71, colonne_cpv_33 ,colonne_fraEstimated, colonne_typeOfContract, colonne_topType]
            
    autres = [colonne_cpv_71, colonne_cpv_33, colonne_typeOfContract_S, colonne_typeOfContract_W]
        
    for colonne in autres :
    
        dict_valeur = colonne.value_counts()
        print(dict_valeur)
    
        nombre_de_lignes = len(dataframe)
        print("Nombre de lignes du dataset Lots :", nombre_de_lignes)
    
        nombre_total_occurrences = dict_valeur.sum()
        nb_vide = nombre_de_lignes - nombre_total_occurrences
        print("nombre de vide : ", nombre_de_lignes - nombre_total_occurrences)
        if nb_vide > (nombre_de_lignes * 60 / 100):
            print("to delete")"""
            
            
    #normalisation
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(dataframe)
    
    
    list_k = [3,4,5,6,7,8]
    lst_rsq = []
    
    #part of this code is taken from our courses of data analytics

    
    for k in list_k :
        print(k)
            
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(dataframe.values)
        labels = kmeans.predict(dataframe)
        rsq = r_square(dataframe.values, kmeans.cluster_centers_, kmeans.labels_, k)

        print("rsq", rsq)
        lst_rsq.append(rsq)
        
        dataframe['cluster_label'] = kmeans.labels_
    
        print(dataframe['cluster_label'].value_counts())  # Nombre d'observations dans chaque cluster
        #print(kmeans.cluster_centers_)
        
    plt.figure()
    plt.plot(list_k, lst_rsq, 'bx-')
    plt.xlabel('k')
    plt.ylabel('RSQ')
    plt.title('The Elbow Method showing the optimal k')
    #plt.show()
    plt.savefig('k-means_elbow_method')
        
  
    kmeans = KMeans(n_clusters=4, random_state=42)
    kmeans.fit(dataframe.values)
    labels = kmeans.predict(dataframe)
    rsq = r_square(dataframe.values, kmeans.cluster_centers_, kmeans.labels_, 4)
    
    dataframe['cluster_label'] = kmeans.labels_
    print(dataframe['cluster_label'].value_counts())

    
    for i in range(len(dataframe.columns)) :
        stats = dataframe.groupby("cluster_label").agg({dataframe.columns[i]: ['mean', 'median', 'min', 'max', 'count']})
        print(stats)

        
    #print(len(dataframe.columns))

    

            
    
        

    
    





def analyse_Lots():
    
    #questionnement PME
    """analyse_Lots_not_cleaned()
    analyse_Lots_cleaned()"""
    

    clustering_Lots()
    
    
    
    
    
    
    """count_cpv = {}
    for element in dataframe['cpv_name']:
        if element in count_cpv :
            count_cpv[element] = count_cpv[element] + 1
        else :
            count_cpv[element] = 0
    
    count_cpv_bis = sorted(count_cpv.items(), key=lambda x: x[1], reverse=True)
    print(count_cpv_bis)"""

    
    
    



def execute_file():
    analyse_Lots()
    
    
execute_file()








