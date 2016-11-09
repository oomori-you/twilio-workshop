#!/usr/bin/env python
# -*- coding:utf-8 -*-
from slackclient import SlackClient
from flask import request, Flask
import twilio.twiml
import os
app = Flask(__name__)

@app.route('/')
def hello_world():
  from_number = request.values.get('From', None)
  
  token = os.environ["SLACK_API_TOKEN"]
  text = ""
  if from_number is None:
    text = "Hello anonymous :tada:"
  else:
    # Greet the caller by name
    text = "Hello {0} :tada:".format(from_number)
  sc = SlackClient(token)
  sc.api_call(
    "chat.postMessage",
    channel="#random",
    text=text
  )

  resp = twilio.twiml.Response()
  resp.say(u"日本語にほんご", language="ja-jp")

  return str(resp)


@app.route('/late/response')
def absent():
  return app.send_static_file('late-response.xml')

@app.route('/absent')
def absent():
  return app.send_static_file('absent.xml')

@app.route('/late')
def absent():
  return app.send_static_file('late.xml')

@app.route('/invalid')
def absent():
  return app.send_static_file('invalid.xml')

@app.route('/reception/response')
def reception_response():
  digits = request.values.get('Digits', None)
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
