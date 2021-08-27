# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 15:39:12 2021

@author: HP
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
# import statistics as s

data = pd.read_excel("C:\\Users\\HP\\Desktop\\Stage\\Code&BasesDeDonnées\\Données\\Stat11StocksBis.xlsx", sheet_name= "Feuil1", usecols=[0, 1, 3, 6, 7, 8, 10, 11, 12, 15, 19, 22, 23, 24, 25, 26])
data_vol = pd.read_excel("C:\\Users\\HP\\Desktop\\Stage\\Code&BasesDeDonnées\\Données\\stock_price_series_options.xlsx", sheet_name= "Exporter la feuille de calcul", usecols=[0, 1, 2, 8])

# 1ère étape on va remplir les SPOT_PRICE MIN et MAX vides 
# avec les cours de compensation

for i in range( len(data) ):
    
    if np.isnan(data.loc[i, 'SPOT_PRICE_MIN']):
        # np.isnan verifie si il y a la valeur "Not a Number" dans la liste
        data.loc[i, 'SPOT_PRICE_MIN'] = data.loc[i, 'COURS_COMPENS']
        data.loc[i, 'SPOT_PRICE_MAX'] = data.loc[i, 'COURS_COMPENS']
        

        
# # -------------------------------------------------------------------        
# # ----------------NOMBRE DE TITRES ÉCHANGÉS PAR STOCK----------------
# # -------------------------------------------------------------------


# # Dans ce tableau on va ajouter l'id des stocks à chaque fois qu'on en croise
# # un nouveau dans la base de donnée
# tab_stock_id = []


# for stock_id in data.loc[:, 'STOCK']:

#     if stock_id not in tab_stock_id:
#         tab_stock_id.append(stock_id)
  
        
# # La fonction sort() permet de trier le tableau du plus petit ID Stock au plus 
# # grand. Le résultat est donc [985, 1282, 1398, 1678, 2471, 3927, 4211, 4677, 
# # 4843, 5272, 10749]

# tab_stock_id.sort()

# # Dans ce tableau on aura un nombre de titres échangés. ex la première
# # ligne contiendra le nombre de titres échangés pour le stock avec le plus 
# # petit id (ici 985). La 2ème ligne le 2ème stock avec le plus petit id (1282) etc

# tab_nb_titre_ech = [0] * 24

# for stock_id in data.loc[:, 'STOCK']:
    
#     for index, value in enumerate(tab_stock_id):
#         if stock_id == value:
#             tab_nb_titre_ech[index] +=1
            
# # print("Moyenne :", np.mean(tab_nb_titre_ech))
# # quartiles = s.quantiles(tab_nb_titre_ech, n=4)
# # print("Quartiles are: " + str(quartiles))
# # print("Standard Deviation is ", np.std(tab_nb_titre_ech))

# # # Affichage graphique de cette statistique

# # x = np.arange(11) 
# # width = 0.4

# # plt.bar(x, tab_nb_titre_ech, width, color = 'black')
# # plt.xticks(x, tab_stock_id, rotation = 'vertical')

# # plt.xlabel("ID Stock")
# # #plt.ylabel("Nombre d'échange")
# # plt.title("Échanges par stock")

# # ------------------------------------------------------------------------
# # ------------------------------------------------------------------------
# # ------------------------------------------------------------------------


# # ------------------------------------------------------------------------
# # -------------------------DUREE DES MATURITE-----------------------------
# # ------------------------------------------------------------------------

# # Ce tableau a au début, 63 lignes initialisées à 0. On parcours la base de donnée.
# # On calcule la maturité de l'option. Pour une maturité T, on ajoute 1 à tab_matu[T]

# tab_matu = [0] * 63

# for i in range(len(data)):
    
#     tab_matu[int(str(dt.datetime.strptime(data.loc[i, 'EXACT_SETDATE'], "%d/%m/%Y") - 
#             dt.datetime.strptime(data.loc[i, 'DAY'], "%d/%m/%Y"))[0] + 
#         str(dt.datetime.strptime(data.loc[i, 'EXACT_SETDATE'], "%d/%m/%Y") 
#             - dt.datetime.strptime(data.loc[i, 'DAY'], "%d/%m/%Y"))[1])] +=1
    

