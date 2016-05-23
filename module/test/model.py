from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR

from db import Base, mysql_engine


class Test_one(Base):
    __tablename__ = 'test_one'
    test = Column(VARCHAR(20),primary_key = True)
    title = Column(VARCHAR(40))

class Test_two(Base):
    __tablename__='test_two'
    test=Column(VARCHAR(20),primary_key = True)