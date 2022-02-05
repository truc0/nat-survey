#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime

"""
CrawlerConst gives names to question id
"""
class CrawlerConst:
    NAME = 10000793
    SAMPLE_DATE = 10000799
    RESULT_DATE = 10000794
    DURATION = 9908737

    ITEM_TEMPLATE = {
        'name': '',
        'durations': []
    }
    


class Crawler:

    def __init__(self, url):
        self.url = url

    def fetch(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            return None
        data = response.json()
        return self.parse(data)
        
    def parse(self, data):
        if not data['success']:
            return None
        rows = data['data']['rows']
        total = data['data']['total']
        return dict(
            data=self.parse_rows(rows),
            total=total,
        )

    def parse_rows(self, rows):
        # data is a map from code of hospital to real data 
        data = dict()
        for row in rows:
            answers = row['answers']
            code = name = duration = None
            for answer in answers:
                id = answer['question']['id']
                if id == CrawlerConst.NAME:
                    code = answer['answer']['code']
                    name = answer['answer']['label']
                elif id == CrawlerConst.DURATION:
                    duration = answer['answer']

            if not (code and name and duration):
                print(code, name, duration)
                raise ValueError('Parse Error')

            if code in data:
                data[code]['durations'].append(duration)
            else:
                data[code] = dict(name=name, durations=[duration])
        
        return [dict(code=code, **item) for code, item in data.items()]


class CachedCrawler(Crawler):

    def __init__(self, url, cache_time=datetime.timedelta(minutes=5)):
        super(CachedCrawler, self).__init__(url)
        self.cache_time = cache_time
        self.cached_result = super(CachedCrawler, self).fetch()
        self.last_request_time = datetime.datetime.now()

    def fetch(self, force_update=False):
        now = datetime.datetime.now()
        expired = now - self.last_request_time > self.cache_time

        if expired or force_update:
            self.cached_result = super(CachedCrawler, self).fetch()
            return self.cached_result
        else:
            return self.cached_result
            

if __name__ == '__main__':
    from config import BASE_URL

    crawler = Crawler(BASE_URL)
    print(crawler.fetch())
 