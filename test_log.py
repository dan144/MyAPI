#!/usr/bin/env python3.4

import requests
import time

page = input('Page? ')
url = 'http://localhost:5000/log'
r = requests.post(url, json={'date':time.gmtime(), 'page':page})
print(r)
