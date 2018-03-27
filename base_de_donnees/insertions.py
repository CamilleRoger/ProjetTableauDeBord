import pymssql
import json
import re

# Lancer le docker
# sudo docker start sql1

# Lancer le bash du serveur de la BD
# sudo docker exec -it sql1 "bash"

# Ouvrir le terminal de SQL Server
# /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P '<YourNewStrong!Passw0rd>'

# Requete pour avoir l'adresse :
# SELECT dec.local_net_address FROM sys.dm_exec_connections AS dec WHERE
# dec.session_id = @@SPID;


def echappement(chaine):
    if chaine is None:
        return None
    else:
        return re.sub("'", "''", chaine)


try:
    connexion = pymssql.connect(
        server='172.17.0.2',
        user='SA',
        password='<YourNewStrong!Passw0rd>',
        database='Base1')
    curseur = connexion.cursor()

    with open('ieee.json') as json_data:
        data = json.load(json_data)
        compteur = 0
        for article in data:
            # if compteur <= 100:  # Pour ne pas faire tout le fichier
            compteur += 1

            if "nb-citations" in article:
                nombre_citation = article['nb-citations']
            else:
                nombre_citation = 0

            if "nb-vues" in article:
                nombre_vue = article['nb-vues']
            else:
                nombre_vue = 0

            if "lieu-conference" in article:
                if article['lieu-conference'] is not None:
                    if "ville" in article['lieu-conference']:
                        ville = article['lieu-conference']['ville']
                    else:
                        ville = None
                    if "etat" in article['lieu-conference']:
                        etat = article['lieu-conference']['etat']
                    else:
                        etat = None
                    if "pays" in article['lieu-conference']:
                        pays = article['lieu-conference']['pays']
                    else:
                        pays = None
                else:
                    ville = None
                    etat = None
                    pays = None
            else:
                ville = None
                etat = None
                pays = None
            resume = echappement(article['resume'])
            revue = echappement(article['revue'])
            titre = echappement(article['titre'])
            type_article = article['type']
            id_article = article['id']
            url = article['url']
            date = article['date']
            try:
                curseur.execute(
                    "INSERT INTO Articles(id_article,resume,nom_revue,nombre_vue,nombre_citation,url,date_article,titre,type,ville,etat,pays) Values(%d,%s,%s,%d,%d,%s,%s,%s,%s,%s,%s,%s)",
                    (id_article,
                     resume,
                     revue,
                     nombre_vue,
                     nombre_citation,
                     url,
                     date,
                     titre,
                     type_article,
                     ville,
                     etat,
                     pays))
            except BaseException:
                pass

            if "mots-cles" in article:
                rang = 1
                for mot in article["mots-cles"]:
                    curseur.execute(
                        "SELECT id_mot_cle FROM Mot_cles where mot_cle = '" +
                        echappement(mot) +
                        "'")
                    id_mot = curseur.fetchone()
                    if id_mot is None:
                        curseur.execute(
                            "INSERT INTO Mot_cles(mot_cle) Values(%s)", mot)
                        curseur.execute(
                            "SELECT id_mot_cle FROM Mot_cles where mot_cle = '" +
                            echappement(mot) +
                            "'")
                        id_mot = curseur.fetchone()
                    try:
                        curseur.execute(
                            "INSERT INTO Contenir(rang_mot_cle_article, id_article, id_mot_cle) Values(%d, %d, %d)",
                            (rang,
                             article['id'],
                                id_mot))
                    except pymssql.Error as e:
                        pass
                    rang += 1
            if "auteurs" in article:
                rang = 1
                for auteur in article["auteurs"]:
                    # Auteurs
                    curseur.execute(
                        "SELECT id_auteur FROM Auteurs where nom_auteur = '" +
                        echappement(
                            auteur["nom-auteur"]) +
                        "'")
                    id_auteur = curseur.fetchone()
                    if id_auteur is None:
                        if auteur["pays-auteur"] is not None:
                            curseur.execute(
                                "INSERT INTO Auteurs(nom_auteur, pays_auteur, infos_auteur) Values(%s, %s, %s)",
                                (echappement(
                                    auteur["nom-auteur"]),
                                    auteur["pays-auteur"],
                                    echappement(
                                    auteur["infos-auteur"])))
                        else:
                            curseur.execute(
                                "INSERT INTO Auteurs(nom_auteur) Values(%s)",
                                (echappement(
                                    auteur["nom-auteur"])))

                        curseur.execute(
                            "SELECT id_auteur FROM Auteurs where nom_auteur = '" +
                            echappement(
                                auteur["nom-auteur"]) +
                            "'")
                        id_auteur = curseur.fetchone()

                    # Ecrire
                    try:
                        curseur.execute(
                            "INSERT INTO Ecrire(rang_auteur_article, id_article, id_auteur) Values(%d, %d, %d)",
                            (rang,
                             article['id'],
                                id_auteur))
                    except pymssql.Error as e:
                        pass
                    rang += 1

            print(compteur, "#", id_article, "inséré.")

    connexion.commit()
    connexion.close()
except pymssql.Error as e:
    print(compteur, article)
    print("Erreur SQL {0} : {1}".format(e.args[0], e.args[1].decode("utf-8")))
