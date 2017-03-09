#coding=utf-8

import base
from app import MyApplication
from base import BaseHandler

__author__ = 'zyf'
import tornado.ioloop
import tornado.web
import tornado.options
import os.path,module

#一个带装饰器的tornado实例，handle放在module里

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application=MyApplication()
    application.listen(5555)
    for dir_handle in base.find_handles():
        application.load_handler_module(dir_handle)

    tornado.ioloop.IOLoop.instance().start()
