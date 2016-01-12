#coding:utf-8

import os
import sys
import time
import MySQLdb

DB_IP = '10.66.116.11'
DB_USER = 'root'
DB_PWD = 'renlong123'
DB_NAME = 'movie_new'

def connect_db():
    db_conn = None
    try:
        db_conn = MySQLdb.connect(DB_IP, DB_USER, DB_PWD, DB_NAME, charset='utf8')
    except Exception, ex:
        return None
    assert db_conn
    curs = db_conn.cursor()
    return curs, db_conn

def select_sql(sql):
    cursor, conn = connect_db()
    if not cursor:
        print '连接数据库失败'
        return -1
    try:
        cursor.execute(sql)
    except Exception, e:
        print '%s' % str(e)
        return -1
    tuple_data = cursor.fetchall()
    return tuple_data

def AddDetail(movie_info):
    cursor, conn = connect_db()
    if not cursor:
        print '连接数据库失败'
        return -1
    selectsql = u'select * from detail where title="%s"' % (movie_info['title'])
    try:
        cursor.execute(selectsql)
    except Exception , e:
        print '%s' % str(e)
        return -1
    tuple_data = cursor.fetchall()
    if len(tuple_data) != 0:
        return 0
    #插入
    insertsql = u'''insert into detail(title, totle_title, directors, bianjus, actors, type, country, language, uptime, timelen, altername, doubanscore, summary, piclist, baiduyunlink, baiduyunpwd, magnetlist, titlepic, qingxi) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")''' % (movie_info['title'],movie_info['totle_title'],movie_info['directors'],movie_info['bianjus'],movie_info['actors'],movie_info['type'], movie_info['country'], movie_info['language'],movie_info['uptime'],movie_info['movietime'], movie_info['altername'], movie_info['doubanscore'],movie_info['summary'],movie_info['piclist'], movie_info['baiduyunlink'], movie_info['baiduyunpwd'], movie_info['magnetlist'], movie_info['titlepic'], movie_info['qingxi'])
    #print (u"sql is : %s" % insertsql)
    try:
        cursor.execute(insertsql)
    except Exception, e:
        print 'insert error. %s' % str(e)
        return -1
    conn.commit()
    return 0
def AddOneName(tablename, name):
    cursor, conn = connect_db()
    if not cursor:
        print '连接数据库失败'
        return -1
    selectsql = u'select * from %s where name="%s"' % (tablename, name)
    try:
        cursor.execute(selectsql)
    except Exception, e:
        print '%s' % str(e)
        return False
    tuple_data = cursor.fetchall()
    if not tuple_data:
        return False
    if len(tuple_data) != 0:
        return True

    #insert
    insertsql = '''insert into %s(name) values(%s)''' % (tablename, name)
    try:
        cursor.execute(insertsql)
    except Exception, e:
        print 'insert error. %s' % str(e)
        return False
    conn.commit()
    return True

def AddDirector(directorname):
    return AddOneName(director,directorname)

def AddBianju(bianjuname):
    return AddOneName(bianju, bianjuname)

def AddActor(actorname):
    return AddOneName(actor, actorname)

def AddType(typename):
    return AddOneName(types, typename)

def AddCountry(countryname):
    return AddOneName(country, countryname)
