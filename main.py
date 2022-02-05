#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import APP_NAME, BASE_URL
from app import create_app
from crawler import CachedCrawler

app = create_app(APP_NAME)
crawler = CachedCrawler(BASE_URL)

@app.route('/api/')
def index():
    return crawler.fetch()
