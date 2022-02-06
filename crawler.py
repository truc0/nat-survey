#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import json

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

    def __init__(self, url, page_size=100):
        self.url = url
        self.page_size = page_size

    def fetch(self):
        response = requests.get(self.url, params={})
        if response.status_code != 200:
            return None
        data = response.json()
        total = data['data']['total']

        result = dict()
        page_index_max = 1 + (total - 1) // self.page_size
        
        for page_index in range(1, page_index_max + 1):
            per_page_result = self.fetch_per_page(page_index)
            result = self.merge_results(result, per_page_result)

        return self.construct_result(raw_data=result, total=total)

    def fetch_per_page(self, page_index):
        params = {
            'current': page_index,
            'pageSize': self.page_size,
        }
        response = requests.get(self.url, params={
            'params': json.dumps(params)
        })
        if response.status_code != 200:
            raise ValueError(f'Error fetching page {page_index}')
        return self.parse(response.json())
        
    def parse(self, data):
        if not data['success']:
            return None
        rows = data['data']['rows']
        return self.parse_rows(rows)

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
        
        return data

    """
    serialize_data transfer `data` from a code-value mapping to a list
    by add code as a property to the value.
    """
    @classmethod
    def serialize_data(cls, data):
        return [dict(code=code, **value) for code, value in data.items()]

    def construct_result(self, raw_data, total):
        return dict(total=total, data=self.serialize_data(raw_data))

    """
    merge_results merges two parsed row, sum up the value of same code
    and add other fields
    """
    @classmethod
    def merge_results(_, one, another):
        result = one.copy()
        another = another.copy()
        for key in another.keys():
            if key in result:
                result[key]['durations'].extend(another[key]['durations'])
            else:
                result[key] = another[key]
        return result


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
            self.last_request_time = datetime.datetime.now()
            return dict(last_update=self.last_request_time, **self.cached_result)
        else:
            return dict(last_update=self.last_request_time, **self.cached_result)
            

if __name__ == '__main__':
    from config import BASE_URL

    crawler = Crawler(BASE_URL)
    print(crawler.fetch())
 