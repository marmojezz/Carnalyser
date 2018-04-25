# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from lxml import html
from carnalyser.items import Car

class WebMotorsSpider(CrawlSpider):
    name = "wmspider"
    allowed_domains = ['www.webmotors.com.br']

    start_urls = [
        'https://www.webmotors.com.br/carros/sp-osasco/honda/city',
    ]

    rules = ( Rule(LinkExtractor(allow=('course-finder', ),restrict_xpaths=('//a[@class="paginationResult.next.radius-3.brd.brd2.brd-gray-dark.mrg-gutter-l"]',)), callback='parse_items',follow=True), )


    def parse(self, response):
        
        doc = Car()
        
        for car in response.xpath('//a[contains(@itemtype, "http://schema.org/Offer")]'):

            ## Extracting anf formating the link

            # Extracting and formating the brand and model and removing blank spaces (source format: u' HONDA CITY ')
            temp = car.css('div.info span.make-model-financiamento::text').extract_first().strip().split(" ")
            brand = temp[0]
            model = temp[1]

            # Extracting and formatting the manufactory year and model year (Sorce format: u' yyyy/yyyy')
            temp = car.css('div.info div.features div.info-veiculo span.content-info-veiculo div.info-veiculo-detalhe::text')[0].extract().strip().split("/")
            year_manufactory = temp[0]
            year_model = temp[1]

            # Extracting and formatting the price (Source format [u' ',u'xx.xxx'])
            price = (''.join(car.css('div.info div.price-novo.space-preco::text').extract())).strip()

            ## Extracting and formatting the version
            # Variable Initialization
            cylinder = 0
            engine = 0
            doors = 0


            # TODO: This certanly can be better. Search for Numpy to deal with that.
            description = car.css('div.info span.version::text').extract_first().strip()
            infos = description.split(" ")
            for desc in infos:
                if desc == '1.0' or desc == '1.4' or desc == '1.5' or desc == '1.6' or desc == '1.8' or desc == '2.0':
                    cylinder = desc
                    pass
                if desc == '8V' or desc == '16V':
                    engine = desc
                    pass
                if desc == '2P' or desc == '4P':
                    doors = desc
                    pass
                if desc == 'FLEX' or desc == 'GASOLINA':
                    fuel_type = desc
                    pass
                pass 

            ## Extracting and formatting kilomiters
            km = car.css('div.info div.features div.info-veiculo span.content-info-veiculo div.info-veiculo-detalhe::text')[1].extract().replace(' ','').replace('km','')
            
            gear_shift = car.css('div.info div.features div.info-veiculo span.content-info-veiculo div.info-veiculo-detalhe::text')[2].extract().strip()
            
            ## Among the values
            yield {
                
                'brand': brand,
                'model': model,
                'price': price,
                'year_manufactory': year_manufactory,
                'year_model': year_model,
                'cylinder': cylinder,
                'engine': engine,
                'doors': doors,
                'fuel': fuel_type,
                'km': km,
                'cambio': gear_shift,
                'desc': description,
                # See https://stackoverflow.com/questions/43922562/scrapy-how-to-use-items-in-spider-and-how-to-send-items-to-pipelines
           }
