import plotly.offline as py
import pandas as pd

df = pd.read_csv('/home/camille/Documents/ProjetTableauDeBord/csv/Les_pays_avec_le_plus_dauteurs.csv', names=['Pays', 'nb'])
df_code = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')[['CODE', 'COUNTRY']]
df = df.merge(df_code, left_on='Pays', right_on='COUNTRY')

data = [ dict(
        type='choropleth',
        autocolorscale = False,
        locations = df['CODE'],
        z = df['nb'],
        text = df['COUNTRY'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 0
            ) ),
        colorbar = dict(
            title = "Nombre d'auteur")
        ) ]


layout = dict(
    title = "Nombre d'auteurs par auteurs par pays",
        geo = dict(
            scope='world',
            projection= dict( type='equirectangular'),
            showland = True,
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)',
            showcountries = True
        )
    )

fig = dict(data=data, layout=layout )
py.plot(fig, filename='d3-cloropleth-map' )
