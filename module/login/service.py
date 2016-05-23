#coding=utf-8

import time
import tornado
from sqlalchemy.orm import sessionmaker

import base
from base import BaseHandler
from db import mysql_engine
from module.login.model import User,Article
from tornado import gen

__author__ = 'zyf'

@base.route("/")
class MainHandler(BaseHandler):
    def get(self):
        id=self.get_secure_cookie("glxt_user")
        data = self.db.query(Article).all()
        if data:
            self.write(data[0])
        else:
            self.write("没有数据")

@base.route("/login")
class LoginHandler(BaseHandler):

    def add_user(self):
        user=User(username='333333',first_name='a',last_name='b',email='zyf@1.com',password='111111')
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        session.add(user)
        session.commit()
    def get(self):
        self.render("login.html", error=None)
    @gen.coroutine
    def post(self):
        #self.add_user()
        user=self.get_argument("user")
        pw=self.get_argument("password")

        data =  self.db.query(User).filter(User.username==user).first()
        if data:
            self.set_secure_cookie("glxt_user", str(data.id))
            self.render("login.html",error=None)
        else:
            self.render("login.html", error=user+" "+pw+"  ")
