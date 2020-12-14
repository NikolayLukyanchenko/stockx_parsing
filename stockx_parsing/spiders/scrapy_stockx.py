import scrapy
from scrapy.loader import ItemLoader
from scrapy.spiders import SitemapSpider
from scrapy.loader.processors import TakeFirst, MapCompose, Join
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


# class StockxSpider(scrapy.Spider):
#     name = 'stock'
#     # allowed_domains = ['clever-lichterman-044f16.netlify.com']
#     start_urls = ['https://stockx.com/air-jordan-4-retro-fire-red-2020']    #1
# #     start_urls = ['https://stockx.com/adidas-yeezy-boost-350-v2-zyon']    #2
# #     start_urls = ['https://stockx.com/nike-air-force-1-low-supreme-box-logo-white']   #3
# #     start_urls = ['https://stockx.com/louis-vuitton-don-kanye-red'] #4
# #     start_urls = ['https://stockx.com/dior-b23-high-top-blue-oblique'] #5
# #     start_urls = ['https://stockx.com/supreme-cross-box-logo-hooded-sweatshirt-heather-grey'] #6 !!!
# #     start_urls = ['https://stockx.com/fear-of-god-essentials-3d-silicon-applique-pullover-hoodie-dark-slate'] #7 !!!
# #     start_urls = ['https://stockx.com/supreme-honda-fox-racing-vue-goggles-red'] #8 !!!
# #     start_urls = ['https://stockx.com/sony-ps5-playstation-5-pulse-3d-wireless-headset-white'] #9
# #     start_urls = ['https://stockx.com/apple-airpods-pro-mwp22am-a'] #10
# #     start_urls = ['https://stockx.com/louis-vuitton-key-pouch-monogram-canvas-brown'] #11
# #     start_urls = ['https://stockx.com/apple-watch-series-5-gps-44mm-space-gray-aluminum-with-black-sport-band-black']  # 12
# #     start_urls = ['https://stockx.com/omega-seamaster-21030422001001-black']  # 13
# #     start_urls = ['https://stockx.com/supreme-cross-box-logo-hooded-sweatshirt-heather-grey'] #14
#
#
#     def parse(self, response):
#         item = Product()
#         # item['product_name'] = response.xpath("/html/head/title/text()").get()
#         item['product_name'] = response.xpath("//div[@class='product-view']//h1/text()").get()
#         # item['product_category'] = response.xpath("/html/body/div[1]/div[1]/div[2]/div[2]/span/div[1]/div/div/ul/li[3]/a/text()").getall()
#         item['product_category'] = response.xpath("//div[@class='grails-crumbs']/ul/li[2]/a/text()").get()
#         item['product_subcategory'] = response.xpath("//div[@class='grails-crumbs']/ul/li[3]/a/text()").get()
#         item['product_subsubcategory'] = response.xpath("//div[@class='grails-crumbs']/ul/li[4]/a/text()").get()
#         # item['product_ticker'] = response.xpath("//div[@class='header-stat']/span/text()").get()
#         # item['product_ticker'] = remove_blank_symbol(response.xpath("//span[@class='soft-black']/text()").get())
#         product_ticker_v1 = remove_blank_symbol(response.xpath("//span[@class='soft-black']/text()").get())
#         product_ticker_v2 = response.xpath("//div[@class='right']/ul/li[4]/span[2]/span/p[2]/text()").get()
#         if product_ticker_v1 is not None:
#             item['product_ticker'] = product_ticker_v1
#         elif product_ticker_v2 is not None:
#             item['product_ticker'] = product_ticker_v2
#         else:
#             item['product_ticker'] = None
#         # item['product_ticker'] = response.xpath("//div[@class='right']/ul/li[4]/span[2]/span/p[2]/text()").get()
#         last_sale_price_v1 = response.xpath("//div[@class='sale-value']/text()").get()
#         last_sale_price_v2 = response.xpath("//div[@class='right']/ul/li/span/span/p[2]/text()").get()
#         if last_sale_price_v1 is not None:
#             item['last_sale_price'] = last_sale_price_v1
#         elif last_sale_price_v2 is not None:
#             item['last_sale_price'] = last_sale_price_v2
#         else:
#             item['last_sale_price'] = None
#         item['lowest_ask_price'] = response.xpath("//div[@class='bid bid-button-b']/div/a/div/div/text()").get()
#         item['highest_bid_price'] = response.xpath("//div[@class='ask ask-button-b']/div/a/div/div/text()").get()
#         retail_price_v1 = remove_blank_symbol(response.xpath("//span[@data-testid='product-detail-retail price']/text()").get())
#         retail_price_v2 = remove_blank_symbol(response.xpath("//span[@data-testid='product-detail-retail']/text()").get())
#         # retail_price_v3 = response.xpath("//div[@class='right']/ul/li[4]/span[2]/span[3]/p[2]/text()").get()
#         retail_price_v3 = response.xpath("//div[@class='right']/ul/li/span[2]/span[8]/p[2]/text()").get()
#         if retail_price_v1 is not None:
#             item['retail_price'] = retail_price_v1
#         elif retail_price_v2 is not None:
#             item['retail_price'] = retail_price_v2
#         elif retail_price_v3 is not None:
#             item['retail_price'] = retail_price_v3
#         else:
#             item['retail_price'] = None
#         item['release_date'] = remove_blank_symbol(response.xpath("//span[@data-testid='product-detail-release date']/text()").get())
#         # item['description'] = response.xpath("//div[@class='product-description description-expanded ']/p/text()").get()
#         description_v1 = response.xpath("//div[@class='product-description description-expanded ']/p/text()").get()
#         description_v2 = response.xpath("//div[@class='product-description description-expanded ']//b/text()").getall()
#         description_v3 = response.xpath("//div[@class='product-description description-condensed ']/p/text()").getall()
#         # item['description'] = description_v3
#         if description_v1 is not None:
#             item['description'] = description_v1
#         elif description_v2:
#             item['description'] = description_v2
#         elif description_v3:
#             item['description'] = description_v3
#         else:
#             item['description'] = None
#
#         # img_urls_1 = response.xpath("//div[@class='image-container']//img/@src").getall()
#         # img_urls_2 = response.xpath("//div[@class='product-media ']//img/@src").getall()
#         img_urls_1 = response.xpath("//div[@class='full ']//img/@src").getall()
#         img_urls_2 = response.xpath("//div[@class='full hidden-xs']//img/@src").getall()
#         img_urls_3 = response.xpath("//div[@class='product-gallery hidden-xs']//img/@src").getall()
#         img_urls_4 = response.xpath("//div[@class='product-hero']//img/@src").getall()
#         item['img_urls'] = img_urls_1 + img_urls_2 + img_urls_3 + img_urls_4
#         # item['img_urls_2'] = response.xpath("//div[@class='image-container']//img/@srcset").getall()
#         # item['product_name'] = response.xpath("//div[@class='pr2-sm css-1ou6bb2']/h1/text()").get()
#         # item['product_category'] = response.xpath("//div[class='grails-crumbs']/ul/li/text()").getall()
#         # item['product_category'] = response.xpath("/html/body/div[1]/div[1]/div[2]/div[2]/span/div[1]/div/div/ul/li[3]/a/text()").getall()
#
#         item['product_url'] = response.url
#         return item