# # Affichage graphique de cette statistique

# x = np.arange(63) 
# width = 0.8

# plt.bar(x, tab_matu, width, color = 'black')

# plt.xlabel("Maturité")
# plt.ylabel("Nombre d'options échangées")
# plt.title("Durées des options")


# # Calculer les pourcentages pour chaque durée d'option: on va regrouper les maturités
# # en 5 groupes: 0-1 jours, 14-17 jours, 28-31 jours, 42, 46 jours, 58-63 jours
# tab_regroupement_matu = [0] * 5
# somme = 0

# for index, matu in enumerate(tab_matu):
#      if index < 3:
#          tab_regroupement_matu[0] += matu
#          somme += matu
#      elif index > 11 and index < 17:
#           tab_regroupement_matu[1] += matu
#           somme += matu
#      elif index > 26 and index < 32:
#             tab_regroupement_matu[2] += matu
#             somme += matu
#      elif index > 41 and index < 48:
#            tab_regroupement_matu[3] += matu
#            somme += matu
#      elif index > 56:
#            tab_regroupement_matu[4] += matu
#            somme += matu

# for index, nb_matu in enumerate(tab_regroupement_matu):
#     tab_regroupement_matu[index] = nb_matu / somme * 100
# print(np.mean(tab_regroupement_matu))
# print(np.std(tab_regroupement_matu))
            

# # ----------------------------------------------------------------------
# # ----------------------------------------------------------------------
# # ----------------------------------------------------------------------


# # ----------------------------------------------------------------------
# # -------------DIVERSES STATS SUR LES COLONNES DE LA BDD----------------
# # ----------------------------------------------------------------------


# # ------------ MOYENNES -----------------

# print("Moyenne MIN:", np.mean(data.loc[:, 'MIN']))
# print("Moyenne MAX:", np.mean(data.loc[:, 'MAX']))
# print("Moyenne SPOT_PRICE_MIN:", np.mean(data.loc[:, 'SPOT_PRICE_MIN']))
# print("Moyenne SPOT_PRICE_MAX:", np.mean(data.loc[:, 'SPOT_PRICE_MAX']))
# print("Moyenne OPTION_VALUE:", np.mean(data.loc[:, 'OPTION_VALUE']), '\n\n')


# # --------------- QUARTILES -------------------

# quartiles = s.quantiles(data.loc[:, 'MIN'], n=4)
# print("Quartiles for MIN are: " + str(quartiles))
# quartiles = s.quantiles(data.loc[:, 'MAX'], n=4)
# print("Quartiles for MAX are: " + str(quartiles))
# quartiles = s.quantiles(data.loc[:, 'SPOT_PRICE_MIN'], n=4)
# print("Quartiles for SPOT_PRICE_MIN are: " + str(quartiles))
# quartiles = s.quantiles(data.loc[:, 'SPOT_PRICE_MAX'], n=4)
# print("Quartiles for SPOT_PRICE_MAX are: " + str(quartiles))
# quartiles = s.quantiles(data.loc[:, 'OPTION_VALUE'], n=4)
# print("Quartiles for OPTION_VALUE are: " + str(quartiles), '\n\n')

# # ----------------ECART-TYPES-----------------------
# print("Standard Deviation of MIN is ", np.std(data.loc[:, 'MIN']))
# print("Standard Deviation of MAX is ", np.std(data.loc[:, 'MAX']))
# print("Standard Deviation of SPOT_PRICE_MIN is ", np.std(data.loc[:, 'SPOT_PRICE_MIN']))
# print("Standard Deviation of SPOT_PRICE_MAX is ", np.std(data.loc[:, 'SPOT_PRICE_MAX']))
# print("Standard Deviation of OPTION_VALUE is ", np.std(data.loc[:, 'OPTION_VALUE']), '\n\n')

# # --------------DIVERS---------------------

# compteur_MINMAX = 0
# compteur_SPOT_PRICE_MINMAX = 0
# compteur_isYesterday = 0

