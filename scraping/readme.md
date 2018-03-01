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

On obtient ce fichier en exécutant la commande `scrapy runspider articles.py`.

## Traitement pour chaque article

Le fichier `ieee.py` contient la spider pour obtenir toutes les informations (e.g.: auteurs, date, mots-clés, etc.) sur chaques articles.
On exécute ce traitement via la commande `scrapy runspider ieee.py`.

Le premier élément du fichier JSON de sortie est le suivant (avec une apparance modifiée) :

```json
 {
    "id": "5666039",
    "url": "http://ieeexplore.ieee.org/document/5666039/",
    "titre": "Variable renewable generation and grid operation",
    "date": "24-28 Oct. 2010",
    "type": "conference",
    "lieu-conference": "Hangzhou, China",
    "nb-citations": 2,
    "nb-vues": 561,
    "resume": "With the advancement in wind and solar technology, now large wind-farms and PV systems are being integrated in the power system. This brings new level of challenges for both protection and planning engineers. This paper reviews the renewable power generation technologies available in the current market and challenges in integrating these in the grid. An introduction is provided for the renewable energy available; including wind, solar and ocean etc. This paper also discusses an example of the large renewable project including system planning; establishing the type of generation sources available and discussion of benefits. The paper also discusses the information required for the planning engineer, types of study and challenges before integrating in the existing system. In the end this paper discusses a real life example and sub-synchronous resonance interaction between wind-farm and series capacitor.",
    "mots-cles": [
        "Generators",
        "Rotors",
        "Wounds",
        "Planning",
        "Reliability",
        "Wind turbines",
        "Automatic voltage control"
    ],
    "auteurs": [
        {
            "nom-auteur": "Amit Jain",
            "infos-auteur": "Power System Research Center at IIIT, Gachibowli, Hyderabad, India"
        },
        {
            "nom-auteur": "Kamal Garg",
            "infos-auteur": "Schweitzer Engineering Laboratories, Pullman, WA USA"
        }
    ]
},
