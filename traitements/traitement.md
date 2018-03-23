BD :
Auteurs(id_auteur, nom_auteur, pays_auteur, infos_auteur)
Ecrire(rang_auteur_article, id_article, id_auteur)
Articles(id_article,resume,nombre_vue,nombre_citation,url,titre,type,ville,etat,pays,date,revue)
Contenir(rang_mot_cle_article, id_article, id_mot_cle)
Mot_cles(mot_cle)

Localisation :
- par pays
- par ville (seulement pour les conférences)
- par institut (seulement pour les conférences)

Temps :
- par an
- par mois
- par jour

Métier :
- par revue
- par article
- par auteur

-- Nombre d'article
-- Localisation
SELECT pays, count(id_article) as occurences
FROM Articles
GROUP BY pays
ORDER By occurences;

SELECT ville, count(id_article) as occurences
FROM Articles
WHERE type = "conference"
GROUP BY ville
ORDER By occurences;

SELECT etat, count(id_article) as occurences
FROM Articles
WHERE type = "conference"
GROUP BY etat
ORDER By occurences;

-- Temps (date = AAAA-MM-JJ HH:MM:SS)
SELECT YEAR(date) as annee, count(id_article) as occurences
FROM Articles
GROUP BY annee
ORDER By occurences;

SELECT MONTH(date) as mois, count(id_article) as occurences
FROM Articles
GROUP BY année
ORDER By occurences;

SELECT DAY(date) as jour, count(id_article) as occurences
FROM Articles
GROUP BY année
ORDER By occurences;

-- Métier
SELECT revue, count(id_article) as occurences
FROM Articles
GROUP BY revue
ORDER By occurences;

SELECT nom_auteur, count(id_article) as occurences
FROM Auteurs AS aut
INNER JOIN Ecrire AS ecr
ON aut.id_auteur = ecr.id_auteur
GROUP BY nom_auteur
ORDER BY occurences;



-- Requêtes Complexes
-- les 10 mots clés les plus fréquents
SELECT TOP(10) mot_cle, count(id_article) as occurences
FROM Mot_cles AS mot
INNER JOIN Contenir AS cont
ON mot.id_mot_cle = cont.id_mot_cle
GROUP BY id_mot_cle
ORDER BY occurences;

-- les 10 articles les plus cités
SELECT TOP(10) id_article, titre, count(nombre_citation) as citations
FROM Articles
GROUP BY id_article
ORDER BY citations;

-- les 10 articles les plus consultés
SELECT TOP(10) id_article, titre, count(nombre_vue) as citations
FROM Articles
GROUP BY id_article
ORDER BY nombre_vue;

-- les 10 mots clés de rang 1 les plus fréquents
SELECT TOP(10) mot_cle, count(id_article) as occurences
FROM Mot_cles AS mot
INNER JOIN Contenir AS cont
ON mot.id_mot_cle = cont.id_mot_cle
WHERE rang_mot_cle_article = 1
GROUP BY id_mot_cle
ORDER BY occurences;

-- les 10 mots clés de rang 2 les plus fréquents
SELECT TOP(10) mot_cle, count(id_article) as occurences
FROM Mot_cles AS mot
INNER JOIN Contenir AS cont
ON mot.id_mot_cle = cont.id_mot_cle
WHERE rang_mot_cle_article = 2
GROUP BY id_mot_cle
ORDER BY occurences;

-- TODO: prendre en compte les niveaux pour les Requêtes Complexes ?
-- ex. les 10 mots clés les plus fréquents par pays, par année, ...