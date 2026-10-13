京东商品信息爬取系统
技术栈： Python、Scrapy 2.13、XPath/CSS 选择器、JSON 接口逆向、浏览器抓包（DevTools）

项目描述：
针对京东商城商品数据采集需求，基于 Scrapy 框架开发可配置关键词、支持多页翻页的爬虫系统，自动化抓取商品标题、店铺名称、价格、详情页链接等字段，并结构化存储为 JSON 文件，为后续数据分析与选品提供数据支撑。

主要工作：

分析url：分析https://re.jd.com/search爬取相对简单不需要h5st签名参数就可以爬取数据并且只要一次搜索抓包得到adInfo，pageUuid字段就可以一直复用请求，爬取数据

搭建 Scrapy 工程：规范划分 Spider / Item / Pipeline / Settings 模块，自定义 JsonPipeline 将采集结果以 UTF-8 编码、缩进格式化写入 output/<关键词>.json，支持按关键词分文件存储。

逆向京东数据接口：通过浏览器 DevTools 抓包定位到京东热卖分页 JSON 接口 re.jd.com/pcSearch/pageing，直接请求该接口获取结构化 JSON 数据，绕过前端渲染。

数据清洗与过滤：接口返回结果中混入"猜你喜欢"推荐流商品（与搜索词无关）。通过分析 moduleInfo 各模块结构，区分主搜索结果模块（goods-pc-filter-upgrade）与推荐流模块（goods-pc-search），仅保留主结果，有效过滤无关商品。

翻页与参数化：爬虫支持命令行传入 -a keyword=关键词 -a pages=页数 动态指定搜索词与爬取页数，逐页构造 page 参数请求分页接口，单页约 48 条数据。


项目运行   python -m scrapy crawl jd_search -a keyword=搜索商品 -a pages=页面数
