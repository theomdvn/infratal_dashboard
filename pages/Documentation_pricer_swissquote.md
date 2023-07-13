Documentation_pricer_swissquote 

Ce code Python a été conçu pour calculer et afficher les frais de change pour une variété de devises, en se basant sur les taux de change actuels obtenus par l'API en ligne de Swiss Quote. Il utilise la bibliothèque Streamlit pour une interface utilisateur web interactive.

Modules importés:
- `streamlit`: Bibliothèque pour créer rapidement des applications web.
- `pandas`: Utilisé pour le traitement et la manipulation des données.
- `datetime`: Utilisé pour travailler avec les dates.
- `plotly.graph_objects` et `plotly_express`: Utilisé pour créer des visualisations interactives.
- `numpy`: Utilisé pour le calcul scientifique.
- `requests`: Utilisé pour effectuer des requêtes HTTP.
- `json`: Utilisé pour travailler avec des données JSON.

Le code crée d'abord des listes de devises classées par catégorie (major, minor, emerging). Ensuite, il crée un dictionnaire qui mappe les codes de devise aux codes de pays correspondants.

La fonction `fees_SQ` calcule les frais de change basés sur les devises et la quantité. Les frais varient en fonction de la catégorie de la devise et de la quantité.

La fonction `conversion` effectue une conversion de devise en récupérant les taux de change actuels à partir d'un service en ligne. Il utilise le module `requests` pour effectuer une requête HTTP vers l'API de conversion de devises, et renvoie le montant converti.

La fonction `rate_TAL_to_currency` calcule le taux de conversion de la devise TAL vers une autre devise en utilisant des proportions fixes et le taux de change actuel.

La fonction `rate_currency_to_TAL` fait l'inverse, elle convertit une autre devise en TAL.

La fonction `conversion_fees_SQ` effectue une conversion de devise tout en prenant en compte les frais de change calculés par la fonction `fees_SQ`.

Ensuite, le code crée une interface utilisateur avec Streamlit. Il y a une colonne de gauche pour entrer des montants en TAL et une colonne de droite pour sortir des montants de TAL. Les utilisateurs peuvent sélectionner la devise, entrer la quantité et voir les résultats de la conversion, y compris les frais. Les données sont affichées sous forme de tableaux et de graphiques.

Dans la colonne de gauche, le code calcule et affiche les montants en diverses devises correspondant à une quantité donnée de TAL. Les frais de conversion sont également calculés et affichés. Dans la colonne de droite, le code fait l'inverse, convertissant une quantité donnée de TAL en une autre devise.

Ce script semble faire partie d'une application plus grande pour le trading de devises, fournissant un moyen pour les utilisateurs de calculer les frais de conversion et les montants convertis pour diverses devises.