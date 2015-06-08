# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
import time
import MySQLdb
import MySQLdb.cursors

class DemoPipeline(object):
    def process_item(self, item, spider):
        return item

        
class MySQLStorePipeline(object):
    """docstring for MySQLstor"""
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = '127.0.0.1',
            db = 'demo',
            user = 'root',
            passwd = 'root',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
        )
        
    def process_item(self, items, spider):
        print spider
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, items)
        query.addErrback(self.handle_error)
        return items
        
    def _conditional_insert(self, tx, item):
        '''
        CREATE TABLE book(\
            title varchar(50),\
            link varchar(50),\
            description varchar(50)\
        );
        '''
        tx.execute(
            "insert into book (title, link, description)\
            values ('%s', '%s', '%s')"%
            (item['title'][0],
            item['link'][0],
            item['desc'][0]
            )
        )
 
    def handle_error(self, e):
        log.err(e)