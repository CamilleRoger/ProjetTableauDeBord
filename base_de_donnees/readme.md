Base de données
=========


## La base de données

Notre base de données utilisiée est une base SQL Server qui se trouve dans 
un [docker](https://fr.wikipedia.org/wiki/Docker_(logiciel)).   
Installation réalisée en suivant ce tutoriel : https://docs.microsoft.com/fr-fr/sql/linux/quickstart-install-connect-docker


## Création de la base

Le fichier *creation.sql* contient le scrit de création de la base de données.


## Insertion des données

Le fichier *insertions.py* contient pour le moment uniquement la connexion avec la base de données.
Il devra contenir le traitement qui permettra d'insérer dans la base les informations récoltées depuis le site (en prétraitant les champs contenant plusieurs éléments séparés par des virgules). Ces informations
sont contenues dans le fichiers *ieee.json*.

