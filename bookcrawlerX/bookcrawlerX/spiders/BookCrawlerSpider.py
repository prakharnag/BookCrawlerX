import os
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookCrawlerSpider(CrawlSpider):
    name = "BookCrawlerSpider"
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
            "availability": response.css(".availability::text")[1].get()
        }
        
        # Extract name from URL using regular expression
        url_pattern = r"http:\/\/books\.toscrape\.com\/catalogue\/([a-zA-Z0-9-]+)_[0-9]+\/index\.html"
        match = re.match(url_pattern, response.url)
        if match:
            name = match.group(1)
            filename = f"{name}.html"
        else:
            filename = "unknown.html"
        
        # Save HTML content
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