#################################################################################################
class StockxSpider(SitemapSpider):
    name = 'stock'
    sitemap_urls = ['https://stockx.com/sitemap/sitemap-0.xml']
    # handle_httpstatus_list = [403]

    def parse(self, response):
        item = Product()
        item['product_name'] = response.xpath("//div[@class='product-view']//h1/text()").get()
        # item['product_category'] = response.xpath("/html/body/div[1]/div[1]/div[2]/div[2]/span/div[1]/div/div/ul/li[3]/a/text()").getall()
        item['product_category'] = response.xpath("//div[@class='grails-crumbs']/ul/li[2]/a/text()").get()
        item['product_subcategory'] = response.xpath("//div[@class='grails-crumbs']/ul/li[3]/a/text()").get()
        item['product_subsubcategory'] = response.xpath("//div[@class='grails-crumbs']/ul/li[4]/a/text()").get()
        # item['product_ticker'] = response.xpath("//div[@class='header-stat']/span/text()").get()
        # item['product_ticker'] = remove_blank_symbol(response.xpath("//span[@class='soft-black']/text()").get())
        product_ticker_v1 = remove_blank_symbol(response.xpath("//span[@class='soft-black']/text()").get())
        product_ticker_v2 = response.xpath("//div[@class='right']/ul/li[4]/span[2]/span/p[2]/text()").get()
        if product_ticker_v1 is not None:
            item['product_ticker'] = product_ticker_v1
        elif product_ticker_v2 is not None:
            item['product_ticker'] = product_ticker_v2
        else:
            item['product_ticker'] = None
        # item['product_ticker'] = response.xpath("//div[@class='right']/ul/li[4]/span[2]/span/p[2]/text()").get()
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
        # retail_price_v3 = response.xpath("//div[@class='right']/ul/li[4]/span[2]/span[3]/p[2]/text()").get()
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
        # item['description'] = response.xpath("//div[@class='product-description description-expanded ']/p/text()").get()
        description_v1 = response.xpath("//div[@class='product-description description-expanded ']/p/text()").get()
        description_v2 = response.xpath("//div[@class='product-description description-expanded ']//b/text()").getall()
        description_v3 = response.xpath("//div[@class='product-description description-condensed ']/p/text()").getall()
        # item['description'] = description_v3
        if description_v1 is not None:
            item['description'] = description_v1
        elif description_v2:
            item['description'] = description_v2
        elif description_v3:
            item['description'] = description_v3
        else:
            item['description'] = None
        # img_urls_1 = response.xpath("//div[@class='image-container']//img/@src").getall()
        # img_urls_2 = response.xpath("//div[@class='product-media ']//img/@src").getall()
        img_urls_1 = response.xpath("//div[@class='full ']//img/@src").getall()
        img_urls_2 = response.xpath("//div[@class='full hidden-xs']//img/@src").getall()
        img_urls_3 = response.xpath("//div[@class='product-gallery hidden-xs']//img/@src").getall()
        img_urls_4 = response.xpath("//div[@class='product-hero']//img/@src").getall()
        item['img_urls'] = img_urls_1 + img_urls_2 + img_urls_3 + img_urls_4
        item['product_url'] = response.url

        test = response.xpath("//div[@class='product-view']//h1/text()").get()

        # if test is not None:
        return item

