#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask

from config import APP_NAME

def create_app(name):
    app = Flask(name)
    return app

if __name__ == '__main__':
    app = create_app(APP_NAME)