#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS

from config import APP_NAME
from config import ALLOWED_ORIGINS

def create_app(name):
    app = Flask(name)
    CORS(app, origins=ALLOWED_ORIGINS)
    return app

if __name__ == '__main__':
    app = create_app(APP_NAME)