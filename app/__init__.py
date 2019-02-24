from flask import Flask
from config import Config
import os, requests
proxyDict = {
              "http"  : os.environ.get('FIXIE_URL', ''),
              "https" : os.environ.get('FIXIE_URL', '')
            }
r = requests.get('http://www.sabreii.com', proxies=proxyDict)

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
