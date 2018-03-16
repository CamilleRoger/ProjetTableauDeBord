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

    curseur.execute("""
        IF OBJECT_ID('ecrire') IS NOT NULL
            DROP TABLE ecrire
        IF OBJECT_ID('appartenir') IS NOT NULL
            DROP TABLE appartenir
        IF OBJECT_ID('contenir') IS NOT NULL
            DROP TABLE contenir
        IF OBJECT_ID('publier') IS NOT NULL
            DROP TABLE publier
        IF OBJECT_ID('Institut') IS NOT NULL
            DROP TABLE Institut
        IF OBJECT_ID('Articles') IS NOT NULL
            DROP TABLE Articles
        IF OBJECT_ID('Revue') IS NOT NULL
            DROP TABLE Revue
        IF OBJECT_ID('Auteurs') IS NOT NULL
            DROP TABLE Auteurs
        IF OBJECT_ID('Mot_cles') IS NOT NULL
            DROP TABLE Mot_cles

        CREATE TABLE Articles(
    	id_article                INT  NOT NULL ,
    	resume                    VARCHAR (25) NOT NULL ,
    	annee_publi               DATETIME NOT NULL ,
    	mois_publi                INT  NOT NULL ,
    	jour_publi                INT  NOT NULL ,
    	duree_conference_associee INT  NOT NULL ,
    	nombre_consultation       INT  NOT NULL ,
    	nombre_citation           INT  NOT NULL ,
    	CONSTRAINT prk_constraint_Articles PRIMARY KEY NONCLUSTERED (id_article)
        );

        CREATE TABLE Auteurs(
    	id_auteur     INT IDENTITY (1,1) NOT NULL ,
    	nom_auteur    VARCHAR (25) NOT NULL ,
    	prenom_auteur VARCHAR (25) NOT NULL ,
    	CONSTRAINT prk_constraint_Auteurs PRIMARY KEY NONCLUSTERED (id_auteur)
        );

        CREATE TABLE Mot_cles(
    	id_mot_cle INT IDENTITY (1,1) NOT NULL ,
    	mot_cle    VARCHAR (25) NOT NULL ,
    	CONSTRAINT prk_constraint_Mot_cles PRIMARY KEY NONCLUSTERED (id_mot_cle)
        );

        CREATE TABLE Revue(
    	id_revue  INT IDENTITY (1,1) NOT NULL ,
    	nom_revue VARCHAR (25) NOT NULL ,
    	CONSTRAINT prk_constraint_Revue PRIMARY KEY NONCLUSTERED (id_revue)
        );

        CREATE TABLE Institut(
    	id_institut      INT IDENTITY (1,1) NOT NULL ,
    	pays_institut    VARCHAR (25) NOT NULL ,
    	ville_institut   VARCHAR (25) NOT NULL ,
    	etat_us_institut VARCHAR (25)  ,
    	CONSTRAINT prk_constraint_Institut PRIMARY KEY NONCLUSTERED (id_institut)
        );

        CREATE TABLE ecrire(
    	rang_auteur_article INT  NOT NULL ,
    	id_article          INT  NOT NULL ,
    	id_auteur           INT  NOT NULL ,
    	CONSTRAINT prk_constraint_ecrire PRIMARY KEY NONCLUSTERED (id_article,id_auteur)
        );

        CREATE TABLE appartenir(
    	id_auteur   INT  NOT NULL ,
    	id_institut INT  NOT NULL ,
    	CONSTRAINT prk_constraint_appartenir PRIMARY KEY NONCLUSTERED (id_auteur,id_institut)
        );

        CREATE TABLE contenir(
    	rang_mot_cle_article INT  NOT NULL ,
    	id_article           INT  NOT NULL ,
    	id_mot_cle           INT  NOT NULL ,
    	CONSTRAINT prk_constraint_contenir PRIMARY KEY NONCLUSTERED (id_article,id_mot_cle)
        );

        CREATE TABLE publier(
    	id_article INT  NOT NULL ,
    	id_revue   INT  NOT NULL ,
    	CONSTRAINT prk_constraint_publier PRIMARY KEY NONCLUSTERED (id_article,id_revue)
        );

        ALTER TABLE ecrire ADD CONSTRAINT FK_ecrire_id_article FOREIGN KEY (id_article) REFERENCES Articles(id_article);
        ALTER TABLE ecrire ADD CONSTRAINT FK_ecrire_id_auteur FOREIGN KEY (id_auteur) REFERENCES Auteurs(id_auteur);
        ALTER TABLE appartenir ADD CONSTRAINT FK_appartenir_id_auteur FOREIGN KEY (id_auteur) REFERENCES Auteurs(id_auteur);
        ALTER TABLE appartenir ADD CONSTRAINT FK_appartenir_id_institut FOREIGN KEY (id_institut) REFERENCES Institut(id_institut);
        ALTER TABLE contenir ADD CONSTRAINT FK_contenir_id_article FOREIGN KEY (id_article) REFERENCES Articles(id_article);
        ALTER TABLE contenir ADD CONSTRAINT FK_contenir_id_mot_cle FOREIGN KEY (id_mot_cle) REFERENCES Mot_cles(id_mot_cle);
        ALTER TABLE publier ADD CONSTRAINT FK_publier_id_article FOREIGN KEY (id_article) REFERENCES Articles(id_article);
        ALTER TABLE publier ADD CONSTRAINT FK_publier_id_revue FOREIGN KEY (id_revue) REFERENCES Revue(id_revue);
    """)

    connexion.commit()
    connexion.close()
except pymssql.Error as e:
    print("Erreur SQL {0} : {1}".format(e.args[0], e.args[1].decode("utf-8")))
    
