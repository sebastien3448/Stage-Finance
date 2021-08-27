# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 10:40:40 2021

@author: HP
"""

import pricingCalls
import statistiquesDescriptives11Stocks
import matplotlib.pyplot as plt

# tableau_stock = [985, 1398, 2471, 3927, 4211, 4313, 4677, 4843, 5272, 6080, 10749]

id_stock = 985
fenetre = 730

vol_impli, date = pricingCalls.calcul_vol_impli_BS(id_stock)
plt.plot(date, vol_impli)
plt.title("Volatilté implicite selon le modèle de B&S pour le stock: " + str(id_stock))

# date_apres, tab_vol_historique_ECE_deuxAns_apres, date_avant, tab_vol_historique_ECE_deuxAns_avant = statistiquesDescriptives11Stocks.calcul_volatilite(id_stock, fenetre)


# plt.subplot(212)
# plt.plot(date_apres, tab_vol_historique_ECE_deuxAns_apres, "b", label='2 ans après')
# plt.legend()


# plt.subplot(211)
# plt.plot(date_avant, tab_vol_historique_ECE_deuxAns_avant, "r", label='2 ans avant')
# plt.legend()

# plt.title("Volatilités réalisée et historique, fenêtre: " + str(fenetre) + " jours stock: " + str(id_stock))
