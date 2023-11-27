import scrapy
from StageProject.items import StageprojectItem
from datetime import date


class LinkedinSpider(scrapy.Spider):
    name = "linkedin"
    url = 'https://fr.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/stage-emplois?position=1&pageNum=0&f_TPR=r86400&start='

    def start_requests(self):
        counter = 0
        url = self.url + str(counter)
        yield scrapy.Request(url, callback=self.parse, meta={'counter': counter})

    def parse(self, response):
        counter = response.meta['counter']
        if response.status == 200:
            posts = response.xpath("//li")
            for post in posts:
                post_item = StageprojectItem()
                post_item['title'] = post.xpath('div/a/span/text()').get(default='not-found').strip()
                post_item['post_url'] = post.xpath('div/a/@href').get(default='not-found').strip()
                post_item['company_name'] = post.xpath('div/div/h4/a/text()').get(default='not-found').strip()
                post_item['company_location'] = post.xpath('div/div/div/span/text()').get(default='not-found').strip()
                post_item['scraped_date'] = date.today().strftime("%d/%m/%Y")
                yield scrapy.Request(post_item['post_url'], callback=self.parse_post_description, meta={'post_item': post_item})

            counter = int(counter) + 25
            url = self.url + str(counter)
            yield scrapy.Request(url=url, callback=self.parse, meta={'counter': counter})

    def parse_post_description(self, response):
        post_item = response.meta.get('post_item', {})
        #post_item['post_description'] = response.xpath('//div[@class="show-more-less-html__markup show-more-less-html__markup--clamp-after-5"]').get(default='not-found').strip()
        post_item['post_description'] = response.xpath('//main/section/div/div/section/div/div/section/div').get(default='not-found').strip()

        yield post_item



