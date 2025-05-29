import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["www.stylevana.com"]
    start_urls = ["https://www.stylevana.com/en_US/skincare/face-care/sunscreen.html"]

    # start_urls = ["https://www.stylevana.com/en_US/skincare/face-care/sunscreen.html",
    #               "https://www.stylevana.com/en_US/skincare/face-care/moisturizer-cream.html",
    #               "https://www.stylevana.com/en_US/skincare/face-care/essence-serum.html",
    #               "https://www.stylevana.com/en_US/skincare/face-care/toner-mist.html",
    #               "https://www.stylevana.com/en_US/skincare/facial-cleanser/face-wash-cleansers.html"]

    # start_urls = ["https://www.stylevana.com/en_US/skincare/face-care/toner-mist.html"]

    def start_requests(self):
        base_url = "https://www.stylevana.com/en_US/skincare/face-care/sunscreen.html"
        for page in range(1, 4):    
            if page == 1:
                url = base_url  
            else:
                url = f"{base_url}?p={page}"

            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,                                       # give it up to 10s
                wait_until=EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "li.product-item")
                ),
                dont_filter=True
            )
        # url = "https://www.stylevana.com/en_US/skincare/face-care/sunscreen.html"
        # yield SeleniumRequest(
        #     url= url,
        #     callback=self.parse,
        #     wait_time=3,
        #     wait_until= EC.presence_of_all_elements_located(
        #         (By.CSS_SELECTOR, "li.product-item")
        #     ),
        #     dont_filter=True
        # )

        # for url in self.start_urls:
            # yield SeleniumRequest(
            #         url= url,
            #         callback=self.parse,
            #         wait_time=3,
            #         wait_until= EC.presence_of_all_elements_located(
            #             (By.CSS_SELECTOR, "li.product-item")
            #         ),
            #         dont_filter=True
            #     )

    def parse(self, response):
        # select all product elements and iterate over them
        for product in response.css("li.product-item"):
            # scrape the desired data from each product
            url = product.css("a.product-item-link::attr(href)").get()
            if not url:
                continue
            page_url = response.urljoin(url)

            yield SeleniumRequest(url = page_url, 
                                  callback=self.parse_item,
                                  wait_time=10,
                                  wait_until=EC.presence_of_element_located(
                                      (By.CSS_SELECTOR, "span.avg-score")
                                      )
                                  )
            
        # pagination_links = response.css("a.page::attr(href)").getall()
        # for link in pagination_links[0:3]:
        # # for pagination_link_element in pagination_link_elements:
        #     # pagination_link_url = pagination_link_elements[i].attrib["href"]
        #     if link:
        #         yield SeleniumRequest(url = response.urljoin(link), 
        #                           callback=self.parse,
        #                           wait_time=3,
        #                           dont_filter=True,
        #                           wait_until=EC.presence_of_element_located(
        #                               (By.CSS_SELECTOR, "li.product-item")
        #                               )
        #                           )

    def parse_item(self, response):
        url = response.url
        image = response.css("div.fotorama__stage__shaft img.fotorama__img::attr(src)").get(default="").strip()
        name = response.css("h1.page-title .base::text").get(default="").strip()
        price = response.css("span.normal-price span.price::text").get(default="").strip()
        brand = response.css("div.product-brand-wrapper a.product-brand::text").get(default="").strip()

        star = response.css("span.avg-score::text").get(default="").strip()
        num_reviews = response.css("span.reviews-amount::text").get(default="").strip()

        info = {
            "url" : url, 
            "image" : image, 
            "name" : name, 
            "price" : price, 
            "brand" : brand,
            "star" : star,
            "num_reviews" : num_reviews.split()[0] if num_reviews else "0"
            }

        yield info 
        # review_url = url + "#marketing-channel-review"
        # yield SeleniumRequest(url = review_url,
        #                       callback=self.parse_reviews,
        #                       meta = {"info": info},
        #                       wait_time=10,
        #                       dont_filter=True,
        #                       wait_until=EC.presence_of_element_located(
        #                               (By.CSS_SELECTOR, "h1.page-title")
        #                               )
        #                           )
        
    # def parse_reviews(self, response):
    #     info = response.meta.get("info", {})
    #     star = response.css("div.bottom-line-items span.avg-score::text").get(default="").strip()
    #     num_reviews = response.css("div.reviews-header span.reviews-amount::text").get(default="").strip()

    #     info.update({
    #         "star": star,
    #         "num_reviews": num_reviews.split()[0]
    #     })

    #     yield info