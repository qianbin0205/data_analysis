import requests
import re
import time
import json
from hashlib import md5
from meituan_tools import Operation
from meituan_tools import ua_random

result = Operation().check_data(table='meituan_error_link',
                                col='url',
                                w_sub={'status': 1})
for u in result:

    url = u[0]
    sub_id = re.findall('areaId=(\d+?)&', url)[0]
    pg = int(re.findall('page=(\d+?)&', url)[0])

    Operation().update(table='meituan_error_link',
                       row=url)
    response = requests.get(url, headers=ua_random(), timeout=10)
    response.close()
    time.sleep(5)

    try:
        poiinfo = eval(response.text)['data']["poiInfos"]
    except:
        Operation().insert(table='meituan_error_link', row=url)
        continue

    while poiinfo:
        for pi in poiinfo:
            poi_id = pi['poiId']
            comment_num = pi['allCommentNum']
            avg_price = pi['avgPrice']
            avg_score = pi['avgScore']
            address = pi['address']
            title = pi['title']
            tp = [sorted(_.items(), key=lambda _: _[0]) for _ in pi['dealList']]
            deal_list = re.sub(r"\'|\"", '’', str(tp))
            img_url = pi['frontImg']

            row = [poi_id, comment_num, avg_price, avg_score,
                   address, title, deal_list, url, img_url, sub_id]
            hashkey = md5(''.join(list(map(str, row))).encode('utf-8')).hexdigest()
            row.insert(0, hashkey)

            result = Operation().check_data(table='meituan_shop_info',
                                            w_sub={'poi_id': poi_id})
            if result:
                result_2nd = Operation().check_data(table='meituan_shop_info',
                                                    w_sub={'hashkey': hashkey})
                if result_2nd:
                    continue
                else:
                    Operation().update(table='meituan_shop_info',
                                       row=row)
            else:
                Operation().insert(table='meituan_shop_info', row=row)

        pg = pg + 1
        url = re.sub(re.compile('page=\d+'), 'page=' + str(pg), url)

        response = requests.get(url, headers=ua_random(), timeout=10)
        response.close()
        time.sleep(1)
        try:
            poiinfo = eval(response.text)['data']["poiInfos"]
        except:
            Operation().insert(table='meituan_error_link', row=url)
            continue
