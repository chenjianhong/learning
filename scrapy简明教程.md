#scrapy 0.24 简明教程#

##新建工程##
```
scrapy startproject <project-name>
```
目录结构如下：
```
│  scrapy.cfg
└─demo
    │  items.py
    │  pipelines.py
    │  settings.py
    │  __init__.py
    │
    └─spiders
            __init__.py
```

##添加item##

```
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field 

class DemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

    

class DmozItem(Item):
    title = Field()
    link = Field()
    desc = Field()
```

##添加爬虫##
```
from scrapy.spider import BaseSpider
from demo.items import DmozItem

class DmozSpider(BaseSpider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            item = DmozItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item
```

