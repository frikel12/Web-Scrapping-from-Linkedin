# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StageprojectItem(scrapy.Item):

    title = scrapy.Field()
    post_url = scrapy.Field()
    company_name = scrapy.Field()
    company_location = scrapy.Field()
    post_description = scrapy.Field()
    scraped_date = scrapy.Field()


