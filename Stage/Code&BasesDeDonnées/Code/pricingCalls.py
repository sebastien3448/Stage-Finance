# # -*- coding: utf-8 -*-
# """
# Created on Fri Jun  4 12:22:39 2021

# @author: HP
# """



from math import sqrt, exp, log
import matplotlib.pyplot as plt
from scipy.stats import norm
import pandas as pd
import numpy as np
from datetime import datetime


data = pd.read_excel("C:\\Users\\HP\\Desktop\\Stage\\Code&BasesDeDonnées\\Données\\Stat11StocksBis.xlsx", sheet_name= "Feuil1", usecols=[0, 1, 3, 6, 7, 8, 10, 11, 12, 15, 19, 23, 24])





# ------------------------CALL PRICE-------------------------------------
# ---------------------------FOR-----------------------------------------
# ----------------------BLACK AND SCHOLES--------------------------------


#   Function to calculate the values of d1 and d2 as well as the call
#   price.  

def d_BS(sigma, S, K, r, t, q):

    d1 = 1 / (sigma * sqrt(t)) * ( log(S/K) + (r  - q + sigma**2 / 2) * t)

    d2 = 1 / (sigma * sqrt(t)) * ( log(S/K) + (r  - q - sigma**2 / 2) * t)

    return d1, d2


def call_price_BS(sigma, S, K, r, t, q, d1, d2):

    C = exp(-r * t) * (S * exp((r - q) * t) * norm.cdf(d1)  - norm.cdf(d2) * K) 

    return C

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------




# ------------------------CALL PRICE-------------------------------------
# ---------------------------FOR-----------------------------------------
# -------------------------BACHELIER-------------------------------------


def d_bach(sigma, S, K, r, t, q):
    
    dn = (exp((q - r) * t) * S - K) / (sigma * S * exp((q - r) * t ) * sqrt(t))
    
    return dn


def call_price_bach(sigma, S, K, r, t, q, dn):
    
    try:    
        C = (exp((q - r) * t) * S - K) * norm.cdf(dn) + S * sigma * exp((q - r) * t) * sqrt(t) * norm.pdf(dn)
    except OverflowError:
        C = 0
        
    return C




#  Option parameters

# S = 1660

# K = 1695

# t = 15/365

# r = 2.89855072463768 / 100

# C0 = 10


def newton_raphson(S, K, r, t, q = 0, C0 = 0, method = 0):
    
    # if method = 0, we use Black Scholes
    # if method = 1, we use Bachelier
    
    tol = 1e-3

    epsilon = 1


    #  Variables to log and manage number of iterations

    count = 0

    max_iter = 1000


    #  We need to provide an initial guess for the root of our function

    vol = 0.25


    while epsilon > tol:

        #  Count how many iterations and make sure while loop doesn't run away

        count += 1

        if count >= max_iter:

            break;


        #  Log the value previously calculated to computer percent change

        #  between iterations

        orig_vol = vol

        if method == 0:
            
            #  Calculate the vale of the call price

            d1, d2 = d_BS(vol, S, K, r, t, q)
        

            function_value = call_price_BS(vol, S, K, r, t, q, d1, d2) - C0
        


            #  Calculate vega, the derivative of the price with respect to

            #  volatility
    

            vega = S * norm.pdf(d1) * sqrt(t) * exp(-q * t)
            
            
            
        if method == 1:
            
            dn = d_bach(vol, S, K, r, t, q)
            
            function_value = call_price_bach(vol, S, K, r, t, dn, q) - C0
                        
            vega = S * sqrt(t) * norm.pdf(dn)
            
            
            
        #  Update for value of the volatility

        vol = -function_value / vega + vol


        #  Check the percent change between current and last iteration

        epsilon = abs( (vol - orig_vol) / orig_vol )

    
    return vol

# S, K, r, t, q, Co, met

# print(newton_raphson(1690, 1695, 0.0289, 15/365, 50/1660, 10, 0))





