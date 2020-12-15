import scrapy
from scrapy.loader import ItemLoader
from scrapy.spiders import SitemapSpider
from scrapy.spiders import CrawlSpider


class Product(scrapy.Item):
    product_url = scrapy.Field()
    product_name = scrapy.Field()
    product_category = scrapy.Field()
    product_subcategory = scrapy.Field()
    product_subsubcategory = scrapy.Field()
    product_ticker = scrapy.Field()
    last_sale_price = scrapy.Field()
    lowest_ask_price = scrapy.Field()
    highest_bid_price = scrapy.Field()
    retail_price = scrapy.Field()
    release_date = scrapy.Field()
    description = scrapy.Field()
    img_urls = scrapy.Field()


def remove_blank_symbol(value):
    if value is not None:
        value = value.replace(' ', '')
    return value


class StockxSpider(SitemapSpider):
    name = 'stock'
    sitemap_urls = ['https://stockx.com/sitemap/sitemap-0.xml']
    # sitemap_urls = ['https://stockx.com/sitemap/sitemap-1.xml']
    # sitemap_urls = ['https://stockx.com/sitemap/sitemap-2.xml']
    # sitemap_urls = ['https://stockx.com/sitemap/sitemap-3.xml']

    def parse(self, response):
        item = Product()
        item['product_name'] = response.xpath("//div[@class='product-view']//h1/text()").get()
        item['product_category'] = response.xpath("//div[@class='grails-crumbs']/ul/li[2]/a/text()").get()
        item['product_subcategory'] = response.xpath("//div[@class='grails-crumbs']/ul/li[3]/a/text()").get()
        item['product_subsubcategory'] = response.xpath("//div[@class='grails-crumbs']/ul/li[4]/a/text()").get()
        product_ticker_v1 = remove_blank_symbol(response.xpath("//span[@class='soft-black']/text()").get())
        product_ticker_v2 = response.xpath("//div[@class='right']/ul/li[4]/span[2]/span/p[2]/text()").get()
        if product_ticker_v1 is not None:
            item['product_ticker'] = product_ticker_v1
        elif product_ticker_v2 is not None:
            item['product_ticker'] = product_ticker_v2
        else:
            item['product_ticker'] = None
        last_sale_price_v1 = response.xpath("//div[@class='sale-value']/text()").get()
        last_sale_price_v2 = response.xpath("//div[@class='right']/ul/li/span/span/p[2]/text()").get()
        if last_sale_price_v1 is not None:
            item['last_sale_price'] = last_sale_price_v1
        elif last_sale_price_v2 is not None:
            item['last_sale_price'] = last_sale_price_v2
        else:
            item['last_sale_price'] = None
        item['lowest_ask_price'] = response.xpath("//div[@class='bid bid-button-b']/div/a/div/div/text()").get()
        item['highest_bid_price'] = response.xpath("//div[@class='ask ask-button-b']/div/a/div/div/text()").get()
        retail_price_v1 = remove_blank_symbol(response.xpath("//span[@data-testid='product-detail-retail price']/text()").get())
        retail_price_v2 = remove_blank_symbol(response.xpath("//span[@data-testid='product-detail-retail']/text()").get())
        retail_price_v3 = response.xpath("//div[@class='right']/ul/li/span[2]/span[8]/p[2]/text()").get()
        if retail_price_v1 is not None:
            item['retail_price'] = retail_price_v1
        elif retail_price_v2 is not None:
            item['retail_price'] = retail_price_v2
        elif retail_price_v3 is not None:
            item['retail_price'] = retail_price_v3
        else:
            item['retail_price'] = None
        item['release_date'] = remove_blank_symbol(response.xpath("//span[@data-testid='product-detail-release date']/text()").get())
        description_v1 = response.xpath("//div[@class='product-description description-expanded ']/p/text()").get()
        description_v2 = response.xpath("//div[@class='product-description description-expanded ']//b/text()").getall()
        description_v3 = response.xpath("//div[@class='product-description description-condensed ']/p/text()").getall()
        if description_v1 is not None:
            item['description'] = description_v1
        elif description_v2:
            item['description'] = description_v2
        elif description_v3:
            item['description'] = description_v3
        else:
            item['description'] = None
        img_urls_1 = response.xpath("//div[@class='full ']//img/@src").getall()
        img_urls_2 = response.xpath("//div[@class='full hidden-xs']//img/@src").getall()
        img_urls_3 = response.xpath("//div[@class='product-gallery hidden-xs']//img/@src").getall()
        img_urls_4 = response.xpath("//div[@class='product-hero']//img/@src").getall()
        item['img_urls'] = img_urls_1 + img_urls_2 + img_urls_3 + img_urls_4
        item['product_url'] = response.url

        return item

