#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import APP_NAME, BASE_URL
from app import create_app
from crawler import Crawler

app = create_app(APP_NAME)

@app.route('/api/')
def index():
    crawler = Crawler(BASE_URL)
    return crawler.fetch()