# 1ère étape on va remplir les SPOT_PRICE MIN et MAX vides 
# avec les cours de compensation

for i in range(len(data)):
    
    if np.isnan(data.loc[i, 'SPOT_PRICE_MIN']):
        # np.isnan verifie si il y a la valeur "Not a Number" dans la liste
        data.loc[i, 'SPOT_PRICE_MIN'] = data.loc[i, 'COURS_COMPENS']
        data.loc[i, 'SPOT_PRICE_MAX'] = data.loc[i, 'COURS_COMPENS']

 
# Création de tableau pour mettre les volatilité implicite de chaque call ainsi que leurs
# prix théorique selon BS   



##----------------------------------------------------------------------
##---------------------------BLACK AND SCHOLES--------------------------
##----------------------------------------------------------------------

def calcul_vol_impli_BS(id_stock):


    implied_vol_tab_BS = []
    true_call_price_tab_BS = []




    tab_implied_vol_un_stock = []
    tab_date_vol_un_stock = []


    tab_maturite = []

    compteur_nan = 0


    # Problème les 930 premières dates sont avant 1900 donc excel ne gère pas 
    # le format date, nous les convertissons en date ici
    #EDIT: pour pas compliquer les potentiels prochaines modifications du code 
    #je ramène tous les dates excel en format texte et je les convertis ici

    for i in range(len(data)):
        
    
        ##--------------1ère étape: convertion des dates au même format-----------
    
    
        debut = data.loc[i, 'DAY']
        fin = data.loc[i, 'EXACT_SETDATE']
    
        # Sur ces deux lignes on convertit les données textes de excel en date 
        date_debut = datetime.strptime(debut, '%d/%m/%Y')
        date_fin = datetime.strptime(fin, '%d/%m/%Y')
        
        # On prend les deux premiers charactères de la date (qui correspond au chiffre du jour: 
        # exemple: dans la chaine "15 jours" on prendra 1 et 5 que l'on convertit ensuite en 
        # int
        temps = int(str(date_fin - date_debut)[0] + str(date_fin - date_debut)[1])
        tab_maturite.append(temps)

    
    
                 
        ##--------------2ème étape: calcul de la volatilité implicite pour tous les stocks-----------

        # On remplit le tableau des volatilités implicites
        implied_vol =  newton_raphson(data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'TAUX SANS RISQUE']/100, temps/365, (data.loc[i, 'DIVIDENDES ANNUALISÉS'] * temps/365)/data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'OPTION_VALUE'], 0)
        implied_vol_tab_BS.append(implied_vol)
 
   
        d1, d2 = d_BS(implied_vol, data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'TAUX SANS RISQUE']/100, temps/365, (data.loc[i, 'DIVIDENDES ANNUALISÉS'] * temps/365)/data.loc[i, 'SPOT_PRICE_MIN'])
        # On remplit le tableau des Call BS
        true_call_price = call_price_BS(implied_vol, data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'TAUX SANS RISQUE']/100, temps/365, (data.loc[i, 'DIVIDENDES ANNUALISÉS'] * temps/365)/data.loc[i, 'SPOT_PRICE_MIN'], d1, d2)    
        true_call_price_tab_BS.append(true_call_price)
    
        ###
        
        ##--------------3ème étape: Récupération de la vol implicite pour un seul stock-----------
    
        if data.loc[i, 'STOCK'] == id_stock:
            tab_implied_vol_un_stock.append(implied_vol)
            tab_date_vol_un_stock.append(datetime.strptime(data.loc[i, 'DAY'], "%d/%m/%Y"))
       
        
        
        
        ##----------Annexe: compte le nombre de fois ou la descente de Newton n'a pas convergée
        if np.isnan(true_call_price_tab_BS[i]):
            compteur_nan += 1
            print("erreur ligne", i + 2, "du tableau excel")
            
  
            
  
    ##--------------4ème étape: Affichage graphique de la vol impli pour un stock choisi-----------   
    vol_impli = []
    date = []
        
    for i in range(len(tab_date_vol_un_stock)):
    
        if tab_date_vol_un_stock[i] not in date: 
                date.append(tab_date_vol_un_stock[i])
                vol_impli.append(tab_implied_vol_un_stock[i])

       
    print(compteur_nan)

    

    return vol_impli, date



