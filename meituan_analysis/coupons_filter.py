import time
import re
from meituan_tools import Operation
from meituan_tools import del_duplicate

op = Operation()
conn = op.db_conn()
cur = conn.cursor()
sql = '''select a.poi_id,a.deal_list,a.stamp from meituan_shop_info as a
inner JOIN
(
select poi_id,max(stamp) as stp from meituan_shop_info
GROUP BY poi_id
) as b on a.poi_id = b.poi_id and a.stamp = b.stp
'''
print('please wait about 360s')
st = time.clock()
cur.execute(sql)
en = time.clock()
print('SQL takes', en - st, 'sends retrieval data')
result = cur.fetchall()
print('filter start!')
for d in result:
    poi_id = d[0]
    tp_d = re.sub('\s+', ' ', d[1].replace('’', '"').replace('\n', ''))
    try:
        deal = del_duplicate(eval(tp_d))
    except SyntaxError:
        print('line 26 eval error', d[1])
        continue

    stamp = d[2].strftime("%Y-%m-%d %H:%M:%S")
    result = op.check_data(table='meituan_coupons_info',
                           w_sub={'poi_id =': poi_id,
                                  'publish_date >=': stamp})
    if result:
        continue

    else:
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
            try:
                op.insert(table='meituan_coupons_info',
                          row=row)
            except:
                print('line 51 insert error', row)

cur.close()
conn.commit()
conn.close()
