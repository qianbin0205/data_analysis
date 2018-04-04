# _*_coding=gbk
import requests
import re
import time
from hashlib import md5
from meituan_tools import Operation
from meituan_tools import ua_random


def err_redo():
    s = requests.session()
    s.keep_alive = False
    op = Operation()
    headers = ua_random()
    result = op.check_data(table='meituan_error_link',
                           col='url',
                           w_sub={'status': 1})
    for u in result:

        url = u[0]
        if 'areaId' in url:
            sub_id = re.findall('areaId=(\d+?)&', url)[0]
            class_type = 2
        elif 'cateId' in url:
            sub_id = re.findall('cateId=(\d+?)&', url)[0]
            class_type = 1
        else:
            raise KeyError('sub key not in url')

        pg = int(re.findall('page=(\d+?)&', url)[0])

        op.update(table='meituan_error_link',
                  row=url)
        response = s.get(url, headers=headers)
        time.sleep(5)

        try:
            poiinfo = eval(response.text)['data']["poiInfos"]
        except:
            op.insert(table='meituan_error_link', row=url)
            time.sleep(5)
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
                deal_list = re.sub(r"\'|\"", "’", str(tp))
                img_url = pi['frontImg']

                row = [poi_id, comment_num, avg_price, avg_score,
                       address, title, deal_list, url, img_url, sub_id, class_type]
                hashkey = md5(''.join(list(map(str, row))).encode('utf-8')).hexdigest()
                row.insert(0, hashkey)

                result = op.check_data(table='meituan_shop_info',
                                       w_sub={'poi_id': poi_id,
                                              'sub_id': sub_id})
                if result:
                    result_2nd = op.check_data(table='meituan_shop_info',
                                               w_sub={'hashkey': hashkey,
                                                      'poi_id': poi_id})
                    if result_2nd:
                        continue
                    else:
                        op.update(table='meituan_shop_info',
                                  row=row)
                else:
                    op.insert(table='meituan_shop_info', row=row)

            pg = pg + 1
            url = re.sub(re.compile('page=\d+'), 'page=' + str(pg), url)

            response = s.get(url, headers=headers)
            time.sleep(1)
            try:
                poiinfo = eval(response.text)['data']["poiInfos"]
            except:
                op.insert(table='meituan_error_link', row=url)
                time.sleep(5)
                continue

    op.clear_err_link()
    r = op.check_data(table='meituan_error_link',
                      col='url',
                      w_sub={'status': 1})
    s.close()
    op.db_close()
    if r:
        err_redo()

    return
