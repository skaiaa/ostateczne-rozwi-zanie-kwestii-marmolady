import scrapy

class JamSpider(scrapy.Spider):
	name = 'regionaljams'

	allowed_domains = ['www.minrol.gov.pl']

	start_urls = ['https://www.minrol.gov.pl/pol/Jakosc-zywnosci/Produkty-regionalne-i-tradycyjne/Lista-produktow-tradycyjnych/(pid)/333']

	custom_settings = {
		'FEED_FORMAT': 'xml',
        'FEED_URI' : '../data/regional_products.xml'
    }

	def parse(self, response):
		PRODUCT_SELECTOR = '//main//article/a/@href'

		for product_url in response.xpath(PRODUCT_SELECTOR).extract():
			# print(product_url)
			yield scrapy.Request(
				response.urljoin(product_url), 
				callback=self.parse_product)


	def parse_product(self, response):
		section = response.css('section.content-view-full')

		attributes = section.css('p::text').extract()

		yield {
			'name': section.css('header::text').extract_first(),
			'appearance': attributes[0],
			'form': attributes[1],
			'size': attributes[2],
			'color': attributes[3],
			'consistency': attributes[4],
			'flavor': attributes[5],
			# 'info': attributes[6],
			# 'tradition': attributes[7]
		}