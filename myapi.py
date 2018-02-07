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
		timestamp = time.strftime('%Y-%m-%d %H:%M:%S', new_data['date'])
		data[timestamp] = new_data['page']
		with open(datafile, 'w') as f:
			json.dump(data, f)
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
	data = get_data()
	if data == {}:
		return render_template('report.html')
	return render_template('report.html', data=data)
