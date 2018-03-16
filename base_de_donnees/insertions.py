import pymssql
import json

# Lancer le docker
# sudo docker start sql1

# Lancer le bash du serveur de la BD
# sudo docker exec -it sql1 "bash"

# Ouvrir le terminal de SQL Server
# /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P '<YourNewSStrong!Passw0rd>'

# Requete pour avoir l'adresse :
# SELECT dec.local_net_address FROM sys.dm_exec_connections AS dec WHERE dec.session_id = @@SPID;


try:
    connexion = pymssql.connect(server='172.17.0.3', user='SA', password='<YourNewStrong!Passw0rd>', database='Base1')
    curseur = connexion.cursor()

    with open('ieee.json') as json_data:
        data = json.load(json_data)
        compteur = 0
        for article in data:
            if compteur <= 2:  # Pour ne pas faire tout le fichier
                compteur += 1

        curseur.execute("SET IDENTITY_INSERT Revue ON")
        curseur.executemany("INSERT INTO Revue(id_revue, nom_revue) VALUES (%d, %s)",
            [(1, 'Revue 1'),
             (2, 'Revue 2'),
             (3, 'Revue 3')])
        curseur.execute("SET IDENTITY_INSERT Revue OFF")

        # curseur.execute("SET IDENTITY_INSERT Articles OFF")
        # curseur.execute("SET IDENTITY_INSERT Revue OFF")
        # curseur.execute("SET IDENTITY_INSERT Auteurs OFF")
        # curseur.execute("SET IDENTITY_INSERT Mot_cles OFF")
        # curseur.execute("SET IDENTITY_INSERT Institut OFF")
        # curseur.execute("SET IDENTITY_INSERT ecrire OFF")
        # curseur.execute("SET IDENTITY_INSERT appartenir OFF")
        # curseur.execute("SET IDENTITY_INSERT contenir OFF")
        # curseur.execute("SET IDENTITY_INSERT publier OFF")
        connexion.commit()

        print("ok")

        # Afficher les résultats
        # curseur.execute("SELECT * FROM revue")
        # ligne = curseur.fetchone()
        # for ligne in curseur:
        #     print(ligne)


        connexion.commit()
    connexion.close()
except pymssql.Error as e:
    print("Erreur SQL {0} : {1}".format(e.args[0], e.args[1].decode("utf-8")))
