import scrapy
from StageProject.items import StageprojectItem


class GlassdorSpider(scrapy.Spider):
    name = "glassdor"
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&start='
    api_url = 'https://www.glassdoor.fr/Emploi/index.htm'

    def start_requests(self):
        # first_job_on_page = 0
        # first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=self.api_url, callback=self.parse_job)

    def parse_job(self, response):
        #first_job_on_page = response.meta['first_job_on_page']
        posts = response.xpath('//li[@class = "JobsList_jobListItem__JBBUV"]')

        for post in posts:
            post_item = StageprojectItem()
            post_item['title'] = post.xpath('div/div/div/div/a/text()').get(default='not-found').strip()
            post_item['post_url'] = post.xpath('div/div/div/div/a/@href').get(default='not-found').strip()
            post_item['company_name'] = post.xpath('div/div/div/div/div/div/text()').get(default='not-found').strip()
            post_item['company_location'] = post.xpath('div/div/div/div/div/text()').get(default='not-found').strip()
            yield scrapy.Request(post_item['post_url'], callback=self.parse_post_description, meta={'post_item': post_item})

        # if first_job_on_page <= 150:
        #     first_job_on_page = int(first_job_on_page) + 25
        #     next_url = self.api_url + str(first_job_on_page)
        #     yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

    def parse_post_description(self, response):
        post_item = response.meta.get('post_item', {})
        #post_item['post_description'] = response.xpath('//div[@class="show-more-less-html__markup show-more-less-html__markup--clamp-after-5"]').get(default='not-found').strip()
        post_item['post_description'] = response.xpath('//div[@id = ["JobDesc1008903259224"]').get(default='not-found').strip()

        yield post_item

