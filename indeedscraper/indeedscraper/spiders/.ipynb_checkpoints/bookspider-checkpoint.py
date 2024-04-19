import os
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookCrawlerSpider(CrawlSpider):
    name = "bookcrawlerspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]
    max_pages = 10  # Maximum number of pages to crawl
    max_depth = 3   # Maximum depth of the crawling process

    rules = (
        Rule(LinkExtractor(allow="catalogue/category"), follow=True),
        Rule(LinkExtractor(allow="catalogue", deny="category"), callback="parse_books"),
    )

    def __init__(self, *args, **kwargs):
        super(BookCrawlerSpider, self).__init__(*args, **kwargs)
        self.visited_pages = 0
        self.depth = 1

    def parse_books(self, response):
        # Extract data as before
        item = {
            "title": response.css(".product_main h1::text").get(),
            "price": response.css(".price_color::text").get(),
            "availability": response.css(".availability::text")[1].get(),
            "rating": response.xpath('//p[@class="star-rating Three"]/@class').re_first(r'(\b\w+\b)$'),
            "description": response.css('#product_description + p::text').get()
        }
        # Save HTML content
        filename = f'{response.url.replace("http://", "").replace("https://", "").replace(".", "_").replace("/", "_")}.html'
        filename = os.path.join("html_files", filename)  # Save files in "html_files" directory
        os.makedirs(os.path.dirname(filename), exist_ok=True)  # Create directory if it doesn't exist
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
        yield item

        # Update page count and check for max pages
        self.visited_pages += 1
        if self.visited_pages >= self.max_pages:
            self.log(f"Reached maximum pages limit of {self.max_pages}. Crawling stopped.")
            return

        # Check depth and follow links if within maximum depth
        if self.depth < self.max_depth:
            self.depth += 1
            for link in response.css('a::attr(href)').extract():
                yield scrapy.Request(response.urljoin(link), callback=self.parse)

    def closed(self, reason):
        self.log(f"Crawler closed: {reason}")
