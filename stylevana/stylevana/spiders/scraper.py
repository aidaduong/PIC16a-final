import scrapy
from scrapy_selenium import SeleniumRequest

class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["www.stylevana.com"]
    start_urls = ["https://www.stylevana.com/en_US/skincare/face-care/sunscreen.html"]

    def start_requests(self):
        url = "https://www.stylevana.com/en_US/skincare/face-care/sunscreen.html"

        yield SeleniumRequest(url=url, callback=self.parse)

    # def parse(self, response):
    #     # select all product elements and iterate over them
    #     for product in response.css("li.product-item"):
    #         # scrape the desired data from each product
    #         url = product.css("a.product-item-link::attr(href)").get(default="").strip()
    #         if not url:
    #             continue
    #         page_url = response.urljoin(url)
    #         yield SeleniumRequest(url = page_url, 
    #                               callback=self.parse_item,
    #                               cb_kwargs={"page_url": page_url})
    #         # image = product.css("img.product-image-photo::attr(src)").get(default="").strip()
    #         # name = product.css("a.product-item-link::text").get(default="").strip()
    #         # price = product.css("span.normal-price span.price::text").get(default="").strip()
    
    #         # # add the data to the list of scraped items
    #         # yield {
    #         #     "url": url,
    #         #     "image": image,
    #         #     "name": name,
    #         #     "price": price
    #         # }
        

    #     # pagination_link_elements = response.css("a.page")
        
    #     # for pagination_link_element in pagination_link_elements:
    #     #     pagination_link_url = pagination_link_element.attrib["href"]
    #     #     if pagination_link_url:
    #     #         yield scrapy.Request(
    #     #             response.urljoin(pagination_link_url)
    #     #         )

    # def parse_item(self, response, page_url):
    #     image = response.css("img.fotorama__img::attr(src)").get(default="").strip()
    #     name = response.css("h1.page-title::text").get(default="").strip()
    #     price = response.css("span.normal-price span.price::text").get(default="").strip()
    #     brand = response.css("a.product-name::text").get(default="").strip()

    #     yield {
    #             "url": page_url,
    #             "image": image,
    #             "name": name,
    #             "price": price,
    #             "brand": brand
    #         }

    # def parse_reviews(self,response):

    def parse(self, response):
        # select all product elements and iterate over them
        for product in response.css("li.product-item"):
            # scrape the desired data from each product
            url = product.css("a.product-item-photo::attr(href)").get(default="").strip()
            image = product.css("img.product-image-photo::attr(src)").get(default="").strip()
            name = product.css("a.product-item-link::text").get(default="").strip()
            price = product.css("span.normal-price span.price::text").get(default="").strip()
    
            # add the data to the list of scraped items
            yield {
                "url": url,
                "image": image,
                "name": name,
                "price": price
            }
        

        pagination_link_elements = response.css("a.page")
        
        for pagination_link_element in pagination_link_elements:
            pagination_link_url = pagination_link_element.attrib["href"]
            if pagination_link_url:
                yield scrapy.Request(
                    response.urljoin(pagination_link_url)
                )