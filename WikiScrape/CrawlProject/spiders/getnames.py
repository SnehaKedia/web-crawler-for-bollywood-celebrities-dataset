# -*- coding: utf-8 -*-
import scrapy
#import pdb
from scrapy.http import Request
from scrapy import Selector
import logging
import re
#from time import sleep

class GetnamesSpider(scrapy.Spider):
    name = 'getnames'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['http://en.wikipedia.org/wiki/List_of_Indian_film_actors',]
    
    urls_wiki = ['','http://en.wikipedia.org/wiki/List_of_Bollywood_actors',
                 'https://en.wikipedia.org/wiki/List_of_Indian_film_actresses']
    count = 0
    
    global_actor_urls=[]
    
    def parse(self, response):
        
        self.count = self.count + 1
        
        actor_urls = response.xpath('//*[@class="div-col columns column-width"]/ul/li/a/@href').extract()   
        
        for url in actor_urls:
            if url not in self.global_actor_urls:
                absolute_url = response.urljoin(url)
                self.global_actor_urls.append(absolute_url)
                yield Request(absolute_url, callback=self.parse_getnames)
                #sleep(3)
        
        if self.count < len(self.urls_wiki):
            yield Request(self.urls_wiki[self.count],callback=self.parse)
            
            
            
    def parse_getnames(self, response):
        
        name = response.xpath('//*[@id="firstHeading"]/text()').extract_first()
        url = response.url
        imgsrc = response.xpath('//td/a[@class="image"]/img/@src').extract()
        if(len(imgsrc)==0):
            imgurl=""
        else:
            imgurl = imgsrc[0].replace('//','https://')
            
        p_elem = response.xpath('//*[@id="mw-content-text"]//table[contains(@class,"infobox")]/following-sibling::p[1]//text()').extract()
        
        if len(p_elem)==0:
            ix=1
            while True:
                ls = response.xpath('//div[@class="mw-parser-output"]/p[{}]//text()'.format(ix)).extract()  
                ls = [x for x in ls if not x.startswith('[')]    
                s = ""
                s = s.join(ls)
                x=re.search('[a-zA-Z]', s)
                if x==None:
                    ix=ix+1
                else:
                    break
        else:
            ls = [x for x in p_elem if not x.startswith('[')]
            s = ""
            s = s.join(ls)
        
        s=s.strip()
        
        
        yield {
            
            'Name' : name,
            'Wiki URL' : url,
            'Image URL' : imgurl,
            'Description' : s
            
            }