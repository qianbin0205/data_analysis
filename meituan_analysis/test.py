import time
from meituan_tools import Operation
import json
import re
from collections import Counter
from functools import reduce


def del_duplicate(li):
    temp_list = list(set([str(i) for i in li]))
    li = [eval(i) for i in temp_list]
    return li


op = Operation()
conn = op.db_conn()
cur = conn.cursor()
d = '''[[(’price’, 88), (’soldCounts’, 0), (’title’, ’SCHNITZEL ‘VIENNA STYLE‘ WITH POTATO SALAD 猪排无限量供应配土豆沙拉1份’)], [(’price’, 198), (’soldCounts’, 0), (’title’, ’周一烤猪肘套餐，建议单人使用’)], [(’price’, 58), (’soldCounts’, 1), (’title’, ’商务午市套餐1份’)], [(’price’, 528), (’soldCounts’, 0), (’title’, ’超值四人套餐，提供免费WiFi’)], [(’price’, 898), (’soldCounts’, 0), (’title’, ’超值六人套餐，提供免费WiFi’)]]
'''
tp_d = re.sub('\s+', ' ', d.replace('’', '"').replace('\n', ''))
deal = del_duplicate(eval(tp_d))
for i in deal:
    poi_id = 158806754
    price = i[0][1]
    sold_coounts = i[1][1]
    title = i[2][1]
    stamp = '2018-04-05 17:55:48'

    sql = '''DELETE FROM meituan_coupons_info 
              where poi_id = {}'''.format(poi_id)
    cur.execute(sql)
    conn.commit()

    for e, i in enumerate(deal):
        price = i[0][1]
        sold_coounts = i[1][1]
        title = i[2][1]
        coup_id = e + 1

        row = [poi_id, coup_id, title, price, sold_coounts, stamp]
        op.insert(table='meituan_coupons_info',
                  row=row)

        conn.commit()
