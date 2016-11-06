#!/usr/bin/env python
# -*- coding:utf-8 -*-
import web

urls = (
  '/(.*)', 'hello'
)

app = web.application(urls, globals()).wsgifunc() # <- .wsgifunc() を追加！

class hello:
  def GET(self, name):
    if not name:
      name = 'World'
    return 'Hello, ' + name + '!'

if __name__ == '__main__':
    app.run()
