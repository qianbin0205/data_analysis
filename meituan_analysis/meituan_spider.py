import requests
import re
import time
from hashlib import md5
from meituan_error_spider import err_redo
from meituan_tools import Operation
from meituan_tools import ua_random

s = requests.session()
s.keep_alive = False
op = Operation()
headers = ua_random()
# 一级区域大列表抓取
# response = requests.get(
#     url='http://sh.meituan.com/meishi/',
#     headers=ua_random()
# )
# reg_area = re.compile('.*"areas":(\[.*\]).*"dinnerCountsAttr".*', re.DOTALL)
# data = json.loads(reg_area.findall(response.text)[0])

# result = op.check_data(table='meituan_area_info')
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
#             op.insert(table='meituan_area_info', row=row)
# 二级店铺抓取
result = op.check_data(table='meituan_area_info',
                       col='sub_id')

for r in result:
    uid = str(r[0])
    url = 'http://sh.meituan.com/meishi/api/poi/getPoiList?' \
          'uuid=9ea17e3be2df43eb9d29.1521878630.3.0.1&platform=1' \
          '&partner=126&riskLevel=1&optimusCode=1&cityName=%E4%B8%8A%E6%B5%B7' \
          '&areaId={}&page=1&userId=764832898'.format(uid)
    pg = 1
    response = s.get(url, headers=headers)
    time.sleep(1)
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
            deal_list = re.sub(r"\'|\"", '’', str(tp))
            img_url = pi['frontImg']
            sub_id = uid

            row = [poi_id, comment_num, avg_price, avg_score,
                   address, title, deal_list, url, img_url, sub_id]
            hashkey = md5(''.join(list(map(str, row))).encode('utf-8')).hexdigest()
            row.insert(0, hashkey)

            result = op.check_data(table='meituan_shop_info',
                                   w_sub={'poi_id': poi_id})
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
s.close()
op.db_close()
err_redo()
