import pymssql
import json

# Lancer le docker
# sudo docker start sql1

# Lancer le bash du serveur de la BD
# sudo docker exec -it sql1 "bash"

# Ouvrir le terminal de SQL Server
# /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P '<YourNewStrong!Passw0rd>'

# Requete pour avoir l'adresse :
# SELECT dec.local_net_address FROM sys.dm_exec_connections AS dec WHERE dec.session_id = @@SPID;


try:
    connexion = pymssql.connect(server='172.17.0.2', user='SA', password='<YourNewStrong!Passw0rd>', database='Base1')
    curseur = connexion.cursor()

	# Nombre d'article
    curseur.execute("""SELECT pays, count(id_article) as occurences
					FROM Articles
					GROUP BY pays
					ORDER By occurences;""")
    for ligne in curseur:
        print(ligne)

    curseur.execute("""SELECT ville, count(id_article) as occurences
					FROM Articles
					WHERE type = 'conference'
					GROUP BY ville
					ORDER By occurences;""")
    for ligne in curseur:
        print(ligne)

    curseur.execute("""SELECT etat, count(id_article) as occurences
					FROM Articles
					WHERE type = 'conference'
					GROUP BY etat
					ORDER By occurences;""")
    for ligne in curseur:
        print(ligne)

    curseur.execute("""SELECT YEAR(date_article), count(id_article) as occurences
					FROM Articles
					GROUP BY YEAR(date_article)
					ORDER By occurences;""")
    for ligne in curseur:
        print(ligne)

    curseur.execute("""SELECT MONTH(date_article), count(id_article) as occurences
					FROM Articles
					GROUP BY MONTH(date_article)
					ORDER By occurences;""")
    for ligne in curseur:
        print(ligne)

    curseur.execute("""SELECT revue, count(id_article) as occurences
					FROM Articles
					GROUP BY revue
					ORDER By occurences;""")
    for ligne in curseur:
        print(ligne)

    curseur.execute("""SELECT nom_auteur, count(id_article) as occurences
					FROM Auteurs AS aut
					INNER JOIN Ecrire AS ecr
					ON aut.id_auteur = ecr.id_auteur
					GROUP BY nom_auteur
					ORDER BY occurences;""")
    for ligne in curseur:
        print(ligne)



	# Requêtes Complexes
    curseur.execute("""SELECT TOP(10) mot_cle, count(id_article) as occurences
					FROM Mot_cles AS mot
					INNER JOIN Contenir AS cont
					ON mot.id_mot_cle = cont.id_mot_cle
					GROUP BY id_mot_cle
					ORDER BY occurences;""")
    for ligne in curseur:
        print(ligne)

    curseur.execute("""SELECT TOP(10) id_article, titre, count(nombre_citation) as citations
					FROM Articles
					GROUP BY id_article
					ORDER BY citations;""")
    for ligne in curseur:
        print(ligne)

    curseur.execute("""SELECT TOP(10) id_article, titre, count(nombre_vue) as citations
					FROM Articles
					GROUP BY id_article
					ORDER BY nombre_vue;""")
    for ligne in curseur:
        print(ligne)

    curseur.execute("""SELECT TOP(10) mot_cle, count(id_article) as occurences
					FROM Mot_cles AS mot
					INNER JOIN Contenir AS cont
					ON mot.id_mot_cle = cont.id_mot_cle
					WHERE rang_mot_cle_article = 1
					GROUP BY id_mot_cle
					ORDER BY occurences;""")
    for ligne in curseur:
        print(ligne)

    curseur.execute("""SELECT TOP(10) mot_cle, count(id_article) as occurences
					FROM Mot_cles AS mot
					INNER JOIN Contenir AS cont
					ON mot.id_mot_cle = cont.id_mot_cle
					WHERE rang_mot_cle_article = 2
					GROUP BY id_mot_cle
					ORDER BY occurences;""")
    for ligne in curseur:
        print(ligne)

    connexion.close()
except pymssql.Error as e:
    print("Erreur SQL {0} : {1}".format(e.args[0], e.args[1].decode("utf-8")))
