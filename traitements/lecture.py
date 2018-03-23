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

    curseur.execute("SELECT * FROM Mot_cles")
    with open("mots_cles.csv", "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

    curseur.execute("SELECT * FROM Articles")
    with open("articles.csv", "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

    curseur.execute("SELECT * FROM Auteurs")
    with open("auteurs.csv", "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

    curseur.execute("SELECT * FROM ecrire")
    with open("ecrire.csv", "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

    curseur.execute("SELECT * FROM contenir")
    with open("contenir.csv", "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for ligne in curseur:
            writer.writerow(ligne)

    connexion.close()
except pymssql.Error as e:
    print("Erreur SQL {0} : {1}".format(e.args[0], e.args[1].decode("utf-8")))
