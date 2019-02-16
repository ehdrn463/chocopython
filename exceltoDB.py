from selenium import webdriver as wd
# 디비 모듈 (쿼리 수행)
import pymysql
import time
import math
import numpy as np
import pandas as pd

def toDB(dormi):
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
            sql = "INSERT INTO dormitory (name, student, room, accept, dormi2, tuition) VALUES (%s);" %str(list(dormi.loc[ name ]))[1:-1]
            # 쿼리 수행
            cursor.execute(sql)
        connection.commit()
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


dormi= pd.read_excel('./data/2017.xls', encoding='utf-8')
for name in dormi.index:
    toDB(dormi)
    # sql = "INSERT INTO dormitory (name, student, room, accept, dormi2, tuition) VALUES (%s);" %str(list(dormi.loc[ name ]))[1:-1]
    # print(sql)


"""
CREATE TABLE `dormitory` (
	`name` VARCHAR(50) NOT NULL,
	`student` INT(11) NOT NULL,
	`room` INT(11) NOT NULL,
	`accept` INT(11) NOT NULL,
	`dormi2` INT(11) NOT NULL,
	`tuition` FLOAT NOT NULL,
	PRIMARY KEY (`name`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;
"""


    
