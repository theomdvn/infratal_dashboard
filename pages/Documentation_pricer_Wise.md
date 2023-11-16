Documentation_pricer_Wise

Ce script Python sert à une application de conversion de devises nommée "Pricer Wise". Il utilise le package Streamlit pour créer une interface utilisateur web interactive, ainsi que plusieurs autres packages pour effectuer des opérations de données, de visualisation et de requêtes réseau.

**Importations:**
- `streamlit`: Un framework pour créer des applications web interactives.
- `pandas`: Une bibliothèque pour la manipulation de données.
- `datetime`: Un module pour travailler avec des dates et des heures.
- `plotly.graph_objects` et `plotly_express`: Des bibliothèques pour la création de graphiques interactifs.
- `numpy`: Une bibliothèque pour les calculs scientifiques.
- `requests`: Un module pour faire des requêtes HTTP.
- `json`: Un module pour manipuler les données JSON.

**Fonctions:**

- `conversion(from_currency, to_currency, amount)`: Convertit une certaine quantité d'une devise en une autre en utilisant l'API de Boursorama.

- `rate_TAL_to_currency(currency)`: Calcule le taux de conversion de TAL à une autre devise en considérant différents taux de change.

- `rate_currency_to_TAL(currency)`: Calcule le taux de conversion d'une devise à TAL.

- `conversion_with_fees(from_currency, to_currency, amount)`: Convertit une certaine quantité d'une devise en une autre en utilisant l'API de Wise et retourne aussi les frais de conversion.

**Application Streamlit:**

Le script crée une interface utilisateur web avec deux colonnes principales.

- Colonne de gauche : Contient une interface pour convertir une certaine quantité d'une devise en TAL. L'utilisateur peut choisir la devise et la quantité à convertir. L'application affiche alors le montant converti en TAL, en tenant compte des différents frais de conversion et de commission.

- Colonne de droite : Contient une interface pour convertir une certaine quantité de TAL en une autre devise. L'utilisateur peut choisir la devise de sortie et la quantité de TAL à convertir. L'application affiche alors le montant converti en devise de sortie, en tenant compte des différents frais de conversion et de commission.

L'application affiche aussi un avertissement sur le total des frais de conversion et de commission pour les deux opérations de conversion.

En outre, l'application offre la possibilité d'afficher les détails des conversions (par exemple, le montant converti pour chaque devise, les frais de conversion pour chaque devise, etc.) dans un tableau de données. 

Les fonctions `conversion_with_fees()` et `conversion()` effectuent des appels à des API externes, il est donc possible que ces fonctions génèrent des avertissements si l'API ne répond pas correctement.