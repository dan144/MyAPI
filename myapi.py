#!/usr/bin/python3.4

import json
import requests
import time

from flask import Flask, render_template, request, make_response

datafile = '/opt/MyAPI/pagehistory.json'
app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

def add_data(new_data):
	data = get_data()
	try:
		# parse new_data
		book = new_data['book']
		page = new_data['page']
		timestamp = int(time.strftime('%s', new_data['date']))

		# add new data to book's entry
		if not data.get(book):
			data[book] = []
		if len(data[book]) == 0 or page > data[book][-1][1]:
			data[book].append([timestamp, page])
		else:
			return False

		with open(datafile, 'w') as f:
			json.dump(data, f, sort_keys=True)
	except ValueError:
		return False
	return True

def get_data():
	data = {}
	try:
		with open(datafile, 'r') as f:
			data = json.load(f)
	except (ValueError, IOError):
		with open(datafile, 'w') as f:
			json.dump(data, f)
	return data

@app.route("/log", methods=["POST"])
def log():
	new_data = request.get_json()
	success = False
	if new_data:
		success = add_data(new_data)
	return make_response("", 200 if success else 400)

@app.route("/report")
def report():
	page_list = []
	for book, page_history in get_data().items():
		for entry in page_history:
			timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[0]))
			page_list.append((book, timestamp, entry[1]))

	if len(page_list) == 0:
		return render_template('report.html')
	return render_template('report.html', data=page_list)
