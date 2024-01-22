
import scrapy

class StackOverflowJSAndCustomQuerySpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['stackoverflow.com']

    def __init__(self, *args, **kwargs):
        super(StackOverflowJSAndCustomQuerySpider, self).__init__(*args, **kwargs)
        # Get custom query from command-line argument
        self.custom_query = kwargs.get('custom_query', None)

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    def start_requests(self):
        # Start with the questions tagged with JavaScript
        yield scrapy.Request(url='https://stackoverflow.com/questions/tagged/javascript', callback=self.parse)

    def parse(self, response):
        # Extracting question titles and links using XPath
        questions = response.xpath('//div[contains(@class, "question-summary")]')

        for question in questions:
            title = question.xpath('.//h3/a/text()').get()
            link = question.xpath('.//h3/a/@href').get()

            if title and link:
                yield {
                    'title': title.strip(),
                    'link': response.urljoin(link),
                }

        # Follow pagination links to scrape additional pages
        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