# for i in range(len(data)):
#     if data.loc[i, 'MIN'] == data.loc[i, 'MAX']:
#         compteur_MINMAX +=1
#     if data.loc[i, 'SPOT_PRICE_MIN'] == data.loc[i, 'SPOT_PRICE_MAX']:
#         compteur_SPOT_PRICE_MINMAX +=1
#     if data.loc[i, 'IS_YESTERDAY'] == 1:
#         compteur_isYesterday +=1
#     # Il est arrivé 26 fois que le titre ne s’échange pas ni le jour même, 
#     # ni la veille

# # ----------------------------------------------------------------------
# # ----------------------------------------------------------------------
# # ----------------------------------------------------------------------


# # ----------------------------------------------------------------------
# # ----------VERIFICATION DES "NO TRADE" DANS LES ECHANGES D'OPTIONS----
# # ----------------------------------------------------------------------

# # Pour chaque ID Stock on va verifier si la difference de date entre chaque 
# # ligne du tableau excel est supérieures à 15j (car une option durait 15j). Si
# # c'est le cas, cela veut dire qu'il y a un moment ou l'option ne s'échangeait 
# # pas et donc qu'il y a un "no trade" pour calculer la volatilité historique.

# # On va parcourir le tableau tab_stock_id puis on va comparer l'id stock de ce
# # tableau a data[i, 'STOCK]. Si les 2 sont égaux alors on peut commencer le 
# # calcul de comparaison des dates

# tab_freq_trou = []

# for index1, stock in enumerate(tab_stock_id):


#     tab_stock_intermediaire = []
#     compteur = 0
    
#     for j in range(len(data)):

#         if stock == data.loc[j, 'STOCK']:
#             tab_stock_intermediaire.append(data.loc[j, 'DAY'])

#     for index in range(len(tab_stock_intermediaire) - 1):
        
#         if tab_stock_intermediaire[index] == tab_stock_intermediaire[index+1]:
#             pass
#         else:
            
#             if int(str(datetime.strptime(tab_stock_intermediaire[index+1], "%d/%m/%Y") 
#                       - datetime.strptime(tab_stock_intermediaire[index], "%d/%m/%Y"))[0]
#                       + str(datetime.strptime(tab_stock_intermediaire[index+1], "%d/%m/%Y") 
#                       - datetime.strptime(tab_stock_intermediaire[index], "%d/%m/%Y"))[1]) > 17:
                
#                 compteur +=1
               
#     tab_freq_trou.append(compteur / tab_nb_titre_ech[index1] * 100) 
    
    
# # On affiche graphiquement les fréquences de "trous" dans les données

# x = np.arange(24) 
# width = 0.4

# plt.bar(x, tab_freq_trou, width, color = 'black')
# plt.xticks(x, tab_stock_id, rotation = 'vertical')

# plt.axhline(y=15, color='r')

# plt.xlabel("ID Stock")
# plt.ylabel("Fréquence de 'no trade' dans les données (en %)")
# plt.title("")

# print("Moyenne des frequences:", np.mean(tab_freq_trou))
# quartiles = s.quantiles(tab_freq_trou, n=4)
# print("Quartiles for MIN are: " + str(quartiles))
# print("Ecart-type:", np.std(tab_freq_trou))

# # ----------------------------------------------------------------------
# # ----------------------------------------------------------------------
# # ----------------------------------------------------------------------



# # --------------AFFICHAGE GRAPHIQUE DU TAUX SANS RISQUE-----------------



# plt.plot(data.loc[:, 'Dates TSR'], data.loc[:, 'taux sans risque(1896-1914)'])

# plt.title("Dynamique des taux sur la période 1896-1914")

# # ----------------------------------------------------------------------
# # ----------------------------------------------------------------------
# # ----------------------------------------------------------------------


# # ----------------------------------------------------------------------
# # -----------------CALCUL DE LA VOLATILITÉ HISTORIQUE-------------------
# # ----------------------------------------------------------------------




# # On crée 11 groupes de 3 tableaux dans lesquels on met respectivement les prix
# # spot bi-hebdo, les volatilités sans dividendes et les volatilités avec dividendes
# tab_985 = []
# tab_rendement_sans_div_985 = []
# tab_moy_rend_sans_div_985 = []
# tab_vol_sans_div_moins_moy_985 = []
# tab_ecart_type_985 = []
# tab_vol_historique_985 = []


# tab_vol_avec_div_985 = []





