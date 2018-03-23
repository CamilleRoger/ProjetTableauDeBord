    curseur.execute("""SELECT pays, count(id_auteur) as occurences
						FROM Auteurs AS aut
						INNER JOIN Ecrire AS ecr
						ON aut.id_auteur = ecr.id_auteur
						INNER JOIN Articles AS art
						ON ecr.id_article = art.id_article
						GROUP BY pays
						ORDER By occurences;""")
    for ligne in curseur:
        print(ligne)

    curseur.execute("""SELECT ville, count(id_article) as occurences
						FROM Auteurs AS aut
						INNER JOIN Ecrire AS ecr
						ON aut.id_auteur = ecr.id_auteur
						INNER JOIN Articles AS art
						ON ecr.id_article = art.id_article
						WHERE type = 'conference'
						GROUP BY ville
						ORDER By occurences;
						""")
    for ligne in curseur:
        print(ligne)

       
    curseur.execute("""SELECT nom_revue, count(id_auteur) as occurences
					FROM Auteurs
					GROUP BY nom_revue
					ORDER By occurences;
					""")
    for ligne in curseur:
        print(ligne)
       