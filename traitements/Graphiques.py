import pymssql
import csv
import plotly
import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

workpath = '/home/mickael/Documents/Projet/csv/'

# Requête nombre d'article par pays

Article_Par_Pays = pd.read_csv(workpath+'Article_Par_Pays.csv', sep=',', names = ["pays", "nombre_article"])
df = pd.DataFrame(Article_Par_Pays)
print(df['nombre_article'])
print(df['pays'])

# Histogramme
Graph = [go.Bar(x=df["pays"], y=df['nombre_article'])]
layout = go.Layout(
    title="nombre d'article par pays",)
fig = go.Figure(data=Graph, layout=layout)
# py.plot(fig, filename="nombre d'article par pays.html")

# camembert
df = pd.DataFrame(Article_Par_Pays)
df = df.values
plt.title("nombre d'articles par pays")
plt.pie(df[:,1], labels = df[:,0])
# pylab.savefig('/home/mickael/Documents/Projet/csv/Graphique/chaussette.png')


# Requête nombre d'article par an
nombre_article_par_an = pd.read_csv(workpath+"nombre_d'article_par_an.csv", sep=',', names = ["annee", "nombre_article"])
df = pd.DataFrame(nombre_article_par_an)

#Courbes / ça marche pas bien c'est pas une série temporelle
trace2 = go.Scatter(
    x = df["nombre_article"],
    #y = df["annee"],
    mode = 'lines',
    name = 'lines'
)
data = [trace2]
# py.plot(data, filename='scatter-mode.html')

# Requête
# nombre_de_conference_dans_dans_un_etat + nombre_de_conference_dans_dans_un_pays
nombre_de_conference_dans_dans_un_etat = pd.read_csv(workpath+"nombre_de_conference_dans_un_etat.csv", sep=',', names = ["etat", "nombre_conference"])
df1 = pd.DataFrame(nombre_de_conference_dans_dans_un_etat)
nombre_de_conference_dans_dans_un_pays = pd.read_csv(workpath+"nombre_de_conference_dans_dans_un_pays.csv", sep=',', names = ["pays","etat", "nombre_conference"])
df2 = pd.DataFrame(nombre_de_conference_dans_dans_un_pays)

trace1 = go.Histogram(
    x=df1['etat'],
    #y=df1["nombre_conference"],
)
trace2 = go.Histogram(
    x=df2['pays'],
    #y=df2["nombre_conference"],
)

data = [trace1, trace2]
layout = go.Layout(barmode='stack')
fig = go.Figure(data=data, layout=layout)
# py.plot(fig, filename='overlaid histogram')



Top_des_article_les_plus_vues = pd.read_csv(workpath+"Top_des_article_les_plus_vues.csv", sep=',', names = ["etat", "nombre_conference"])
df1 = pd.DataFrame(Top_des_article_les_plus_vues)
Top_des_article_les_plus_cites = pd.read_csv(workpath+"Top_des_article_les_plus_cites.csv", sep=',', names = ["pays","etat", "nombre_conference"])
df2 = pd.DataFrame(Top_des_article_les_plus_cites)




#yolo
