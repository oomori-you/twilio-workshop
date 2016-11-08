#!/usr/bin/env python
# -*- coding:utf-8 -*-
from slackclient import SlackClient
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
  token = os.environ["SLACK_API_KEY"]
  sc = SlackClient(token)
  sc.api_call(
    "chat.postMessage",
    channel="#random",
    text="Hello from Python! :tada:"
  )
  return 'Hello World!!!'



if __name__ == '__main__':
    app.run()
