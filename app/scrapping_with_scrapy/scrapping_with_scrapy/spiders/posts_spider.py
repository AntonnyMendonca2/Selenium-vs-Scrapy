import scrapy
import logging

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler("scrapy.log"),
                              logging.StreamHandler()])

class ScrappingWithScrapt(scrapy.Spider):
    name = "spider"
    start_urls = ["https://www.metacritic.com/browse/games/score/metascore/all/all/filtered"]

    def parse(self, response):
        try:
            for post in response.css('.clamp-list > tr'):
                yield {
                    'title': post.css('.title h3::text').get(),
                    'plataform':post.css('td.clamp-summary-wrap > div.clamp-details > div > span.data::text').get(),
                    'release_date': post.css('div.clamp-details > span::text').get(),
                    'rate': post.css('div.clamp-metascore > a > div::text').get(),
                    'sumary': post.css('td.clamp-summary-wrap > div.summary::text').get()
                }
                next_page = response.css('div.page_flipper > span.flipper.next > a::attr(href)').get()
                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)
        except Exception as e:
            logging.warning("'\033[93m' Houve um erro ao encontrar o elemento de classe '.clamp-list', confira se a classe da div foi alterado no site'\033[0m")

