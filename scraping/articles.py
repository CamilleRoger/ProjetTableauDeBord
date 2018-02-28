""" Commande
scrapy runspider articles.py -o articles.csv
"""

import re
import scrapy
from scrapy_splash import SplashRequest


class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    # paramètrage pour faire le lien avec le serveur Splash local
    custom_settings = {
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
        # 'DOWNLOAD_DELAY': 0.25,
        # 'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7',
    }

    def start_requests(self):
        yield SplashRequest(
            #url='http://ieeexplore.ieee.org/document/7495234/',
            url='http://ieeexplore.ieee.org/search/searchresult.jsp?queryText=(.QT.smart%20grid.QT.)&matchBoolean=true&pageNumber=1&rowsPerPage=10&newsearch=true&searchField=Search_All',
            callback=self.parse_articles,
            meta={'splash': {'args': {'wait': 5}}})

    def parse_articles(self, response):
        """Génère la liste des articles à analyser"""

        # TODO Le fait de rechercher à chaque itération (page) le nombre total de page peut sans doute être optimisé
        nombre_page = response.css("div.Dashboard-header.ng-scope > span.ng-scope > span.strong.ng-binding::text").extract()
        nombre_page = int(nombre_page[1].replace(',', ''))

        page_actuelle_re = re.search('(?<=pageNumber=)\d+', response.url)
        page_actuelle = int(page_actuelle_re.group(0))

        for article in response.css("h2.result-item-title > a.ng-binding.ng-scope::attr('href')").extract():
            re1 = re.search('(?<=/document/)\d+', article)
            if re1:
                numero = int(re1.group(0))
                yield {"id": numero,}

                # exemple de cas à part : 6381808 (eBook)

        # Alternative pour le débuggage
        # for article in response.css("h2.result-item-title > a.ng-binding.ng-scope::attr('href')").extract():
        #     re1 = re.search('(?<=/document/)\d+', article)
        #     if re1:
        #         numero = int(re1.group(0))
        #         yield {"id": numero, "type": 1, "page": page_actuelle, "html": article}
        #     else:
        #         re2 = re.search('(?<=/xpl/articleDetails\.jsp\?arnumber=)\d+', article)
        #         if re2:
        #             numero = int(re2.group(0))
        #             yield {"id": numero, "type": 2, "page": page_actuelle, "html": article}
        #         else:
        #             yield {"id": None, "type": 3, "page": page_actuelle, "html": article}

        if page_actuelle < nombre_page:
            print("Page numéro : ", page_actuelle)
            page_suivante = "http://ieeexplore.ieee.org/search/searchresult.jsp?queryText=(.QT.smart%20grid.QT.)&matchBoolean=true&pageNumber=" + str(page_actuelle + 1) + "&rowsPerPage=10&newsearch=true&searchField=Search_All"
            yield SplashRequest(url=page_suivante,
                                callback=self.parse_articles,
                                meta={'splash': {'args': {'wait': 5}}})
