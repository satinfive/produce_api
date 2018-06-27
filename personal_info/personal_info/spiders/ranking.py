import scrapy
import scrapy_splash
import csv
from .utils import kor_to_utf8, get_current_ranking


class PersonalSpider(scrapy.Spider):

    name = "ranking"

    start_urls = [get_current_ranking(),
                  ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy_splash.SplashRequest(url=url, callback=self.parse, endpoint='render.html')

    def parse(self, response):

        rank_ep = response.url.split('/')[-1]
        rows = [['name', 'rank_name']]

        rank_el = [li for li in response.css('li')
                   if 'profile' in li.css('a::attr(href)').extract()[0]
                   and li.css('a::attr(href)').extract()[0].split('/')[-1] != '0']

        for el in rank_el:
            rank_num = el.css('span::text').extract()[0]
            name = el.css('a::text').extract()[-1]
            rows.append([kor_to_utf8(name), rank_num])

        with open('ranking_data_' + rank_ep + '.csv', 'w') as csv_f:

            writer = csv.writer(csv_f)
            writer.writerows(rows)