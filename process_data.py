# -*- coding: utf-8 -*-


import apriori
import pandas as pd
import numpy as np
import pyfpgrowth as pyfg


# Apriori
def Apriori(data,minS=0.2,minC=0.05):
    order_records =np.array(data).tolist() # tranform Dataframe to list
    L, suppData = apriori.apriori(order_records, minSupport=minS)  # find frequent itemsets
    rules = apriori.generateRules(order_records, L, suppData, minConf=minC) #calculate the minimum support rule
    rules=pd.DataFrame(rules, columns=['item1', 'item2', 'instance', 'support', 'confidence',
                                             'lift'])# export result to DataFrame
    return rules
def Fp_growth(data,minS=0.2,minC=0.05):
    order_records = np.array(data).tolist()
    suppData = pyfg.find_frequent_patterns(order_records, support_threshold=minS*len(order_records))
    rules = pyfg.generate_association_rules(suppData, confidence_threshold=minC)

    rules = pd.DataFrame.from_dict(rules, orient='index', columns=['itemX','itemY','support','confidence','lift'])
    rules = rules.sort_values('confidence', ascending=False)
    return rules















