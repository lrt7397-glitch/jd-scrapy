

import scrapy


class JdScrapyItem(scrapy.Item):
    """京东商品数据项，每个 scrapy.Field() 定义一个可填充字段"""

    keyword = scrapy.Field()      # 搜索关键词，标识该商品由哪个关键词搜出
    title = scrapy.Field()        # 商品标题

    shopName = scrapy.Field()     # 店铺名称
    price = scrapy.Field()        # 商品价格
    landUrl = scrapy.Field()      # 商品详情页链接
