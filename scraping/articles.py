import re
import scrapy
from math import ceil
from scrapy_splash import SplashRequest


class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    fichier_csv = 'articles.csv'
    # purger le fichier de sortie JSON
    open(fichier_csv, 'w').close()
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
        'LOG_LEVEL': 'INFO',
        'FEED_FORMAT': 'csv',
        'FEED_URI': fichier_csv}

    def start_requests(self):
        yield SplashRequest(
            url='http://ieeexplore.ieee.org/search/searchresult.jsp?queryText=(.QT.smart%20grid.QT.)&matchBoolean=true&rowsPerPage=10&newsearch=true&searchField=Search_All',
            callback=self.parse_nombre_pages,
            meta={'splash': {'args': {'wait': 5}},
                  'numero-page': 1})

    def parse_nombre_pages(self, response):
        nombre_pages = response.css(
            "div.Dashboard-header.ng-scope > span.ng-scope > span.strong.ng-binding::text").extract()
        nombre_pages = ceil(int(nombre_pages[1].replace(',', '')) / 10)
        yield SplashRequest(
            url='http://ieeexplore.ieee.org/search/searchresult.jsp?queryText=(.QT.smart%20grid.QT.)&matchBoolean=true&pageNumber=1&rowsPerPage=10&newsearch=true&searchField=Search_All',
            callback=self.parse_articles,
            meta={'splash': {'args': {'wait': 5}},
                  'nombre-pages': nombre_pages,
                  'numero-page': 1})

    def parse_articles(self, response):
        nombre_pages = response.meta['nombre-pages']
        numero_page_en_cours = response.meta['numero-page']
        for article in response.css(
                "h2.result-item-title > a.ng-binding.ng-scope::attr('href')").extract():
            recherche = re.search('(?<=/document/)\d+', article)
            if recherche:
                yield {"id": int(recherche.group(0))}

        print("Page", numero_page_en_cours, "/", nombre_pages, "terminée.")

        if numero_page_en_cours < nombre_pages:
            numero_page_suivante = numero_page_en_cours + 1
            yield SplashRequest(url=re.sub("pageNumber=\d+", "pageNumber=" + str(numero_page_suivante), response.url),
                                callback=self.parse_articles,
                                meta={'splash': {'args': {'wait': 5}},
                                      'nombre-pages': nombre_pages,
                                      'numero-page': numero_page_suivante})
