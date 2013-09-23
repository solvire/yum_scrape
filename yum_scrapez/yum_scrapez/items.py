# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class YumScrapezItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class DisplayItem(Item):
    
    name = Field()
    address = Field()
    city = Field()
    state = Field()
    zip = Field()
    phone1 = Field()
    phone2 = Field()
    rank = Field()
    website = Field()
    page_link = Field()
    latitude = Field()
    longitude = Field()
    request_url = Field()
    pass

    def cleanup(self):
        return