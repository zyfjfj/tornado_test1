#coding=utf-8
import os

import tornado.web
from sqlalchemy.orm import scoped_session, sessionmaker
import module
from base import BaseHandler
from db import mysql_engine, Base
from module import create_all


class MyApplication(tornado.web.Application):
    def __init__(self):
        settings = dict(
            blog_title=u"Tornado Blog",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/login",
            debug=True,
        )
        super(MyApplication, self).__init__(**settings)
        # Have one global connection to the blog DB across all handlers
        self.db = scoped_session(sessionmaker(bind=mysql_engine,
                                     autocommit=False, autoflush=True,
                                     expire_on_commit=False))
        create_all()

    def load_handler_module(self, handler_module, perfix=".*$"):
        """
        从模块加载 RequestHandler
            `handler_module` : 模块
            `perfix` : url 前缀
        """
        # 判断是否是有效的 RequestHandler (是类且是 RequestHandler 的子类)
        is_handler = lambda cls: isinstance(cls, type) \
                                 and issubclass(cls, BaseHandler)
        # 判断是否拥有 url 规则
        has_pattern = lambda cls: hasattr(cls, 'url_pattern') \
                                  and cls.url_pattern
        handlers = []
        # 迭代模块成员
        for i in dir(handler_module):
            cls = getattr(handler_module, i)
            if is_handler(cls) and has_pattern(cls):
                handlers.append((cls.url_pattern, cls))
        self.add_handlers(perfix, handlers)

    def _get_host_handlers(self, request):
        """
        覆盖父类方法, 一次获取所有可匹配的结果. 父类中该方法一次匹配成功就返回, 忽略后续
        匹配结果. 现通过使用生成器, 如果一次匹配的结果不能使用可以继续匹配.
        """
        host = request.host.lower().split(':')[0]
        # 使用生成器表达式而非列表推导式, 减少性能折扣
        handlers = (i for p, h in self.handlers for i in h if p.match(host))
        # Look for default host if not behind load balancer (for debugging)
        if not handlers and "X-Real-Ip" not in request.headers:
            handlers = [i for p, h in self.handlers for i in h if p.match(self.default_host)]
        return handlers
    #
    def create_all(self):
        Base.metadata.create_all(mysql_engine)