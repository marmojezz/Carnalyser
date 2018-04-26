# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from lxml import html
import numpy as np

class TrovitSpider(CrawlSpider):
    name = "trovitspider"
    allowed_domains = ['carros.trovit.com.br']

    start_urls = [
        'https://carros.trovit.com.br/index.php/cod.search_cars/what_d.honda city/isUserSearch.1'
    ]

    rules = ( Rule(LinkExtractor(allow=('course-finder', ),restrict_xpaths=('//a[@class="paginationResult.next.radius-3.brd.brd2.brd-gray-dark.mrg-gutter-l"]',)), callback='parse_items',follow=True), )


    def parse(self, response):
        i = 0
        for car in response.xpath('//div[contains(@itemtype, "http://schema.org/Car https://schema.org/Offer")]'):

            ## Extracting anf formating the link

            # Extracting and formating the brand and model and removing blank spaces (source format: u' HONDA CITY ')
            temp = car.css('div.details h4 a strong::text').extract()
            brand = temp[0]
            model = temp[1]
            
            # Extracting and formatting the manufactory year and model year (Sorce format: u' yyyy/yyyy')
            #temp = car.css('div.info div.features div.info-veiculo span.content-info-veiculo div.info-veiculo-detalhe::text')[0].extract().strip().split("/")
            #year_manufactory = temp[0]
            #year_model = temp[1]

            # Extracting and formatting the price (Source format [u' ',u'xx.xxx'])
            price = car.css('div.features div.price span.amount::text').extract_first()

            ## Extracting and formatting the version
            # Variable Initialization
            cylinder = 0
            engine = 0
            doors = 0
            #print("price " + price)

            # TODO: This certanly can be better. Search for Numpy to deal with that.
            description = car.css('div.details h4 a::text').extract()[1]
            print(description)
            infos = description.split(" ")
            for desc in infos:
                if desc == '1.0' or desc == '1.4' or desc == '1.5' or desc == '1.6' or desc == '1.8' or desc == '2.0':
                    cylinder = desc
                    pass
                if desc == '8v' or desc == '16v':
                    engine = desc
                    pass
                if desc == '2p' or desc == '4p':
                    doors = desc
                    pass
                if desc == 'flex' or desc == 'gasolina':
                    fuel_type = desc
                    pass
                pass 

            ## Extracting and formatting kilomiters
            #km = car.css('div.info div.features div.info-veiculo span.content-info-veiculo div.info-veiculo-detalhe::text')[1].extract().replace(' ','').replace('km','')
            
            #gear_shift = car.css('div.info div.features div.info-veiculo span.content-info-veiculo div.info-veiculo-detalhe::text')[2].extract().strip()
            
            desc = ''.join(car.css('div.details div.description p::text').extract())
            ## Among the values
            yield {
                'brand': brand,
                'model': model,
                'price': price,
                #'year_manufactory': year_manufactory,
                #'year_model': year_model,
                'cylinder': cylinder,
                'engine': engine,
                'doors': doors,
                'fuel': fuel_type,
                #'km': km,
                #'cambio': gear_shift,
                'desc': desc
           }
