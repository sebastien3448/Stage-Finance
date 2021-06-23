# # -*- coding: utf-8 -*-
# """
# Created on Fri Jun  4 12:22:39 2021

# @author: HP
# """



from math import sqrt, exp, log

from scipy.stats import norm



# ------------------------CALL PRICE-------------------------------------
# ---------------------------FOR-----------------------------------------
# ----------------------BLACK AND SCHOLES--------------------------------


#   Function to calculate the values of d1 and d2 as well as the call
#   price.  

def d_BS(sigma, S, K, r, t):

    d1 = 1 / (sigma * sqrt(t)) * ( log(S/K) + (r + sigma**2 / 2) * t)

    d2 = d1 - sigma * sqrt(t)

    return d1, d2


def call_price_BS(sigma, S, K, r, t, d1, d2):

    C = norm.cdf(d1) * S - norm.cdf(d2) * K * exp(-r * t)

    return C

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------




# ------------------------CALL PRICE-------------------------------------
# ---------------------------FOR-----------------------------------------
# -------------------------BACHELIER-------------------------------------


def d_bach(sigma, S, K, r, t):
    
    dn = (exp(r * t) * S - K) / (sigma * S * exp(r * t ) * sqrt(t))
    
    return dn


def call_price_bach(sigma, S, K, r, t, dn):
    
     C = (exp(r * t) * S - K) * norm.cdf(dn) + S * sigma * exp(r * t) * sqrt(t) * norm.pdf(dn)
     
     return C




#  Option parameters

# S = 1660

# K = 1695

# t = 15/365

# r = 2.89855072463768 / 100

# C0 = 10



def newton_raphson(S, K, r, t, C0, method):
    
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

            d1, d2 = d_BS(vol, S, K, r, t)
        

            function_value = call_price_BS(vol, S, K, r, t, d1, d2) - C0
        


            #  Calculate vega, the derivative of the price with respect to

            #  volatility
    

            vega = S * norm.pdf(d1) * sqrt(t)
            
            
            
        if method == 1:
            
            dn = d_bach(vol, S, K, r, t)
            
            function_value = call_price_bach(vol, S, K, r, t, dn) - C0
                        
            vega = S * sqrt(t) * norm.pdf(dn)
            
            
            
        #  Update for value of the volatility

        vol = -function_value / vega + vol


        #  Check the percent change between current and last iteration

        epsilon = abs( (vol - orig_vol) / orig_vol )

    
    return vol



import pandas as pd
import numpy as np
from datetime import datetime


data = pd.read_excel("C:\\Users\\HP\\Desktop\\RenduStage\\base_de_donnees_stage.xlsx", sheet_name= "Exporter la feuille de calcul", usecols=[0, 1, 3, 6, 7, 8, 10, 11, 12, 15, 19, 22])


# 1ère étape on va remplir les SPOT_PRICE MIN et MAX vides 
# avec les cours de compensation

for i in range(len(data)):
    
    if np.isnan(data.loc[i, 'SPOT_PRICE_MIN']):
        # np.isnan verifie si il y a la valeur "Not a Number" dans la liste
        data.loc[i, 'SPOT_PRICE_MIN'] = data.loc[i, 'COURS_COMPENS']
        data.loc[i, 'SPOT_PRICE_MAX'] = data.loc[i, 'COURS_COMPENS']

 
# Création de tableau pour mettre les volatilité implicite de chaque call ainsi que leurs
# prix théorique selon BS   

implied_vol_tab = []
true_call_price_tab = []
call_reel = []


# Problème les 930 premières dates sont avant 1900 donc excel ne gère pas 
# le format date, nous les convertissons en date ici

