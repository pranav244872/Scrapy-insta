import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()

            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield response.follow(book_url, callback = self.parse_book_page)
        
        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback = self.parse)
    
    def parse_book_page(self, response):
        table_rows = response.css("table tr")
        yield {
            'URL': response.url,
            'TITLE':response.css('.product main h1::text').get(),
            'PRODUCT TYPE': table_rows[1].css('td ::text').get(),
            'PRICE EXCLUDING TAX': table_rows[2].css('td ::text').get(),
            'PRIC INCLUDING TAX': table_rows[3].css('td ::text').get(),
            'TAX': table_rows[4].css('td ::text').get(),
            'AVAILABILITY':table_rows[5].css('td ::text').get(),
            'NUM OF REVIEWS': table_rows[6].css('td ::text').get(),
            'STARS': response.css('p.star-rating').attrib['class'],
            'CATEGORY': response.xpath("//ul[@class='breadcrumb']/li[@class = 'active']/preceding-sibling::li[1]/a/text()[normalize-space()]").get().strip(),
            'DESCRIPTION': response.xpath("/html/body/div/div/div[2]/div[2]/article/p/text()[normalize-space()]").get().strip(),
            'PRICE': response.xpath("/html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/p[1]/text()").get().strip(),
        }