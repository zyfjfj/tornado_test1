# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

__author__ = 'zyf'

DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PWD = '123456'
DB_NAME = 'tornado_db'

Base = declarative_base()  # create Base lei
engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8' %
                       (DB_USER, DB_PWD, DB_HOST, DB_NAME),
                       encoding='utf-8', echo=False,
                       pool_size=100, pool_recycle=10)
