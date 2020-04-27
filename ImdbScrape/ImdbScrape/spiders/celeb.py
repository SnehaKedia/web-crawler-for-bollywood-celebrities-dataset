# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import logging

class CelebSpider(scrapy.Spider):
    name = 'celeb'
    allowed_domains = ['imdb.com']
    start_urls = ['http://www.imdb.com/list/ls068010962/']
    count = 0

    def parse(self, response):
        
        urls = response.xpath('//div[@class="lister-item mode-detail"]//h3/a/@href').extract()
        for url in urls:
            abs_url = response.urljoin(url)+'/'
            yield Request(abs_url, callback=self.parse_celeb)
        
        #--------NEXT PAGE----------------
        next_page_url = response.xpath('//a[@class="flat-button lister-page-next next-page"]/@href').extract_first()   
        if next_page_url==None:
            logging.info('PARSED ACTORS : {}'.format(self.count))
            pass
        else:
            abs_next_page_url = response.urljoin(next_page_url)
            yield Request(abs_next_page_url)
            
            
    def parse_celeb(self, response):
        
        self.count = self.count +1
        
        name = response.xpath('//table[@id="name-overview-widget-layout"]//h1/span[@class="itemprop"]/text()').extract_first() 

        img = response.xpath('//table[@id="name-overview-widget-layout"]//td[@id="img_primary"]//img[@id="name-poster"]/@src').extract_first() 
        
        fullbiolink = response.url + 'bio'
        
        birthdate = response.xpath('//table[@id="name-overview-widget-layout"]//td[@id="overview-top"]//div[@id="name-born-info"]/time/a[1]/text()').extract_first()
        birthyear = response.xpath('//table[@id="name-overview-widget-layout"]//td[@id="overview-top"]//div[@id="name-born-info"]/time/a[2]/text()').extract_first() 
        birthplace = response.xpath('//table[@id="name-overview-widget-layout"]//td[@id="overview-top"]//div[@id="name-born-info"]/a/text()').extract_first()
        
        
        about = response.xpath('//table[@id="name-overview-widget-layout"]//td[@id="overview-top"]//div[@class="inline"]/text()').extract_first().strip()
        if about[len(about)-3:len(about)] == '...':
            about = about + ' Read more from IMDB Bio Link'
        
        height_list = response.xpath('//div[@id="details-height"]/text()').extract()
        if len(height_list)==0:
            height=''
        else:
            height = height_list[1].strip()
        ''' To express seperately in " and in m
        h=height.split('(')
        h = [x.strip(')') for x in h]
        '''
        
        aka_list = response.xpath('//div[@id="details-akas"]/text()').extract()
        aka_list = [x.strip() for x in aka_list if not x.strip()=='']
        
        nickname = ''
        nn_list = response.xpath('//div[@id="dyk-nickname"]/text()').extract()
        nn_list = [x.strip() for x in nn_list if not x.strip()=='']
        if len(nn_list) != 0:
            nickname = nn_list[0]
        
        trademark = ''
        trd_list = response.xpath('//div[@id="dyk-trademark"]/text()').extract()
        trd_list = [x.strip() for x in trd_list if not x.strip()=='']
        if len(trd_list) != 0:
            trademark = trd_list[0]
            
        star_sign = response.xpath('//div[@id="dyk-star-sign"]/a/text()').extract_first()
        
        yield{
            'Name' : name,
            'Image URL': img,
            'IMDB Bio Link' : fullbiolink,
            'Birth Date' : birthdate,
            'Birth Year' : birthyear,
            'Birth Place' : birthplace,
            'About' : about,
            'Height' : height,
            'Alternative Names' : aka_list,
            'Nickname' : nickname,
            'Trademark' : trademark,
            'Star Sign' : star_sign
            }
        