#calcul_vol_impli_BS(985)



##----------------------------------------------------------------------
##-------------------------------BACHELIER------------------------------
##----------------------------------------------------------------------
    

def calcul_vol_impli_Bach(id_stock):
    
    # Les étapes sont les mêmes que celles décrites dans la méthode pour 
    # calculer la vol implicite selon la méthode de Black&Scholes


    implied_vol_tab_B = []
    true_call_price_tab_B = []


    tab_implied_vol_un_stock = []
    tab_date_vol_un_stock = []


    tab_maturite = []

    compteur_nan = 0


    # Problème les 930 premières dates sont avant 1900 donc excel ne gère pas 
    # le format date, nous les convertissons en date ici
    #EDIT: pour pas compliquer les potentiels prochaines modifications du code 
    #je ramène tous les dates excel en format texte et je les convertis ici

    for i in range(len(data)):
    #edit il y a une matherror sur les dernières lignes de l'excel quand je veux 
    #calculer la vol implicite selon le modèle de bachelier, je n'ai pas eu le 
    #temps d'aller le verifier dans le stage
    
    
        debut = data.loc[i, 'DAY']
        fin = data.loc[i, 'EXACT_SETDATE']
    
        # Sur ces deux lignes on convertit les données textes de excel en date 
        date_debut = datetime.strptime(debut, '%d/%m/%Y')
        date_fin = datetime.strptime(fin, '%d/%m/%Y')
        
        # On prend les deux premiers charactères de la date (qui correspond au chiffre du jour: 
        # exemple: dans la chaine "15 jours" on prendra 1 et 5 que l'on convertit ensuite en 
        # int
        temps = int(str(date_fin - date_debut)[0] + str(date_fin - date_debut)[1])
        tab_maturite.append(temps)

                 
            
    
    

        # On remplit le tableau des volatilités implicites
        implied_vol =  newton_raphson(data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'TAUX SANS RISQUE']/100, temps/365, (data.loc[i, 'DIVIDENDES ANNUALISÉS'] * temps/365)/data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'OPTION_VALUE'], 1)
        implied_vol_tab_B.append(implied_vol)
 
   
        dn = d_bach(implied_vol, data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'TAUX SANS RISQUE']/100, temps/365, (data.loc[i, 'DIVIDENDES ANNUALISÉS'] * temps/365)/data.loc[i, 'SPOT_PRICE_MIN'])
        # On remplit le tableau des Call BS
        true_call_price_B = call_price_bach(implied_vol, data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'TAUX SANS RISQUE']/100, temps/365, (data.loc[i, 'DIVIDENDES ANNUALISÉS'] * temps/365)/data.loc[i, 'SPOT_PRICE_MIN'], dn)    
        true_call_price_tab_B.append(true_call_price_B)


        if data.loc[i, 'STOCK'] == id_stock:
            tab_implied_vol_un_stock.append(implied_vol)
            tab_date_vol_un_stock.append(datetime.strptime(data.loc[i, 'DAY'], "%d/%m/%Y"))
            
            

    
        if np.isnan(true_call_price_tab_B[i]):
            compteur_nan += 1
            print("erreur ligne", i + 2, "du tableau excel")
            
            
        
    vol_impli = []
    date = []
        
    for i in range(len(tab_date_vol_un_stock)):
    
        if tab_date_vol_un_stock[i] not in date: 
            if tab_implied_vol_un_stock[i] > -5:
                date.append(tab_date_vol_un_stock[i])
                vol_impli.append(tab_implied_vol_un_stock[i])

    print(compteur_nan)

    return vol_impli, date
    
#calcul_vol_impli_Bach(985)    





