import scrapy
from scrapy_selenium import SeleniumRequest

class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["www.yesstyle.com"]
    start_urls = ["https://www.yesstyle.com/en/beauty-face-cleansers/list.html/bcc.15545_bpt.46#/s=10&l=1&bt=37&bpt=46&bcc=15545&sb=136&pn=1"]

    def start_requests(self):
        url = "https://www.yesstyle.com/en/beauty-face-cleansers/list.html/bcc.15545_bpt.46#/s=10&l=1&bt=37&bpt=46&bcc=15545&sb=136&pn=1"
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        # select all product elements and iterate over them
        for product in response.css("div.itemContainer"):
            # scrape the desired data from each product
            url = product.css("a").attrib["href"]
            image = product.css("a div.itemCover img::attr(src)").get()
            name = product.css("a div.itemContent div.itemTitle::text").get().strip() 
            price = product.css("a div.itemContent div.itemPrice span::text").get()

            # image = product.css(".card-img-top").attrib["src"]
            # name = product.css("h4 a::text").get()
            # price = product.css("h5::text").get()
    
            # add the data to the list of scraped items
            yield {
                "url": url,
                "image": image,
                "name": name,
                "price": price
            }

        # getting pagination links
        pagination_elements = response.css('span[data-ng-repeat="page in pagination.intermediatePages"] > a')

        for page in pagination_elements:
            href = page.attrib["href"]
            yield SeleniumRequest(
                url=response.urljoin(href),
                callback=self.parse,
                wait_time=3,              # let the JS render
                wait_until=lambda d: d.find_element_by_css_selector("div.itemContainer")
            )

        # for element in pagination_elements:
        #     link_url = element.attrib["href"]
        # if link_url:
        #     yield scrapy.Request(response.urljoin(link_url))