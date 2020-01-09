import sys
import itertools
import pandas as pd

def spc(data,deviation):
    toatal = data.shape[0]
    defective_count = data[data[deviation] > 0.5].shape[0]
    defective= defective_count / (toatal + sys.float_info.epsilon)
    return defective

def count_confidence_columns(data,deviation,item):
    result_item = data.groupby(item)[deviation].agg(['mean', 'count', 'sum'])
    return result_item
def count_confidence_value(data):
    data.loc[data.Deviation < 0.5, 'Deviation'] = 0
    data.loc[data.Deviation >= 0.5, 'Deviation'] = 1
    confidence = data['Deviation'].sum() / data['Deviation'].count()
    return confidence
def auto_suggestion(data):
    columns = ['matDataBComponents[1].batch',
               'matDataBComponents[1].vendor', 'matDataBComponents[2].batch',
               'matDataBComponents[2].vendor', 'matDataBComponents[3].batch',
               'matDataBComponents[3].vendor', 'matDataBComponents[4].batch',
               'matDataBComponents[4].vendor', 'toolData[1].toolID',
               'toolData[12].toolID', 'toolData[2].toolID',
               'MouldMachineNo',
               'MouldNestNo', 'TablePosition', 'Moulding.toolData[1].toolID',
               'Moulding.toolData[2].toolID', 'Moulding.toolData[3].toolID',
               'Moulding.toolData[4].toolID', 'Moulding.toolData[5].toolID',
               'Moulding.toolData[6].toolID', 'Moulding.toolData[7].toolID', ]
    data.loc[data.Deviation < 0.5, 'Deviation'] = 0
    data.loc[data.Deviation >= 0.5, 'Deviation'] = 1
    for column in columns:
        data[column] = column + '__' + data[column]
    data2 = data.drop_duplicates(columns)

    def count(item):
        result_item_1 = data.groupby(item)['Deviation'].agg(['mean', 'count', 'sum'])
        result_item_2 = data2.groupby(item)['Deviation'].agg(['count', ]).rename(columns={'count': 'ccount'})
        result_item = pd.merge(result_item_1, result_item_2, left_index=True, right_index=True)
        return result_item

    result = pd.DataFrame(columns=['mean', 'sum', 'count', 'ccount'])
    for i in range(1, 4):
        result_list = list(map(count, list(itertools.combinations(columns, i))))
        result_list = pd.concat(result_list)
        result_list = result_list[(result_list['ccount'] / result_list['count'] > 0.5) & (result_list['count'] > 100)]
        result = result.append(result_list).sort_values('mean', ascending=False).head(20)
    return result