'''
Created on Sep 18, 2013

@author: solvire
'''
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from yum_scrapez.items import DisplayItem


class YumellowSpider(BaseSpider):
    name = 'yumellow'
    parsed_pages = []
    allowed_domains = ['www.yellowpages.com']
    start_urls = [
        'http://www.yellowpages.com/santa-barbara-ca/restaurants',
        'http://www.yellowpages.com/carpinteria-ca/restaurants',
        'http://www.yellowpages.com/ojai-ca/restaurants',
        'http://www.yellowpages.com/santa-paula-ca/restaurants',
        'http://www.yellowpages.com/ventura-ca/restaurants',
        'http://www.yellowpages.com/oxnard-ca/restaurants'
        'http://www.yellowpages.com/port-hueneme-ca/restaurants',
        'http://www.yellowpages.com/camarillo-ca/restaurants',
        'http://www.yellowpages.com/somis-ca/restaurants',
        'http://www.yellowpages.com/newbury-park-ca/restaurants',
        'http://www.yellowpages.com/thousand-oaks-ca/restaurants',
        'http://www.yellowpages.com/moorpark-ca/restaurants',
        'http://www.yellowpages.com/simi-valley-ca/restaurants',
        'http://www.yellowpages.com/malibu-ca/restaurants',
        'http://www.yellowpages.com/westlake-village-ca/restaurants',
        'http://www.yellowpages.com/agoura-hills-ca/restaurants',
        'http://www.yellowpages.com/calabasas-ca/restaurants'
    ]
    
    def parse(self, response):
        
        hxs = HtmlXPathSelector(response)
        base_url = get_base_url(response)
        
        # used to keep from parsing pages if we hit an error 
        last_page = False
        cnt = 0
        # get the responses section 
        sites = hxs.select("//div[@class='listing-content']")
        for site in sites:
            cnt += 1
            item = DisplayItem()
            item['name'] = site.select(".//a[@class='url ']/text()").extract()
            item['address'] = site.select(".//span[@class='street-address']/text()").extract()
            item['city'] = site.select(".//span[@class='locality']/text()").extract()
            item['state'] = site.select(".//span[@class='region']/text()").extract()
            item['zip'] = site.select(".//span[@class='postal-code']/text()").extract()
            item['phone1'] = site.select(".//span[@class='business-phone phone']/text()").extract()
            item['phone2'] = site.select(".//span[@class='additional-phones']/text()").extract()
            item['rank'] = site.select(".//div[@class='result-rating']//p[contains(@class,'average')]/text()").extract()
            item['website'] = site.select(".//a[@class='track-visit-website']/@href").extract()
            item['page_link'] = site.select(".//a[@class='url ']/@href").extract()
            item['latitude'] = site.select(".//span[@class='latitude']/text()").extract()
            item['longitude'] = site.select(".//span[@class='longitude']/text()").extract()
            item['request_url'] = response.url
            # we are finding cities listed now which are not part of the URL we are testing
            # break from these and pick them up later
            try:
                print "parsed page: \n " + item['name'][0] + "Inside city: " + item['city'][0]
            except Exception as inst:
                print type(inst)
                print inst.args
                print inst
                print "Failed to parse record for " + response.url + " on record " + str(cnt)
                continue
            
            if(response.url.find(item['city'][0].lower().replace(' ','-')) < 1):
                last_page = True
                print "WE were broken here with URL: " + response.url + " AND " + item['city'][0].lower().replace(' ','-') + "\n"
                break
            yield item
        
        next_url = hxs.select("//li[@class='next']/a/@href").extract()
        if ((len(next_url) > 0) and not last_page ):
            url = urljoin_rfc(base_url, next_url[0])
            yield Request(url, callback=self.parse)
            