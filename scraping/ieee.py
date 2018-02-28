""" Commande
scrapy runspider ieee.py
"""

import re
import csv
import scrapy
from scrapy_splash import SplashRequest


class IeeeSpider(scrapy.Spider):
    name = 'ieee'
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
        with open('articles.csv', newline='') as fichier_csv:
            lecteur = csv.reader(fichier_csv)
            next(lecteur)
            for numero_article in lecteur:
                print(numero_article[0])
                yield SplashRequest(
                    url='http://ieeexplore.ieee.org/document/' + numero_article[0] + '/',
                    callback=self.parse,
                    meta={'splash': {'args': {'wait': 2}}})

    def parse(self, response):
        rurl = response.url
        print('url: ', rurl)

        titre = response.css('h1.document-title > span.ng-binding::text').extract_first()
        print('titre: ', titre)

        auteurs = response.css('div.ng-scope.doc-ft-extra-padded > section.ng-isolate-scope > div.ng-scope > section.document-all-authors.ng-scope > div.ng-scope > div > div.author-container.stats-author-container.ng-scope > div.pure-u-18-24 > div > a > span.ng-binding::text').extract()
        print('auteurs: ', auteurs)

        date = response.css('div.u-pb-1.doc-abstract-confdate.ng-binding.ng-scope::text').extract()[2]
        print('date: ', date)

        nb_vues = response.css('div.document-banner-metric-count.ng-binding::text').extract()[1]
        print('nb-vues: ', nb_vues)

        resume = response.css('div.abstract-text.ng-binding::text').extract_first()
        print('resume: ', resume)

        # yield SplashRequest(url='http://ieeexplore.ieee.org/document/7495234/keywords', callback=self.parse_mots_cles)
        # yield SplashRequest(url='http://ieeexplore.ieee.org/document/7495234/authors', callback=self.parse_auteurs)

        # mots_cles = response.css('li.doc-keywords-list-item.ng-scope > ul.u-mt-1.u-p-0.List--no-style.List--inline > li.ng-binding.ng-scope > a.stats-keywords-list-item.ng-binding::text').extract()

        # auteurs = response.css('div.pure-u-18-24 > div > a > span.ng-binding::text').extract()