# # Première formule: on va la calculer sans les dividendes premièrement, de 
# # manière logarithmique: la rentabilité r(t) = ln(P(t+1) / P(t)), puis en l'annualisant
# # Les données d'étendent majoritairement de 1896 à 1914

# # Ajout des prix des stocks et des dividendes

# for i in range(len(data_vol)):
    
#     if data_vol.loc[i, 'STOCK'] == 4211:
#         tab_985.append([data_vol.loc[i, 'PRICE'], data_vol.loc[i, 'Dividendes']])
        
# # Ajout du tableau des rendements
        

# for i in range(len(tab_985) - 1):
    
#     tab_rendement_sans_div_985.append(np.log(tab_985[i+1][0] / tab_985[i][0]))
    
# # On calcule la volatilité historique sur 1 an (i.e. 24 valeurs) donc pour que 
# # le code comprenne qu'on ne calcule que sur 24 valeurs à chaque fois, on parcours
# # le tableau des rendements par 24
    
    
# for X in [i for i in range(432) if i % 24 == 0]:
#     somme = 0
    
#     for x in range(X, X+24):
#         somme += tab_rendement_sans_div_985[x]
#     tab_moy_rend_sans_div_985.append(somme / 24)
    
    
# for index, X in enumerate([i for i in range(432) if i % 24 == 0]):
#     for x in range(X, X+24):
#         tab_vol_sans_div_moins_moy_985.append(tab_rendement_sans_div_985[x] - tab_moy_rend_sans_div_985[index])


# for X in [i for i in range(432) if i % 24 == 0]:
#     somme = 0
    
#     for x in range(X, X+24):
#         somme += np.square(tab_vol_sans_div_moins_moy_985[x])
#     tab_ecart_type_985.append(somme / 23)  

# for value in tab_ecart_type_985:
#     tab_vol_historique_985.append(np.sqrt(value))  
    
    
    
# print("moyenne:", np.mean(tab_vol_historique_985))

# quartiles = s.quantiles(tab_vol_historique_985, n=4)
# print("Quartiles for MIN are: " + str(quartiles))
# print("std:", np.std(tab_vol_historique_985))
    
# # Affichage graphique

# date = ["01/1896", "01/1897", "01/1898", "01/1899", "01/1900", "01/1901",
#             "01/1902", "01/1903", "01/1904", "01/1905", "01/1906", "01/1907",
#             "01/1908", "01/1909", "01/1910", "01/1911", "01/1912", "01/1913"]

# plt.plot(date, tab_vol_historique_985)
# plt.xticks(rotation = 'vertical')
# plt.title("Volatilité historique, stock 3927 - Rio Tinto")





# # ----------------------------------------------------------------------
# # ----------------------------------------------------------------------
# # ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# --------------------VOLATILITÉ HISTORIQUE/RÉALISÉE--------------------
# ----------------------------------------------------------------------

id_stock = 3927
fenetre = 730



# Fonction qui remplit les tableaux des prix et des dates

def rempli_tableau_prix_date(id_stock):
    
    tab_ECE = []
    dates = []
    
    for i in range(len(data_vol)):
    
        if data_vol.loc[i, 'STOCK'] == id_stock:
            tab_ECE.append([data_vol.loc[i, 'PRICE'], data_vol.loc[i, 'Dividendes']])
            dates.append(datetime.strptime(data_vol.loc[i, 'DAY'], "%d/%m/%Y"))
    
    return tab_ECE, dates

tab_ECE, dates = rempli_tableau_prix_date(id_stock)


# Ces deux fonctions permettent de définir les dates 2 ans avant / 2 ans après
# afin de pouvoir calculer les volatilités réalisées et historiques

def calcul_date_vol_deux_ans_avant(tab_date, fenetre):
    
    for index, date in enumerate(tab_date):
        
        j = index
        while tab_date[j] - tab_date[0] < timedelta(days=fenetre):
            j+=1
        return len(tab_date) - (j + 1) 
    

    
def calcul_date_vol_deux_ans_apres(tab_date, fenetre):
    
    for index, date in enumerate(tab_date):
        
        j = index
        while tab_date[0] - tab_date[j] < timedelta(days=fenetre):
            j+=1
        return len(tab_date) - (j + 1)





