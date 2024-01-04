import scrapy
from ..items import Covid19Item


class CovidSpider(scrapy.Spider):
    """
    Spider to scrape COVID-19 related data from 'https://covid19.gov.vn'.
    """

    name = "covid"
    allowed_domains = ["covid19.gov.vn"]
    url1 = 'https://covid19.gov.vn/timelinebigstory/1d44b380-0adb-11ec-bf1c-e9c9e7c491f4'
    url2 = 'https://covid19.gov.vn/timelinebigstory/77be6f00-0ada-11ec-bb49-178244d0bacf'

    urls = []

    # Generate a list of URLs for scraping
    for i in range(1, 33):
        urls.append(f'{url1}/{i}.htm')

    for i in range(1, 97):
        urls.append(f'{url2}/{i}.htm')

    def start_requests(self):
        """
        Generate start requests for each URL in the spider's 'urls' list.
        """
        for url in self.urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'url': url}
            )

    def parse(self, response):
        """
        Parse the response and extract COVID-19 related data.

        Args:
            response (scrapy.http.Response): The response object.

        Yields:
            Covid19Item: An item containing COVID-19 related data.
        """
        for item in response.css('li.timeline-item'):
            covid_item = Covid19Item()

            # Extracting time and new cases information
            covid_item['time'] = item.css('div.timeago::text').get()
            covid_item['new_cases'] = item.css('div.item-bigstory-tit>h3::text').get()

            # Extracting city cases information
            contents = item.css('div.kbwscwl-content').getall()
            for content in contents:
                covid_item['city_cases'] = content

                # Yield the item to be processed further or stored in the output
                yield covid_item
