#!/usr/bin/env python
# -*- coding:utf-8 -*-
from slackclient import SlackClient
from flask import request, url_for, redirect, Flask
import os
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
  return "Hello World!!!"

@app.route('/reception/ask', methods=['GET', 'POST'])
def reception():
  return app.send_static_file('reception-ask.xml')

@app.route('/reception/answer', methods=['GET', 'POST'])
def reception_response():
  digits = (int)(request.values.get('Digits', None))
  if digits == 1:
    return redirect(url_for('absent'))
  elif digits == 2:
    return redirect(url_for('late/ask'))
  else:
    return redirect(url_for('invalid'))

@app.route('/absent', methods=['GET', 'POST'])
def absent():
  from_number = request.values.get('From', None)
  text = u"`{0}` さんは本日欠勤です。".format(number_to_name(from_number))
  tweet(text);
  return app.send_static_file('absent.xml')

@app.route('/late/ask', methods=['GET', 'POST'])
def late():
  return app.send_static_file('late-ask.xml')

@app.route('/late/answer', methods=['GET', 'POST'])
def late_response():
  from_number = request.values.get('From', None)
  digits = (str)(request.values.get('Digits', None))
  t = datetime.datetime.strptime(digits, '%H%M')
  text = u"`{0}` さんは本日遅刻です。".format(number_to_name(from_number))
  text += u"出社予定時刻は `{0}:{1}` です。\n".format(t.hour, t.minute)
  tweet(text);
  return app.send_static_file('late-answer.xml')

@app.route('/invalid', methods=['GET', 'POST'])
def invalid():
  return app.send_static_file('invalid.xml')

'''
e.g.
  from_number = request.values.get('From', None)
  text = u"`{0}` さんは~~です。".format(number_to_name(from_number))
  tweet(text);
'''
def tweet(text):
  token = os.environ["SLACK_API_TOKEN"]
  sc = SlackClient(token)
  sc.api_call(
    "chat.postMessage",
    channel="#random",
    text=text
  )
def number_to_name(number):
  dic = {
    u"+819029551295": u"大森 雄佑"
  }
  return dic.get(number, 'anonymous')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
