# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("mysql://sunvins:taoyin@localhost:3306/pydb?charset=utf8", echo = False)
Base = declarative_base()

class FieldTb(Base):
    __tablename__ = 'FieldTb'
    cid = Column(Integer,primary_key=True)
    url = Column(String(128))
    tbname = Column(String(64))
    pxpath = Column(String(64))
    xpath = Column(String(64))
    fieldname = Column(String(64))
    descr = Column(String(64))

class FieldRsTb(Base):
    __tablename__ = 'FieldRsTb'
    cid = Column(Integer,primary_key=True)
    batchid = Column(Integer)
    tbname = Column(String(64))
    fieldname = Column(String(64))
    fieldvalue = Column(String(64))
    updatedttm = Column(String(64))

class Article(Base):
    __tablename__ = 'Article'
    cid = Column(Integer, primary_key=True)
    url = Column(String(120))
    proj = Column(String(120))
    title = Column(String(120))
    detail_url = Column(String(120))
    pub_date = Column(String(32))
    content = Column(String(3000))
    updatedttm = Column(String(64))

def init_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)

init_db()   #创建所有表
Session = sessionmaker(bind=engine)
session = Session()
