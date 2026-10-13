

# Scrapy settings for jd_scrapy project
#
# For simplicity, this file contains only settings considered important and
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "jd_scrapy"  # 项目名称

# 爬虫代码所在模块，Scrapy 据此发现所有 Spider 类
SPIDER_MODULES = ["jd_scrapy.spiders"]
NEWSPIDER_MODULE = "jd_scrapy.spiders"  # scrapy genspider 生成新爬虫的存放位置

ADDONS = {}


# 浏览器 User-Agent，伪装成 Edge 浏览器绕过最基础的反爬
# （与 spider 内 HEADERS 的 user-agent 保持一致）
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36 Edg/155.0.0.0"
)

# 是否遵守目标站 robots.txt 规则；京东 robots 限制较多，这里关闭以放行搜索页
ROBOTSTXT_OBEY = False

# 限速与并发控制：降低并发、增加间隔，减少被封 IP 风险
CONCURRENT_REQUESTS_PER_DOMAIN = 2  # 单域名最多 2 个并发请求
DOWNLOAD_DELAY = 1                   # 相邻请求间隔 1 秒

# 启用 Cookie：京东搜索页需要登录态/风控 Cookie，必须开启才能带上 spider 里的 cookies
COOKIES_ENABLED = True

# 默认请求头：spider 内已带完整浏览器头，这里仅保留兜底 Referer
DEFAULT_REQUEST_HEADERS = {
    "Referer": "https://re.m.jd.com/",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "jd_scrapy.middlewares.JdScrapySpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "jd_scrapy.middlewares.JdScrapyDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# 启用数据处理管道：JsonPipeline 负责把结果保存为 JSON 文件
# 数字 300 为优先级（越小越先执行）
ITEM_PIPELINES = {
    "jd_scrapy.pipelines.JsonPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
# 导出文件编码设为 utf-8，避免中文乱码
FEED_EXPORT_ENCODING = "utf-8"
