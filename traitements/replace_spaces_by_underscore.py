import re

with open('Top_des_mots_cles_par_article.csv', 'r') as csvfile:
    for ligne in csvfile:
        ligne = re.sub(" ", "_", ligne)
	   