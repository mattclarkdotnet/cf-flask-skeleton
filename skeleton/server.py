from flask import Flask, render_template
from os import getenv
import logging

app = Flask(__name__)

FLASK_DEBUG = bool(getenv('FLASK_DEBUG', False))
APP_DEBUG = bool(getenv('APP_DEBUG', False))

if APP_DEBUG:
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Set appplication log level to debug')

if FLASK_DEBUG:
    app.debug = True
    logging.debug('Set Flask app.debug to True - beware of excessive stat() volume on CF instances')


@app.route('/')
def main():
    logging.debug('Rendering main template')
    return render_template('main.html')

def testable_func(a, b):
    return a * b