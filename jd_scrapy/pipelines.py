
import json
import os


class JsonPipeline:
    """将爬取结果保存为 JSON 数组文件的管道"""

    def __init__(self):
        self.file = None        # 输出文件句柄
        self.first = True       # 是否为第一条数据（用于控制逗号分隔）
        self.count = 0          # 已保存条数计数

    @classmethod
    def from_crawler(cls, crawler):
        """Scrapy 实例化 Pipeline 的入口，这里无需 crawler 配置，直接返回实例"""
        return cls()

    def open_spider(self, spider):
        """爬虫启动：根据关键词命名文件，创建 output 目录，写入 JSON 数组开头 '['"""
        keyword = getattr(spider, "keyword", "jd")
        # 过滤非法文件名字符，保留字母数字和 _-
        safe = "".join(c for c in keyword if c.isalnum() or c in "_-") or "jd"
        out_dir = os.path.join(os.getcwd(), "output")  # 输出到当前工作目录下的 output/
        os.makedirs(out_dir, exist_ok=True)
        self.filename = os.path.join(out_dir, "%s.json" % safe)
        self.file = open(self.filename, "w", encoding="utf-8")
        self.file.write("[\n")  # JSON 数组起始
        spider.logger.info("JSON 输出文件: %s", self.filename)

    def process_item(self, item, spider):
        """每条数据的写入逻辑：非首条前补逗号，再写入格式化的 JSON 对象"""
        if not self.first:
            self.file.write(",\n")  # 与上一条之间用逗号分隔
        self.first = False
        # ensure_ascii=False 保留中文，indent=2 美化缩进
        line = json.dumps(dict(item), ensure_ascii=False, indent=2)
        self.file.write(line)
        self.count += 1
        return item  # 必须返回 item，供后续 pipeline 使用

    def close_spider(self, spider):
        """爬虫结束：写入 JSON 数组结尾 ']'，关闭文件并打印统计"""
        self.file.write("\n]\n")
        self.file.close()
        spider.logger.info("共保存 %d 条数据到 %s", self.count, self.filename)
