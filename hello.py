#!/usr/bin/env python
# -*- coding:utf-8 -*-
from slackclient import SlackClient
from flask import Flask
import twilio.twiml
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
  token = os.environ["SLACK_API_TOKEN"]
  sc = SlackClient(token)
  sc.api_call(
    "chat.postMessage",
    channel="#random",
    text="Hello from Python! :tada:"
  )

  resp = twilio.twiml.Response()
  resp.say("Hello Monkey")

  return str(resp)


if __name__ == '__main__':
    app.run()
