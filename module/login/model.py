# coding=utf-8
from sqlalchemy.ext.declarative import declarative_base

from db import mysql_engine, Base

__author__ = 'zyf'
from sqlalchemy import Column, String, Integer, VARCHAR


class Article(Base):
    __tablename__ = 'articles'
    user = Column(VARCHAR(20), primary_key=True)
    title = Column(VARCHAR(40))
    time = Column(VARCHAR(20))
    content = Column(VARCHAR(2000))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(75), nullable=False)
    password = Column(String(128), nullable=False)

    def __repr__(self):
        return "<User('%s'):pw('%s')>" % (self.username, self.password)


Models = {'articles': Article, 'users': User}


def get_model(name):
    return Models[name]
