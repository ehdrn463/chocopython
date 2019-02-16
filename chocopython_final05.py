from selenium import webdriver as wd
import pymysql
import time 


def toDB(room):
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
            sql = "INSERT INTO room_price (name, guarantee, month, total) VALUES (%s);"%str(roominfo)[1:-1]
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


try:
    # 타겟 사이트
    site_url = 'https://www.dabangapp.com/search#/map?id=&type=search&filters=%7B%22deposit-range%22%3A%5B0%2C999999%5D%2C%22price-range%22%3A%5B0%2C999999%5D%2C%22room-type%22%3A%5B0%2C1%2C2%2C3%2C4%2C5%5D%2C%22deal-type%22%3A%5B0%2C1%5D%2C%22location%22%3A%5B%5B126.62013471679688%2C37.38581769625844%5D%2C%5B127.35896528320313%2C37.74395186654787%5D%5D%7D&position=%7B%22center%22%3A%5B126.98955000000001%2C37.5651%5D%2C%22zoom%22%3A11%7D&cluster=%7B%22name%22%3A%22%22%7D'
    school_list=[]
    for i in range(len(selectSchool_list())):
        school_list.append(selectSchool_list()[i]['name'])
    print(school_list)
    # 브라우저 띠우기
    driver = wd.Chrome(executable_path='./chromedriver.exe')
    driver.get(site_url)
    ######## 검색하는곳 저기 서울특별시 송파구 가락동을 나중에 %s 로 만든후 나중에 데이터베이스에서 읽어오게 해서 자동검색
    for i in school_list:
        driver.find_element_by_class_name('SearchForm-input').send_keys(i)
        time.sleep(3)
        driver.find_element_by_class_name('SearchForm-btn').click()
        ######### 검색 후 이동############
        #driver.find_element_by_id('frmNIDLogin').submit()
        #
        time.sleep(3)
        print(driver.find_element_by_css_selector('.icon-text span').text)
        print(i)
        goods=driver.find_elements_by_css_selector('.Room-list>li')
        
        roominfo_list=[]
      
        print(driver.find_element_by_css_selector('.icon-text span').text)
        
        for good in goods:
            try:
                Room_price=good.find_element_by_css_selector('span.RoomItem-price__type').text
                Room_summary=good.find_element_by_css_selector('span.RoomItem-summary').text
                if Room_price == '월세' and '원룸' in Room_summary:
                    price_na=good.find_element_by_css_selector('span.RoomsItem-price__title').text
                    price_one=price_na.split('/')
                    roominfo=[i,int(price_one[0])*10,int(price_one[1])*10,int(price_one[0])/10 + int(price_one[1])*10]
                    print(roominfo)
                    toDB(roominfo)
                else:
                    pass
            except Exception as e:
                print('에러 발생',e) 
    print(roominfo_list,len(roominfo_list))
    driver.quit()
    driver.close()

    import sys
    sys.exit()

    print("성공")
except Exception as e:
    print("오류 발생 시발",e)



"""
CREATE TABLE `room` (
	`num` INT(11) NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(128) NOT NULL,
	`guarantee` INT(11) NOT NULL,
	`month` INT(11) NOT NULL,
  `total` INT(11) NOT NULL,
	PRIMARY KEY (`num`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;
"""

