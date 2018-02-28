Scraping
========

## Lister les articles

Le fichier `articles.py` contient la spider pour obtenir la liste des numéros d'articles.
Cette liste est disponible dans le fichier `articles.csv`, elle est sous la forne :

```csv
id
1
2
3
```

On obtient ce fichier en exécutant la commande `scrapy runspider articles.py -o articles.csv`.

## Traitement pour chaque article

Le fichier `ieee.py` contient la spider pour obtenir toutes les informations (e.g.: auteurs, date, mots-clés, etc.) sur chaque articles.
On exécute ce traitement via la commande `scrapy runspider ieee.py`.
