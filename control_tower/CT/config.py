# -*- coding: utf-8 -*-
import os
import urllib

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# -- SESSION CONFGURATIONS -- #
# os.urandom(24)
SECRET_KEY = '\x9b\xf1x\t;\xfe\x0c\x1c?\no\xe2/\x9a\x86\x00\x7f0\x04!\xe2R\xa0\x7f'
PERMANENT_SESSION_LIFETIME = 1800
SESSION_COOKIE_NAME = 'CT'

# Banco de dados local
SQLALCHEMY_DATABASE_URI = 'sqlite:///ct.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = 'False'

# -- API RECAPCHA GOOGLE -- #
# Get key in https://www.google.com/recaptcha
RECAPTCHA_USE_SSL = True
RECAPTCHA_PUBLIC_KEY = '6LeK6hYUAAAAAJU8p2oRaEdkwaXryb2QpCNM-H2W'
RECAPTCHA_PRIVATE_KEY = '6LeK6hYUAAAAAL4lJSBZ-SIaJctFuUTjKaJpmEeQ'
RECAPTCHA_OPTIONS = {'theme': 'white'}
