# -*- coding: utf-8 -*-
import scrapy


class NaukriSpider(scrapy.Spider):
    # url = "https://www.naukri.com/data-analyst-jobs-in-ncr"
    name = 'naukri'
    subUrl = "data-analyst-jobs-in-ncr/"
    allowed_domains = ['naukri.com']
    start_urls = ["https://www.naukri.com/data-analyst-jobs-in-ncr/"]

    def parse(self, response):
        for job in response.xpath("//div[@type='tuple']"):
            item = {
                "title": job.xpath("a/ul/li[@class='desig']/@title").extract_first(),
                "url": job.xpath("a/@href").extract_first(),

                "company": job.xpath("a/span/span[@class='org']/text()").extract_first(),
                "ratings": job.xpath("a/span/span[@class='rating']/text()").extract_first(),

                "reviews": job.xpath("a/span/span[@class='rating']\
                        /span[@class='review']/text()").extract_first(),


                "expierence": job.xpath("a/span[@class='exp']/text()").extract_first(),
                "location": job.xpath("a/span[@class='loc']/span/text()").extract_first(),
                "keyskills": job.xpath("a/div[@class='more']/div[@class='desc']\
                                    /span[@class='skill']/text()").extract_first(),

                "desc": job.xpath("a/div[@class='more']\
                                    /span[@class='desc']/text()").extract_first(),

                "salary": job.xpath("div[@class='other_details']//\
                            span[@class='salary  ']/text()").extract_first(),

                "posted_by": job.xpath("div[@class='other_details']/\
                            div[@class='rec_details']/a[@class='rec_name']/text()").extract_first(),

                "posted_on": job.xpath("div[@class='other_details']/\
                            div[@class='rec_details']/span[@class='date']/text()").extract_first(),
            }
            yield item

        next_page_url = response.xpath("//div[@class='pagination']/a/@href").extract()[-1]
        if next_page_url:
            request = scrapy.Request(url=next_page_url)
            yield request



