#!/usr/bin/env python
# -*- coding:utf-8 -*-
from slackclient import SlackClient
from flask import request, url_for, redirect, Flask
import twilio.twiml
import os
import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
  return "Hello World!!!"

@app.route('/late/response')
def late_response():
  text = ""
  from_number = request.values.get('From', None)
  digits = (str)(request.values.get('Digits', None))
  t = datetime.datetime.strptime(2359, '%H%M')
  if from_number is None:
    text += u"{0} さんは本日遅刻です。".format("anonymous")
    text += u"出社予定時刻は {0}:{1} です。\n".format(t.hour, t.minute)
  else:
    text += u"{0} さんは本日遅刻です。\n".format(from_number)
    text += u"出社予定時刻は {0}:{1} です。\n".format(t.hour, t.minute)
  
  token = os.environ["SLACK_API_TOKEN"]
  sc = SlackClient(token)
  sc.api_call(
    "chat.postMessage",
    channel="#random",
    text=text
  )
  return app.send_static_file('late-response.xml')

@app.route('/absent')
def absent():
  text = ""
  from_number = request.values.get('From', None)
  if from_number is None:
    text = u"{0} さんは本日欠勤です。".format("anonymous")
  else:
    text = u"{0} さんは本日欠勤です。".format(from_number)
  
  token = os.environ["SLACK_API_TOKEN"]
  sc = SlackClient(token)
  sc.api_call(
    "chat.postMessage",
    channel="#random",
    text=text
  )
  return app.send_static_file('absent.xml')

@app.route('/late')
def late():
  return app.send_static_file('late.xml')

@app.route('/invalid')
def invalid():
  return app.send_static_file('invalid.xml')

@app.route('/reception/response')
def reception_response():
  digits = (int)(request.values.get('Digits', None))
  if digits == 1:
    return redirect(url_for('absent'))
  elif digits == 2:
    return redirect(url_for('late'))
  else:
    return redirect(url_for('invalid'))
  
@app.route('/reception')
def reception():
  return app.send_static_file('reception.xml')

if __name__ == '__main__':
    app.run()
