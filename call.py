#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import request, url_for, Flask
from twilio.rest import TwilioRestClient
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
  return "Hello World!!!"

@app.route('/call', methods=['GET', 'POST'])
def call():
  account = os.environ["TWILIO_SID"]
  token = os.environ["TWILIO_AUTH_TOKEN"]
  f = os.environ["TWILIO_PHONE_NUMBER"]
  to = request.values.get('to', None)
  to = "+81" + to[1:-1]
  
  print app.config
  print request.remote_addr
  print request.remote_addr + url_for('call_response')
  print request
  client = TwilioRestClient(account, token)
  call = client.calls.create(
    to=to,
    from_=f,
    url=(request.url_root + url_for('call_response'))
  )
  return call.sid

@app.route('/call/response', methods=['GET', 'POST'])
def call_response():
  return app.send_static_file('call.xml')

if __name__ == '__main__':
  app.run(host='0.0.0.0')
