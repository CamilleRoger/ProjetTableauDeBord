    curseur.execute("""SELECT aut1.nom_auteur, aut2.nom_auteur, COUNT(id_article) AS occurences
					FROM Auteurs AS aut1, Auteurs AS aut2
					INNER JOIN Ecrire AS ecr1
					ON aut1.id_auteur = ecr1.id_auteur
					INNER JOIN Ecrire AS ecr2
					ON aut2.id_auteur = ecr2.id_auteur
					WHERE ecr1.id_article = ecr2.id_article
					GROUP BY aut1.nom_auteur, aut2.nom_auteur
					ORDER By occurences;""")
    for ligne in curseur:
        print(ligne)