# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~

    :copyright: (c) 2012 by GrexIt.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.py')
