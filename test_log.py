#!/usr/bin/env python3.4

import requests
import time

time_format = '%Y-%m-%d %H:%M:%S'

book = input('Book? ')
page = input('Page? ')
date = input('Date (format {})? '.format(time_format))
if date == '':
	date = time.gmtime()
else:
	date = time.strptime(date, time_format)

url = 'http://localhost:5000/log'
r = requests.post(url, json={'book': book, 'date': date, 'page': int(page)})
print(r)
if r.status_code not in (200, 400):
	print(r.content)
