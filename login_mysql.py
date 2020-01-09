import pymysql
import pandas as pd
def main(sql):
       conn = pymysql.connect(host='localhost',
                       user='root',password='yuan20112',
                       database='wujin',
                        charset='utf8')
       cur = conn.cursor()
       cur.execute(sql)
       result = cur.fetchall()  # 获取查询结果
       col_result = cur.description  # 获取查询结果的字段描述

       columns = []
       for i in range(len(col_result)):
           columns.append(col_result[i][0])  # 获取字段名，咦列表形式保存

       df = pd.DataFrame(columns=columns)
       for i in range(len(result)):
           df.loc[i] = list(result[i])  # 按行插入查询到的数据

       conn.close()
       return df

