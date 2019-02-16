from selenium import webdriver as wd
# 디비 모듈 (쿼리 수행)
import pymysql
import time
import math
import numpy as np
import pandas as pd


def selectSchool_list():
    result=None
    connection = None
    try:
        # DB연결
        connection = pymysql.connect(host='localhost',
                                user='root',
                                password='1234',
                                db='chocopython',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            # 쿼리문 작성 및 인자 세팅
            sql = "SELECT name FROM dormitory;"
            # 쿼리 수행
            cursor.execute(sql)
            # 결과 패치
            result = cursor.fetchall()
    except Exception as e:
        result = None
        print(e)
    else:
        print("정상 수행")
    finally:
        if connection: # 보험처리, connection이 0이면 넘어감
            connection.close()
    return result
school_list=[]
for i in range(len(selectSchool_list())):
    school_list.append(selectSchool_list()[i]['name'])

print(school_list)