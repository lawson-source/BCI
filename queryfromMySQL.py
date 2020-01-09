import  pymysql
from sqlalchemy import create_engine
import pandas as pd
engine=create_engine("mysql+pymysql://root:yuan20112@localhost/wujin?charset=UTF8MB4")
data=pd.read_sql_table('data',engine)
print(data.head(5))