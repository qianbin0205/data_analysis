import json
from meituan_tools import Operation

# 数据库连接
op = Operation()
conn = op.db_conn()
cur = conn.cursor()

sql = '''select round(lng,4),round(lat,4),count(*) * 10 from meituan_shop_map as m
        inner join meituan_shop_info as i on i.poi_id = m.poi_id
        where i.sub_id = 20059
        group by round(lng,4),round(lat,4);'''

cur.execute(sql)
result = cur.fetchall()
hotmap = [{"lng": float(i[0]), "lat": float(i[1]), "count": int(i[2])} for i in result]

conn.close()
op.db_close()
print(hotmap)
# with open('hotmap.txt', 'w', encoding='utf-8') as f:
#     f.write(str(hotmap))
#     f.close()
