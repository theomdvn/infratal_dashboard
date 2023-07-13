Documentation_protect

Ce script Python sert à une application nommée "Protect with TAL" qui utilise le package Streamlit pour créer une interface utilisateur web interactive. L'application permet de convertir différentes devises en TAL, une devise de référence, et inversement.

**Importations :**

- `streamlit` : Un framework pour créer des applications web interactives.
- `plotly.graph_objects` et `plotly_express` : Des bibliothèques pour la création de graphiques interactifs.
- `pandas` : Une bibliothèque pour la manipulation de données.
- `requests` et `json` : Des modules pour faire des requêtes HTTP et manipuler les données JSON.
- `database` et `currency_country_map` : Des modules personnalisés qui fournissent des données nécessaires à l'application.

**Fonctions :**

- `conversion(from_currency, to_currency, amount)` : Convertit une certaine quantité d'une devise en une autre en utilisant l'API de Boursorama.

- `rate_TAL_to_currency(currency)` : Calcule le taux de conversion de TAL à une autre devise.

- `rate_currency_to_TAL(currency)` : Calcule le taux de conversion d'une devise à TAL.

**Interface utilisateur Streamlit :**

Le script crée une interface utilisateur web avec deux colonnes principales :

- Colonne de gauche : Permet à l'utilisateur de choisir une devise et une quantité à convertir en TAL. L'application affiche alors le montant converti en TAL. De plus, elle présente un graphique en camembert montrant la répartition du montant converti en différentes devises et or. L'utilisateur a également la possibilité d'afficher ces informations dans un tableau de données.

- Colonne de droite : Permet à l'utilisateur de choisir une quantité de TAL à convertir en une autre devise. L'application affiche alors le montant converti dans la devise choisie. De même, elle présente un graphique en camembert montrant la répartition du montant converti en différentes devises et or. L'utilisateur a également la possibilité d'afficher ces informations dans un tableau de données.

Les fonctions `conversion()`, `rate_TAL_to_currency()`, et `rate_currency_to_TAL()` effectuent des appels à des API externes, il est donc possible que ces fonctions génèrent des avertissements si l'API ne répond pas correctement.