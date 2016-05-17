#coding=utf-8

import time

import tornado
from tornado import gen
import json
import base
from base import BaseHandler

__author__ = 'zyf'
@base.route('/sleep')
class SleepHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 5)
        self.write("when i sleep 5s")
@base.route('/justnow')
class JustNowHandler(BaseHandler):
    def get(self):
        self.write("i hope just now see you")
@base.route('/get_json')
class GetJson(BaseHandler):
    def get(self):
        info = {'user': 'leno'}
        return  self.write(json.dumps(info))