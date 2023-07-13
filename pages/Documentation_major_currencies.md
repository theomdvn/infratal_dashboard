Documentation_Major_Currencies

Ce script Python utilise Streamlit pour créer une application web qui analyse et visualise des données financières. Voici une description détaillée de ce que fait chaque section de votre code :

1. **Importation des bibliothèques** : Le code importe les bibliothèques nécessaires. Cela comprend `streamlit` pour construire l'application web, `pandas` pour le traitement des données, `datetime` pour manipuler les dates, `plotly.graph_objects` et `plotly_express` pour les visualisations graphiques, `numpy` pour les opérations numériques, `requests` pour les requêtes HTTP et `json` pour manipuler les objets JSON. Enfin, il importe une base de données depuis un module local appelé `Home`.

2. **Prétraitement des données** : Le code effectue plusieurs transformations sur la base de données. Il convertit `USDEUR` en `EURUSD`, calcule `GLDEUR` à partir de `GLDUSD` et `USDEUR`, supprime les colonnes commençant par `USD` et remplace `EUR` dans les noms de colonnes. Il supprime également les colonnes `TALUSD` et `GLDUSD`.

3. **Interface Streamlit** : Le code crée trois colonnes dans l'interface Streamlit et ajoute une image au centre.

4. **Fonction `XXXTAL`** : Cette fonction calcule le rapport inverse entre une devise donnée et `TAL`.

5. **Filtre de date** : Les utilisateurs peuvent sélectionner une date de début à partir de la barre latérale de Streamlit. Les données sont ensuite filtrées pour inclure uniquement les dates entre la date de début sélectionnée et la veille.

6. **Création du premier graphique (`fig`)** : Le code crée un graphique Plotly qui illustre la résilience de `sTAL` face à la dépréciation de différentes devises. Il trace une ligne de base (zéro) pour `sTAL` et superpose des graphiques de variations pour chaque devise par rapport à `sTAL`.

7. **Création du second graphique (`fig2`)** : De la même manière, le code crée un autre graphique Plotly qui montre comment `sTAL` se défend contre la dépréciation de la valeur dans les devises des marchés émergents.

8. **Affichage des graphiques** : Enfin, le code affiche les deux graphiques dans l'application Streamlit.

Notez que ce code suppose que certaines colonnes spécifiques existent dans la base de données, comme `TAL`, `USD`, `CHF`, `GBP`, `JPY`, `CNY`, `SGD`, `BRL`, `CAD`, `TRY`, `INR`, `KRW`, `MXN`, et `ZAR`. Si ces colonnes ne sont pas présentes dans votre base de données, le code pourrait ne pas fonctionner correctement.