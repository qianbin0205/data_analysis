# coding=gbk
import requests
import re
import time
import json
from meituan_tools import Operation
from hashlib import md5

# from meituan_tools import ua_random

# op = Operation()
# result = op.check_data(table='meituan_error_link',
#                        col='url',
#                        w_sub={'status': 1})
#
# print(result)
# if result:
#     print(True)

a = [3245331, 5116, 26, 3.1, '松江区岳阳街道荣乐中路大润发超市首层552-652号（荣乐中路西林北路）', '蒙自源（松江大润发店）', '[[(’price’, 18), (’soldCounts’, 273527), (’title’, ’20元代金券1张，可叠加’)], [(’price’, 43.5), (’soldCounts’, 281890), (’title’, ’50元代金券1张，可叠加’)], [(’price’, 22), (’soldCounts’, 147724), (’title’, ’菌香过桥米线1份’)], [(’price’, 29), (’soldCounts’, 96562), (’title’, ’番茄牛肉过桥米线+手工牛肉饼1份’)], [(’price’, 25), (’soldCounts’, 83350), (’title’, ’傣味酸汤米线+回味素串串1份’)], [(’price’, 22), (’soldCounts’, 87941), (’title’, ’肥牛过桥饭+小木耳+金桔柠檬茶1份’)], [(’price’, 35), (’soldCounts’, 5669), (’title’, ’松茸土鸡米线+回味素串串1份’)]]', 'http://sh.meituan.com/meishi/api/poi/getPoiList?uuid=9ea17e3be2df43eb9d29.1521878630.3.0.1&platform=1&partner=126&riskLevel=1&optimusCode=1&cityName=%E4%B8%8A%E6%B5%B7&cateId=60&page=1&userId=764832898', 'http://p0.meituan.net/600.600/deal/0b23240b3a5f3ed86623664f96a7067c173651.jpg', '60', 1]
hashkey = md5(''.join(list(map(str, a))).encode('utf-8')).hexdigest()
print(hashkey)

a = [3245331, 5116, 26, 3.1, '松江区岳阳街道荣乐中路大润发超市首层552-652号（荣乐中路西林北路）', '蒙自源（松江大润发店）', '[[(’price’, 18), (’soldCounts’, 273527), (’title’, ’20元代金券1张，可叠加’)], [(’price’, 43.5), (’soldCounts’, 281890), (’title’, ’50元代金券1张，可叠加’)], [(’price’, 22), (’soldCounts’, 147724), (’title’, ’菌香过桥米线1份’)], [(’price’, 29), (’soldCounts’, 96562), (’title’, ’番茄牛肉过桥米线+手工牛肉饼1份’)], [(’price’, 25), (’soldCounts’, 83350), (’title’, ’傣味酸汤米线+回味素串串1份’)], [(’price’, 22), (’soldCounts’, 87941), (’title’, ’肥牛过桥饭+小木耳+金桔柠檬茶1份’)], [(’price’, 35), (’soldCounts’, 5669), (’title’, ’松茸土鸡米线+回味素串串1份’)]]', 'http://sh.meituan.com/meishi/api/poi/getPoiList?uuid=9ea17e3be2df43eb9d29.1521878630.3.0.1&platform=1&partner=126&riskLevel=1&optimusCode=1&cityName=%E4%B8%8A%E6%B5%B7&cateId=60&page=1&userId=764832898', 'http://p0.meituan.net/600.600/deal/0b23240b3a5f3ed86623664f96a7067c173651.jpg', '60', 2]
hashkey = md5(''.join(list(map(str, a))).encode('utf-8')).hexdigest()
print(hashkey)