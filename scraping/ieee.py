import re
import csv
import scrapy
import pycountry
from scrapy_splash import SplashRequest


class IeeeSpider(scrapy.Spider):
    name = 'ieee'
    fichier_json = 'ieee.json'
    # purger le fichier de sortie JSON
    open(fichier_json, 'w').close()
    custom_settings = {
        # paramètrage pour faire le lien avec le serveur Splash local
        'SPLASH_URL': 'http://localhost:8050',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'LOG_LEVEL': 'INFO',
        'FEED_FORMAT': 'json',
        'FEED_URI': fichier_json,
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def start_requests(self):
        with open('articles.csv', newline='') as fichier_csv:
            lecteur = csv.reader(fichier_csv)
            next(lecteur)
            compteur = 0  # TODO
            for numero_article in lecteur:
                compteur += 1  # TODO
                if compteur >= 20:  # TODO
                    break  # TODO
                item = {}
                item['id'] = int(numero_article[0])
                yield SplashRequest(
                    url='http://ieeexplore.ieee.org/document/' + numero_article[0] + '/',
                    callback=self.parse,
                    meta={'splash': {'args': {'wait': 2}},
                          'item': item})

    def parse(self, response):
        item = response.meta['item']
        item['url'] = response.url
        item['titre'] = response.css('h1.document-title > span.ng-binding::text').extract_first()
        try:
            item['date'] = re.compile(r'[\n\r\t]').sub('', response.css('div.u-pb-1.doc-abstract-confdate.ng-binding.ng-scope::text').extract()[2])
            item['type'] = "conference"

            lieu = re.compile(r'[\n\r\t]').sub('', response.css('div.u-pb-1.doc-abstract-conferenceLoc.ng-binding.ng-scope::text').extract()[2])
            lieu = lieu.split(", ")
            lieu_conf = {}
            if len(lieu) == 2:
                lieu_conf["ville"] = lieu[0]
                lieu_conf["pays"] = lieu[1]
            elif len(lieu) == 3:
                lieu_conf["ville"] = lieu[0]
                lieu_conf["etat"] = lieu[1]
                lieu_conf["pays"] = lieu[2]
            else:
                lieu_conf = None
            item['lieu-conference'] = lieu_conf
        except:
            try:
                item['date'] = re.compile(r'[\n\r\t]').sub('', response.css('div.u-pb-1.doc-abstract-pubdate.ng-binding.ng-scope::text').extract()[2])
                item['type'] = "publication"
            except:
                item['date'] = None
                item['type'] = None

        for compteur in response.css("button.document-banner-metric.ng-scope"):
            donnees = compteur.css("div.ng-binding::text").extract()
            if donnees[1] == "Citations":
                item['nb-citations'] = int(donnees[0])
            elif donnees[1] == "Text Views":
                item['nb-vues'] = int(donnees[0])

        item['resume'] = response.css('div.abstract-text.ng-binding::text').extract_first()
        yield SplashRequest(url=response.url + 'keywords',
                            callback=self.parse_mots_cles,
                            meta={'splash': {'args': {'wait': 2}},
                                  'item': item})

    def parse_mots_cles(self, response):
        item = response.meta['item']
        for liste in response.css('li.doc-keywords-list-item.ng-scope'):
            if liste.css('li.doc-keywords-list-item.ng-scope > strong.ng-binding::text').extract_first() == "IEEE Keywords":
                item['mots-cles'] = liste.css('a.stats-keywords-list-item.ng-binding::text').extract()
                break
        yield SplashRequest(url=re.sub("keywords", "authors", response.url),
                            callback=self.parse_auteurs,
                            meta={'splash': {'args': {'wait': 2}},
                                  'item': item})

    def parse_auteurs(self, response):
        item = response.meta['item']
        noms_auteurs = response.css('div.pure-u-18-24 > div > a > span.ng-binding::text').extract()
        infos_auteurs = response.css('div.pure-u-18-24 > div.ng-binding::text').extract()
        auteurs = []
        for i in range(len(noms_auteurs)):
            auteur = {}
            auteur['nom-auteur'] = noms_auteurs[i]
            nom = [x.name for x in pycountry.countries]
            dnom = {}
            for n in nom:
                dnom[n] = n

            dnom['USA'] = 'United States'
            dnom['U.K.'] = 'United Kingdom'
            dnom['U.K'] = 'United Kingdom'
            dnom['UK'] = 'United Kingdom'
            dnom['México'] = 'Mexico'

            dnom = {k.lower(): i for k, i in dnom.items()}

            try:
                # print(infos_auteurs)
                res = re.findall("(?=(" + '|'.join(map(re.escape, dnom.keys())) + "))", infos_auteurs[i].lower()) # rechercher les pays parmi le dictionnaire dnom
                if len(res) == 0:
                    res = ['usa']
                auteur['pays-auteur'] = dnom[res[0].lower()]
                auteur['infos-auteur'] = infos_auteurs[i]  # TODO
            except:
                auteur['pays-auteur'] = None

            auteurs.append(auteur)
        item['auteurs'] = auteurs

        print("Document n°", item['id'], "récolté.")

        yield item
