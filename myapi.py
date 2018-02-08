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

def chronological_slot(timestamp, page, history):
	if len(history) == 0:
		return 0
	if timestamp < history[0][0] and page < history[0][1]:
		return 0
	elif timestamp > history[-1][0] and page > history[-1][1]:
		return len(history)

	for i in range(len(history) - 1):
		if timestamp in range(history[i][0] + 1, history[i + 1][0]) and page in range(history[i][1] + 1, history[i + 1][1]):
			return i+1
	return -1

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
		slot = chronological_slot(timestamp, page, data[book])
		if slot == -1:
			return False
		data[book].insert(slot, [timestamp, page])

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

@app.route("/csv")
def csv():
	raw_text = ''
	for book, page_history in get_data().items():
		raw_text += book + ','
		for entry in page_history:
			raw_text += str(entry[1]) + ','
		raw_text += '<br/>'
	return raw_text
