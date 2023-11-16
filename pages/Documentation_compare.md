# Documentation du Code Python

Ce script Python utilise le module Streamlit pour créer une application Web interactive pour comparer différents taux de change avec TAL (qui semble être une certaine forme de devise ou d'actif). L'application permet aux utilisateurs de sélectionner une plage de dates, de choisir une devise à protéger, et éventuellement de comparer TAL à une autre devise. Elle produit également des statistiques pour les différentes devises sélectionnées.

## Importation des modules nécessaires

```python
import streamlit as st
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
import plotly_express as px
import numpy as np
from Home import database
```

## Fonctions d'opérations de devises

```python
def anyrate(df,from_currency,to_currency):
    #Calcule le taux de change entre deux devises
    x = (1/df[from_currency])*df[to_currency]
    return x

def XXXTAL(df, from_currency):
    #Calcule le taux de change entre une devise et TAL
    x = (1/df[from_currency])*(1/df['TAL'])
    return x

def qtytal(df, from_currency):
    #Calcule la valeur de 1000 TAL en une autre devise
    x = 1000*(df[from_currency])*df['TAL'][0]
    return x
```

## Préparation des données

Les données sont chargées depuis une base de données et sont préparées pour l'analyse. Cela comprend la manipulation de noms de colonnes, le retrait de certaines colonnes, et la création de nouvelles colonnes basées sur les taux de change entre différentes devises.

## Sélection de la plage de dates

Les utilisateurs peuvent sélectionner une plage de dates pour l'analyse. Les dates sont converties en chaînes de caractères pour une utilisation ultérieure.

## Sélection de la devise

Les utilisateurs peuvent choisir la devise qu'ils souhaitent protéger. Ils ont également la possibilité de comparer TAL à une autre devise.

## Création du graphique

Le graphique est créé en utilisant Plotly. Si l'utilisateur a choisi de comparer TAL à une autre devise, une autre trace est ajoutée au graphique.

## Affichage des résultats

Le graphique est affiché à l'aide de Streamlit. De plus, certaines statistiques sont calculées et affichées, telles que le rendement moyen, l'écart-type, la VaR (Value at Risk), l'ES (Expected Shortfall), et le maximum Drawdown.

Des informations supplémentaires sont également fournies pour aider les utilisateurs à comprendre les statistiques.

## Affichage des statistiques

Les statistiques pour chaque devise sont affichées dans un tableau. Si l'utilisateur a choisi de comparer TAL à une autre devise, des statistiques supplémentaires sont calculées et affichées.