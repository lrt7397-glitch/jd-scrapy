"""
运行示例：
  python -m scrapy crawl jd_search -a keyword=衣服 -a pages=3
"""

import json
import urllib.parse

import scrapy

from jd_scrapy.items import JdScrapyItem
class JdSearchSpider(scrapy.Spider):
    name = "jd_search"  # 爬虫名称，命令行用 scrapy crawl jd_search 调用


    # 本爬虫专属配置（与全局 settings.py 合并，此处优先级更高）
    custom_settings = {
        "DOWNLOAD_DELAY": 1,                   # 每次请求间隔 1 秒，降低被封风险
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,   # 单域名并发数限制为 2
        "COOKIES_ENABLED": True,               # 必须启用 cookies，否则带不上登录态
    }

    # 浏览器抓包得到的 cookies（登录态 + 风控指纹），缺这些会被 302 到风控页
    COOKIES = {
        
    }

    # 浏览器抓包得到的请求头
    HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36 Edg/155.0.0.0",
    }

 
    #必填字段"adInfo","pageUuid"
    # 分页接口的固定参数（adInfo/pageUuid 来自抓包），keyword 和 page 动态注入  
    PARAMS = {
        # "adInfo": ,
        # "pageUuid": ,         
    }

    # 分页接口 URL
    API_URL = "https://re.jd.com/pcSearch/pageing"

    def __init__(self, keyword="衣服", pages="1", *args, **kwargs):
        """
        接收命令行参数：
          keyword: 搜索关键词，默认"衣服"
          pages:   爬取的页数，默认 1 页（每页约 48 个商品）
        用法：-a keyword=手机 -a pages=3
        """
        super(JdSearchSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.pages = int(pages)

    def start_requests(self):
        """为每一页构造一个带 cookies/headers 的 JSON 接口请求"""
        for page in range(1, self.pages + 1):
            params = dict(self.PARAMS)
            params["keyword"] = self.keyword   # 注入搜索关键词
            params["page"] = str(page)         # 注入页码
            url = self.API_URL + "?" + urllib.parse.urlencode(params)
            # referer 带上关键词，让请求看起来像从搜索页翻页触发
            headers = dict(self.HEADERS)
            # headers["referer"] = "https://re.jd.com/search?keyword=%s" % urllib.parse.quote(self.keyword)
            yield scrapy.Request(
                url=url,
                headers=headers,
                cookies=self.COOKIES,
                callback=self.parse,
                meta={"page": page},
                dont_filter=True,
            )

    def parse(self, response):
        """解析 JSON 接口：从 data.products 逐条提取商品字段"""
        page = response.meta.get("page", 0)
        try:
            data = json.loads(response.text)
        except Exception as e:
            self.logger.error("第 %d 页 JSON 解析失败: %s；响应长度=%d", page, e, len(response.text))
            return

        root = data.get("data") or {}
        products = root.get("products") or []
        total = root.get("totalCount")
        total_pages = root.get("totalPages")
        self.logger.info(
            "第 %d 页：返回 %d 个商品（totalCount=%s totalPages=%s）",
            page, len(products), total, total_pages,
        )

        count = 0
        for goods in products:
            if not isinstance(goods, dict):
                continue
            item = JdScrapyItem()
            item["keyword"] = self.keyword
            item["title"] = goods.get("title", "")
            item["shopName"] = goods.get("shopName", "")
            item["price"] = goods.get("price", "")
            item["landUrl"] = goods.get("landUrl", "")
            count += 1
            yield item
        self.logger.info("第 %d 页解析完成，产出 %d 个商品", page, count)