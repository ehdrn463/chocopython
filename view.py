import pymysql as sql
import pandas as pd
from sqlalchemy import create_engine
import pandas.io.sql as pSql
import numpy as np
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import platform
import seaborn as sns

# 한글폰트 처리
plt.rcParams['axes.unicode_minus']=False
if platform.system() == 'Windows': #윈도우
    path = 'C:\Windows\Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc( 'font', family=font_name )

elif platform.system() == 'Darwin': #맥
    rc( 'font', family='AppleGothic' )

else:
    print('지원불가')

engine = create_engine("mysql+pymysql://root:1234@127.0.0.1:3306/chocopython", encoding='utf8')
conn   = engine.connect()

dormi = pSql.read_sql("SELECT * FROM dormitory", conn)
room = pSql.read_sql("SELECT * FROM room_price", conn)
# name 기준으로 제정렬 평균
room_name= pd.pivot_table( room, index='name', aggfunc=np.mean)
# 테이블 합치기
dormi['room_total']=list(room_name['total'])

# 기숙사비, 등록금
sns.set_style('darkgrid')
sns.lmplot(x = 'dormi2', y = 'tuition',  data = dormi, height =7, palette='Set2')
plt.show()

# 기숙사비, 방값
sns.set_style('darkgrid')
sns.lmplot(x = 'dormi2', y = 'room_total',  data = dormi, height =7, palette='Set2')
plt.show()

# 기숙사비, 학생수
sns.set_style('darkgrid')
sns.lmplot(x = 'dormi2', y = 'student',  data = dormi, height =7, palette='Set2')
plt.show()