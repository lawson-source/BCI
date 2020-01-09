from sqlalchemy import create_engine
import pandas as pd
class load_data:
    def __init__(self,start_date='2019-03-01',end_date='2019-09-31'):
        self.start_date=start_date
        self.end_date=end_date
    def load_data(self):
        columns = [
           'Deviation', 'matDataBComponents[1].vendor', 'matDataBComponents[2].vendor', 'matDataBComponents[3].vendor',
            'matDataBComponents[4].vendor', 'toolData[1].toolID', 'toolData[12].toolID', 'toolData[2].toolID',
            'MouldMachineNo', 'MouldNestNo', 'TablePosition', 'Moulding.toolData[1].toolID',
            'Moulding.toolData[2].toolID',
            'Moulding.toolData[3].toolID', 'Moulding.toolData[4].toolID', 'Moulding.toolData[5].toolID',
            'Moulding.toolData[6].toolID', 'Moulding.toolData[7].toolID', 'Ident No.','X','Y','Production Date'
        ]
        # load data from MySQL
        sql = 'SELECT * FROM dataunique WHERE `Production Date`>\'%s\' AND `Production Date`<\'%s\''%(self.start_date,self.end_date)
        engine = create_engine("mysql+pymysql://root:yuan20112@localhost/wujin?charset=UTF8MB4")
        data = pd.read_sql(sql, engine)
        data = data[columns].dropna()
        return data

def main():
    ld=load_data().load_data()
    return ld

if __name__ == '__main__':
    main()
