#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS

from config import APP_NAME
from config import ALLOWED_ORIGINS
from config import CACHED_TIME
from crawler import Crawler, CachedCrawler

def create_app(name):
    app = Flask(name)
    CORS(app, origins=ALLOWED_ORIGINS)
    return app

def create_cached_crawler(BASE_URL):
    return CachedCrawler(BASE_URL, CACHED_TIME)

if __name__ == '__main__':
    app = create_app(APP_NAME)