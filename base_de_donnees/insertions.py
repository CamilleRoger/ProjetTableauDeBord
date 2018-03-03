import pymssql

try:
    connexion = pymssql.connect(server='172.17.0.4', user='SA', password='<YourNewStrong!Passw0rd>', database='TestDB')
    curseur = connexion.cursor()
    curseur.execute("SELECT * from Inventory")
    ligne = curseur.fetchone()
    while ligne:
        print(ligne[0], ligne[1], ligne[2])
        ligne = curseur.fetchone()
except pymssql.Error as erreur:
   print("Erreur SQL :", erreur)
