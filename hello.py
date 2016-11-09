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

@app.route('/reception')
def root():
  return app.send_static_file('reception.xml')

if __name__ == '__main__':
    app.run()
