import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["www.stylevana.com"]
    # start_urls = ["https://www.stylevana.com/en_US/skincare/face-care/sunscreen.html"]
    # start_urls = ["https://www.stylevana.com/en_US/skincare/face-care/moisturizer-cream.html"]
    # start_urls = ["https://www.stylevana.com/en_US/skincare/face-care/essence-serum.html"]
    # start_urls = ["https://www.stylevana.com/en_US/skincare/face-care/toner-mist.html"]
    start_urls = ["https://www.stylevana.com/en_US/skincare/facial-cleanser/face-wash-cleansers.html"]

    def start_requests(self):
        base_url = self.start_urls[0]

        # pagination - iterate thru the first 3 pages
        # the pagination is done by adding ?p=1, ?p=2, etc. to the URL
        for page in range(1, 4):    
            url = f"{base_url}?p={page}"

            # yield a SeleniumRequest for each page (ChatGPT-plus 30 May 2025)
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,                                       
                wait_until=EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "li.product-item")
                ),
                dont_filter=True
            )

    def parse(self, response):
        # select all product elements and iterate over them
        for product in response.css("li.product-item"):
            # scrape the desired data from each product
            url = product.css("a.product-item-link::attr(href)").get()
            if not url:
                continue
            page_url = response.urljoin(url)

            # yield a SeleniumRequest for each product page (ChatGPT-plus 30 May 2025)
            yield SeleniumRequest(url = page_url, 
                                  callback=self.parse_item,
                                  wait_time=10,
                                  wait_until=EC.presence_of_element_located(
                                    #   (By.CSS_SELECTOR, "span.avg-score")
                                        (By.CSS_SELECTOR, "span.normal-price")
                                      )
                                  )

    def parse_item(self, response):

        # get the CSS selectors for various information (ChatGPT-plus 30 May 2025)
        # fill NA values with empty strings
        url = response.url

        image = response.css("div.fotorama__stage__shaft img.fotorama__img::attr(src)").get(default="").strip()
        name = response.css("h1.page-title .base::text").get(default="").strip()
        price = response.css("span.normal-price span.price::text").get(default="").strip()
        brand = response.css("div.product-brand-wrapper a.product-brand::text").get(default="").strip()

        star = response.css("span.avg-score::text").get(default="NA").strip()
        num_reviews = response.css("span.reviews-amount::text").get(default="0").strip()

        info = {
            "url" : url, 
            "image" : image, 
            "name" : name, 
            "price" : price, 
            "brand" : brand,
            "star" : star,
            "num_reviews" : num_reviews.split()[0] if num_reviews else "0" # get the first string from num_reviews, since it's like "25 reviews"
            }

        yield info 