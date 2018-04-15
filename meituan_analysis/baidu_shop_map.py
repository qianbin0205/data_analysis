import requests
import json
import re
from meituan_tools import Operation
from datetime import datetime

# 数据库连接
op = Operation()
conn = op.db_conn()
cur = conn.cursor()

check_sql = '''select distinct i.poi_id, substring_index(substring_index(substring_index(i.address,'（',1),'(',1),'。',1) as sub_addr 
              from meituan_shop_info as i
              left join meituan_shop_map as m on i.poi_id = m.poi_id
              where m.poi_id is null;'''

insert_sql = '''INSERT INTO meituan_shop_map(poi_id, addr, url, lng, 
                lat, confidence, precise, level, status, entrydate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
cur.execute(check_sql)

# baidu API准备
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Referer': 'http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding',
}

href = 'http://api.map.baidu.com/geocoder/v2/'
ak = 'WOHKbVZKL0Ids8XSNuuroaqnBOMPUBnS'
for i in cur.fetchall():
    print(i)
    poi_id = i[0]
    addr = ''.join(i[1].split())
    payload = {'address': addr, 'output': 'json', 'ak': ak, 'callback': 'showLocation'}
    url = href.format(addr, ak)
    response = requests.get(href, params=payload, headers=headers)
    print(response.text)
    data_reg = re.compile('({.*})\)')
    map_str = data_reg.findall(response.text)[0]
    map_json = json.loads(map_str)
    r = [poi_id, addr, url]

    if map_json['result']:
        # 经度值
        r.append(map_json['result']['location']['lng'])
        # 纬度值
        r.append(map_json['result']['location']['lat'])
        # 位置的附加信息，是否精确查找。1为精确查找，即准确打点；0为不精确，即模糊打点（模糊打点无法保证准确度，不建议使用）
        r.append(map_json['result']['precise'])
        # 可信度，描述打点准确度，大于80表示误差小于100m。该字段仅作参考，返回结果准确度主要参考precise参数
        r.append(map_json['result']['confidence'])
        # 地址类型
        r.append(map_json['result']['level'])
    else:
        r.extend([None] * 5)
        print('extract miss')
    # 返回结果状态值， 成功返回0，其他值请查看下方返回码状态表
    r.append(map_json['status'])
    r.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cur.execute(insert_sql, r)
    conn.commit()

conn.close()
op.db_close()