def valeur_date(id_stock, fenetre):
    
    tab_ECE, dates = rempli_tableau_prix_date(id_stock)
    
    date_deux_ans_avant = calcul_date_vol_deux_ans_avant(dates, fenetre)
    dates.reverse()
    date_deux_ans_apres = calcul_date_vol_deux_ans_apres(dates, fenetre)
    dates.reverse()
    
    return date_deux_ans_avant, date_deux_ans_apres

print(valeur_date(id_stock, fenetre))
dates.reverse()



# Calcul pur de la volatilité 2 ans avant et 2 ans après pour chaque valeur


def calcul_volatilite(id_stock, fenetre):
    
    tab_ECE, dates = rempli_tableau_prix_date(id_stock)

    date_deux_ans_avant, date_deux_ans_apres = valeur_date(id_stock, fenetre)
    


    date_avant = []
    date_apres = []




    tab_vol_historique_ECE_deuxAns_apres = []


    for i in range(0, date_deux_ans_apres+1):
        tab_rendement_sans_div_ECE_deuxAns_apres = []
        tab_vol_sans_div_moins_moy_ECE_deuxAns_apres = []
    

        j = i
    
    
        while dates[j+1] - dates[i] < timedelta(days=fenetre):
       
            tab_rendement_sans_div_ECE_deuxAns_apres.append(tab_ECE[j+1][0] / tab_ECE[j][0] - 1)
            j+=1
        somme = 0
        for k in range(len(tab_rendement_sans_div_ECE_deuxAns_apres)):
            tab_vol_sans_div_moins_moy_ECE_deuxAns_apres.append(tab_rendement_sans_div_ECE_deuxAns_apres[k]
                                                  - np.mean(tab_rendement_sans_div_ECE_deuxAns_apres))
        
            somme += np.square(tab_vol_sans_div_moins_moy_ECE_deuxAns_apres[k])

        tab_vol_historique_ECE_deuxAns_apres.append(np.sqrt(somme / (len(tab_vol_sans_div_moins_moy_ECE_deuxAns_apres) - 1)))
        date_apres.append(dates[i])

    tab_vol_historique_ECE_deuxAns_avant = []

    tab_ECE.reverse()
    dates.reverse()


    for i in range(0, date_deux_ans_avant+1):

        tab_rendement_sans_div_ECE_deuxAns_avant = []
        tab_vol_sans_div_moins_moy_ECE_deuxAns_avant = []
    

        j = i
    
    
        while dates[i] - dates[j+1] < timedelta(days=fenetre):
       
            tab_rendement_sans_div_ECE_deuxAns_avant.append(tab_ECE[j-1][0] / tab_ECE[j][0] - 1)
            j+=1
        
        somme = 0
        for k in range(len(tab_rendement_sans_div_ECE_deuxAns_avant)):
            tab_vol_sans_div_moins_moy_ECE_deuxAns_avant.append(tab_rendement_sans_div_ECE_deuxAns_avant[k]
                                                  - np.mean(tab_rendement_sans_div_ECE_deuxAns_avant))
        
            somme += np.square(tab_vol_sans_div_moins_moy_ECE_deuxAns_avant[k])

        tab_vol_historique_ECE_deuxAns_avant.append(np.sqrt(somme / (len(tab_vol_sans_div_moins_moy_ECE_deuxAns_avant) - 1)))
        date_avant.append(dates[i])
        
    return date_apres, tab_vol_historique_ECE_deuxAns_apres, date_avant, tab_vol_historique_ECE_deuxAns_avant



# date_apres, tab_vol_historique_ECE_deuxAns_apres, date_avant, tab_vol_historique_ECE_deuxAns_avant= calcul_volatilite(id_stock, fenetre)


# plt.subplot(212)
# plt.plot(date_apres, tab_vol_historique_ECE_deuxAns_apres, "b", label='2 ans après')


# plt.subplot(211)
# plt.plot(date_avant, tab_vol_historique_ECE_deuxAns_avant, "r", label='2 ans avant')


# plt.legend()
# plt.title("Volatilités réalisée et historique, fenêtre: " + str(fenetre) + " jours stock: " + str(id_stock))

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------    





















