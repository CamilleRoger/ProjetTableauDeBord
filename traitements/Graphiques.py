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

# Histogramme
# Requête nombre d'article par pays
Article_Par_Pays = pd.read_csv(
    workpath +
    'Article_Par_Pays.csv',
    sep=',',
    names=[
        "pays",
        "nombre_article"])
df = pd.DataFrame(Article_Par_Pays)
# print(df['nombre_article'])
# print(df['pays'])

Graph = [go.Bar(x=df["pays"], y=df['nombre_article'])]
layout = go.Layout(
    title="Nombre d'articles par pays",)
fig = go.Figure(data=Graph, layout=layout)
py.plot(fig, filename="nombre_article_par_pays_histogramme.html")

# Requête nombre d'article par an
nombre_article_par_an = pd.read_csv(
    workpath +
    "nombre_d'article_par_an.csv",
    sep=',',
    names=[
        "annee",
        "nombre_article"])
df = pd.DataFrame(nombre_article_par_an)

Graph = [go.Bar(x=df["annee"], y=df['nombre_article'])]
layout = go.Layout(
    title="Evolution du nombre d'articles publié par année",)
fig = go.Figure(data=Graph, layout=layout)
py.plot(fig, filename="Evolution du nombres d'article publié par année.html")

# Courbes
# nombre d'article par mois annee
nombre_article_par_an_mois = pd.read_csv(
    workpath +
    "nombre_d'article_par_mois_annee.csv",
    sep=',',
    names=[
        "mois-annee",
        "nombre_article"])
df = pd.DataFrame(nombre_article_par_an_mois)

trace2 = go.Scatter(
    x=df["mois-annee"],
    y=df["nombre_article"],
    mode='lines+markers',
    name='lines+markers'
)
data = [trace2]
layout = go.Layout(
    title="Evolution du nombre d'articles publié par année et par mois",)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='Evolution_du_nombre_articles_publié_par_annee_et_mois.html')

# histogramme nombre d'article par mois
nombre_article_par_mois = pd.read_csv(
    workpath + "nombre_d'article_par_mois.csv", sep=',',
    names=["mois", "nombre_article"])
df = pd.DataFrame(nombre_article_par_mois)

Graph = [go.Bar(x=df["mois"], y=df['nombre_article'])]
layout = go.Layout(
    title="Evolution du nombre d'articles publié par mois",)
fig = go.Figure(data=Graph, layout=layout)
py.plot(fig, filename="Evolution du nombre d'articles publié par année.html")

# nombre d'article par ville
Les_villes_les_mieux_frequentes = pd.read_csv(
    workpath +
    "Les_villes_les_mieux_frequentes.csv",
    sep=',',
    names=[
        "ville",
        "nombre_article"])
df = pd.DataFrame(Les_villes_les_mieux_frequentes)

df = df.values
labels = df[:, 0]
values = df[:, 1]
trace = go.Pie(labels=labels, values=values)
py.plot([trace], filename="Les_villes_les_plus_fréquentés.html")

# Requête les pays ayant le plus de conference sur Smart Grid
nombre_de_conference_dans_dans_un_pays = pd.read_csv(
    workpath +
    "nombre_de_conference_dans_un_pays.csv",
    sep=',',
    names=[
        "pays",
        "nombre_conference"])
df = pd.DataFrame(nombre_de_conference_dans_dans_un_pays)

Graph = [go.Bar(x=df["pays"], y=df['nombre_conference'])]
layout = go.Layout(
    title="Les pays ayant le plus de conférence sur Smart Grid",)
fig = go.Figure(data=Graph, layout=layout)
py.plot(fig, filename="Les pays ayant le plus de conférence sur Smart Grid.html")