for i in range(930):
    
    debut = data.loc[i, 'DAY']
    fin = data.loc[i, 'EXACT_SETDATE']
    
    # Sur ces deux lignes on convertit les données textes de excel en date 
    date_debut = datetime.strptime(debut, '%d/%m/%Y')
    date_fin = datetime.strptime(fin, '%d/%m/%Y')
    # On prend les deux premiers charactères de la date (qui correspond au chiffre du jour: 
    # exemple: dans la chaine "15 jours" on prendra 1 et 5 que l'on convertit ensuite en 
    # int
    temps = int(str(date_fin - date_debut)[0] + str(date_fin - date_debut)[1])

    # On remplit le tableau des volatilités implicites
    implied_vol =  newton_raphson(data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'taux']/100, temps/365, data.loc[i, 'OPTION_VALUE'], 0)
    implied_vol_tab.append(implied_vol)
 
   
    d1, d2 = d_BS(implied_vol, data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'taux']/100, temps/365)
    # On remplit le tableau des Call BS
    true_call_price = call_price_BS(implied_vol, data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'taux']/100, temps/365, d1, d2)    
    true_call_price_tab.append(true_call_price)
    call_reel.append(data.loc[i, 'OPTION_VALUE'])


# Ici excel a les format date donc manip précédente inutile
for i in range(930, len(data)):
    
    
    
    debut = data.loc[i, 'DAY']
    fin = data.loc[i, 'EXACT_SETDATE']
    temps = int(str(fin - debut)[0] + str(fin - debut)[1])


    implied_vol =  newton_raphson(data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'taux']/100, temps/365, data.loc[i, 'OPTION_VALUE'], 0)
    implied_vol_tab.append(implied_vol)
 
   
    d1, d2 = d_BS(implied_vol, data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'taux']/100, temps/365)
        
    true_call_price = call_price_BS(implied_vol, data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'taux']/100, temps/365, d1, d2)    
    true_call_price_tab.append(true_call_price)
    call_reel.append(data.loc[i, 'OPTION_VALUE'])



# for i in range(930):
    
#     call_reel.append(data.loc[i, 'OPTION_VALUE'])
    
#     debut = data.loc[i, 'DAY']
#     fin = data.loc[i, 'EXACT_SETDATE']
    
#     # Sur ces deux lignes on convertit les données textes de excel en date 
#     date_debut = datetime.strptime(debut, '%d/%m/%Y')
#     date_fin = datetime.strptime(fin, '%d/%m/%Y')
#     # On prend les deux premiers charactères de la date (qui correspond au chiffre du jour: 
#     # exemple: dans la chaine "15 jours" on prendra 1 et 5 que l'on convertit ensuite en 
#     # int
#     temps = int(str(date_fin - date_debut)[0] + str(date_fin - date_debut)[1])

#     # On remplit le tableau des volatilités implicites
#     implied_vol =  newton_raphson(data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'taux']/100, temps/365, data.loc[i, 'OPTION_VALUE'], 1)
#     implied_vol_tab.append(implied_vol)
 
   
#     dn = d_bach(implied_vol, data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'taux']/100, temps/365)
#     # On remplit le tableau des Call BS
#     true_call_price = call_price_bach(implied_vol, data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'taux']/100, temps/365, dn)    
#     true_call_price_tab.append(true_call_price)


# # Ici excel a les format date donc manip précédente inutile
# for i in range(930, len(data)):
    
    
    
#     debut = data.loc[i, 'DAY']
#     fin = data.loc[i, 'EXACT_SETDATE']
#     temps = int(str(fin - debut)[0] + str(fin - debut)[1])


#     implied_vol =  newton_raphson(data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'taux']/100, temps/365, data.loc[i, 'OPTION_VALUE'], 1)
#     implied_vol_tab.append(implied_vol)
 
   
#     dn = d_bach(implied_vol, data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'taux']/100, temps/365)
        
#     true_call_price = call_price_bach(implied_vol, data.loc[i, 'SPOT_PRICE_MIN'], data.loc[i, 'MIN'] - data.loc[i, 'OPTION_VALUE'], data.loc[i, 'taux']/100, temps/365, dn)    
#     true_call_price_tab.append(true_call_price)
    
    
# Comparaison Call_BS vs real_call

ecart_relatif = []
    
for i in range(len(true_call_price_tab)): 
      if not np.isnan(true_call_price_tab[i]):
          ecart_relatif.append(abs(true_call_price_tab[i] - data.loc[i, 'OPTION_VALUE']) / data.loc[i, 'OPTION_VALUE'] * 100)

print("L'écart relatif est de:", np.mean(ecart_relatif), "%")





