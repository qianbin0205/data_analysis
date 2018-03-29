import requests
import re
import time
import json
from hashlib import md5
from meituan_tools import Operation
from meituan_tools import ua_random

response = requests.get(
    url='http://sh.meituan.com/meishi/',
    headers=ua_random()
)
# reg_area = re.compile('.*"areas":(\[.*\]).*"dinnerCountsAttr".*', re.DOTALL)
# data = json.loads(reg_area.findall(response.text)[0])

# result = Operation().check_data(table='meituan_area_info')
# if result:
#     for main in data:
#         main_id = int(main['id'])
#         main_area = main['name']
#         for sub in main['subAreas']:
#             sub_id = int(sub['id'])
#             sub_area = sub['name']
#             sub_url = sub['url']
#             row = [main_id, main_area, sub_id, sub_area, sub_url]
#             hashkey = md5(''.join(list(map(str, row))).encode('utf-8')).hexdigest()
#             row_all = row.insert(0, hashkey)
#             Operation().insert(table='meituan_area_info', row=row)

result = Operation().check_data(table='meituan_area_info',
                                col='sub_id')
err_list = []
for r in result:
    uid = str(r[0])
    url = 'http://sh.meituan.com/meishi/api/poi/getPoiList?' \
          'uuid=9ea17e3be2df43eb9d29.1521878630.3.0.1&platform=1' \
          '&partner=126&riskLevel=1&optimusCode=1&cityName=%E4%B8%8A%E6%B5%B7' \
          '&areaId={}&page=1&userId=764832898'.format(uid)
    pg = 1
    response = requests.get(url, headers=ua_random())
    time.sleep(1)
    try:
        data = eval(response.text)['data']
    except:
        print('first data eval error!', url)
        err_list.append(url)
        continue
    poiinfo = data["poiInfos"]
    while poiinfo:
        if pg > 1:
            response = requests.get(url, headers=ua_random())
            time.sleep(1)
            try:
                data = eval(response.text)['data']
            except:
                print('poiinfo eval error!', url)
                err_list.append(url)
            poiinfo = data["poiInfos"]

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
            sub_id = uid

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
                Operation().insert(table='meituan_area_info', row=row)

        pg = pg + 1
        url = re.sub(re.compile('page=\d+'), 'page=' + str(pg), url)

while err_list:
    print('err_list_cnt:', len(err_list))
    url = err_list.pop(0)
    response = requests.get(url, headers=ua_random())
    time.sleep(1)
    try:
        data = eval(response.text)['data']
    except:
        err_list.append(url)
        print('errlist eval error!', url)
        continue
    poiinfo = data["poiInfos"]

    sub_id = re.compile('areaId=(\d+)').findall(url)[0]
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
        row2 = row.insert(0, hashkey)

        result = Operation().check_data(table='meituan_shop_info',
                                        col={'poi_id': poi_id})
        if result:
            if Operation().check_data(table='meituan_shop_info',
                                      col={'hashkey': hashkey}):
                Operation().update(table='meituan_shop_info',
                                   row=row2)
        else:
            Operation().insert(table='meituan_area_info', row=row)

Operation().db_close()
