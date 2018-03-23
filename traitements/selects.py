import pymssql
import csv

# Lancer le docker
# sudo docker start sql1

# Lancer le bash du serveur de la BD
# sudo docker exec -it sql1 "bash"

# Ouvrir le terminal de SQL Server
# /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P '<YourNewStrong!Passw0rd>'

# Requete pour avoir l'adresse :
# SELECT dec.local_net_address FROM sys.dm_exec_connections AS dec WHERE dec.session_id = @@SPID;


try:
    connexion = pymssql.connect(server='172.17.0.2', user='SA', password='<YourStrong!Passw0rd>', database='Base1')
    curseur = connexion.cursor()

	# Nombre d'article
    curseur.execute("""SELECT pays, count(id_article) as occurences
					FROM Articles
					GROUP BY pays
					ORDER By occurences DESC;""")
    with open("csv/Article_Par_Pays.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

    curseur.execute("""SELECT ville, count(id_article) as occurences
					FROM Articles
					WHERE type = 'conference'
					GROUP BY ville
					ORDER By occurences DESC;""")
    with open("csv/nombre_de_conference_dans_un_pays.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)


    curseur.execute("""SELECT pays, etat, count(id_article) as occurences
					FROM Articles
					WHERE type = 'conference'
                    AND etat is not null
					GROUP BY pays, etat
					ORDER By pays, occurences DESC;""")
    with open("csv/nombre_de_conference_dans_dans_un_etat.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

    curseur.execute("""SELECT YEAR(date_article), count(id_article) as occurences
					FROM Articles
					GROUP BY YEAR(date_article)
					ORDER By occurences DESC;""")
    with open("csv/nombre_d'article_par_an.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

    curseur.execute("""SELECT MONTH(date_article), count(id_article) as occurences
					FROM Articles
					GROUP BY MONTH(date_article)
					ORDER By occurences DESC;""")
    with open("csv/nombre_d'article_par_mois.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

    curseur.execute("""SELECT nom_revue, count(id_article) as occurences
					FROM Articles
					GROUP BY nom_revue
                    HAVING count(id_article) > 5
					ORDER By occurences DESC;""")
    with open("csv/nom_de_la_revue_par_article.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

    curseur.execute("""SELECT nom_auteur, count(id_article) as occurences
					FROM Auteurs AS aut
					INNER JOIN Ecrire AS ecr
					ON aut.id_auteur = ecr.id_auteur
					GROUP BY nom_auteur
                    HAVING count(id_article) > 5
					ORDER BY occurences DESC;""")
    with open("csv/nom_d'article_par_auteur.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

	# Requêtes Complexes
    curseur.execute("""SELECT TOP(20) mot_cle, count(id_article) as occurences
					FROM Mot_cles, Contenir
					Where Mot_cles.id_mot_cle = Contenir.id_mot_cle
					GROUP BY mot_cle
					ORDER BY occurences DESC;""")
    with open("csv/Top_des_mots_cles_par_article.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

    curseur.execute("""SELECT TOP(20) id_article, titre, nombre_citation
					FROM Articles
					ORDER BY nombre_citation DESC; """)
    with open("csv/Top_des_article_les_plus_cites.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

    curseur.execute("""SELECT TOP(30) id_article, titre, nombre_vue
					FROM Articles
					ORDER BY nombre_vue DESC;""")
    with open("csv/Top_des_article_les_plus_vues.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

    curseur.execute("""SELECT TOP(20) mot_cle, count(id_article) as occurences
					FROM Mot_cles AS mot
					INNER JOIN Contenir AS cont
					ON mot.id_mot_cle = cont.id_mot_cle
					WHERE rang_mot_cle_article = 1
					GROUP BY mot_cle
					ORDER BY occurences DESC;""")
    with open("csv/Top_des_mots_cles_de_rang_1.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

    curseur.execute("""SELECT TOP(20) mot_cle, count(id_article) as occurences
					FROM Mot_cles AS mot
					INNER JOIN Contenir AS cont
					ON mot.id_mot_cle = cont.id_mot_cle
					WHERE rang_mot_cle_article = 2
					GROUP BY mot_cle
					ORDER BY occurences DESC;""")
    with open("csv/Top_des_mots_cles_de_rang_2.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)


    curseur.execute("""SELECT pays_auteur, count(aut.id_auteur) as occurences
						FROM Auteurs AS aut, Articles as art, Ecrire as ecr
                        Where aut.id_auteur = ecr.id_auteur
						And ecr.id_article = art.id_article
						GROUP BY pays_auteur
						ORDER By occurences DESC;""")
    with open("csv/Les_pays_avec_le_plus_dauteurs.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

    curseur.execute("""SELECT ville, count(art.id_article) as occurences
						FROM Auteurs AS aut, Ecrire AS ecr, Articles AS art
                        Where aut.id_auteur = ecr.id_auteur
						And ecr.id_article = art.id_article
						And type = 'conference'
						GROUP BY ville
						ORDER By occurences DESC; """)
    with open("csv/Les_villes_les_mieux_frequentes.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)


    curseur.execute("""SELECT nom_revue, count(aut.id_auteur) as occurences
					FROM Auteurs AS aut, Ecrire AS ecr, Articles AS art
                    Where aut.id_auteur = ecr.id_auteur
					And ecr.id_article = art.id_article
					GROUP BY nom_revue
                    HAVING count(aut.id_auteur) > 10
					ORDER By occurences DESC; """)
    with open("csv/Les_revues_les_plus_fréquentés.csv", "w") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)


    connexion.close()
except pymssql.Error as e:
    print("Erreur SQL {0} : {1}".format(e.args[0], e.args[1].decode("utf-8")))
