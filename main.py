#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request

from config import APP_NAME, BASE_URL
from app import create_app, create_cached_crawler

app = create_app(APP_NAME)
crawler = create_cached_crawler(BASE_URL)

@app.route('/api/')
def index():
    force_update = request.args.get('force_update', False)
    force_update = force_update in ('True', 'true', True)
    return crawler.fetch(force_update=force_update)
