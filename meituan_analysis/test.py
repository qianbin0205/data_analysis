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

a = [3245331, 5116, 26, 3.1, '�ɽ��������ֵ�������·���󷢳����ײ�552-652�ţ�������·���ֱ�·��', '����Դ���ɽ����󷢵꣩', '[[(��price��, 18), (��soldCounts��, 273527), (��title��, ��20Ԫ����ȯ1�ţ��ɵ��ӡ�)], [(��price��, 43.5), (��soldCounts��, 281890), (��title��, ��50Ԫ����ȯ1�ţ��ɵ��ӡ�)], [(��price��, 22), (��soldCounts��, 147724), (��title��, �������������1�ݡ�)], [(��price��, 29), (��soldCounts��, 96562), (��title��, ������ţ���������+�ֹ�ţ���1�ݡ�)], [(��price��, 25), (��soldCounts��, 83350), (��title��, ����ζ��������+��ζ�ش���1�ݡ�)], [(��price��, 22), (��soldCounts��, 87941), (��title��, ����ţ���ŷ�+Сľ��+������ʲ�1�ݡ�)], [(��price��, 35), (��soldCounts��, 5669), (��title��, ��������������+��ζ�ش���1�ݡ�)]]', 'http://sh.meituan.com/meishi/api/poi/getPoiList?uuid=9ea17e3be2df43eb9d29.1521878630.3.0.1&platform=1&partner=126&riskLevel=1&optimusCode=1&cityName=%E4%B8%8A%E6%B5%B7&cateId=60&page=1&userId=764832898', 'http://p0.meituan.net/600.600/deal/0b23240b3a5f3ed86623664f96a7067c173651.jpg', '60', 1]
hashkey = md5(''.join(list(map(str, a))).encode('utf-8')).hexdigest()
print(hashkey)

a = [3245331, 5116, 26, 3.1, '�ɽ��������ֵ�������·���󷢳����ײ�552-652�ţ�������·���ֱ�·��', '����Դ���ɽ����󷢵꣩', '[[(��price��, 18), (��soldCounts��, 273527), (��title��, ��20Ԫ����ȯ1�ţ��ɵ��ӡ�)], [(��price��, 43.5), (��soldCounts��, 281890), (��title��, ��50Ԫ����ȯ1�ţ��ɵ��ӡ�)], [(��price��, 22), (��soldCounts��, 147724), (��title��, �������������1�ݡ�)], [(��price��, 29), (��soldCounts��, 96562), (��title��, ������ţ���������+�ֹ�ţ���1�ݡ�)], [(��price��, 25), (��soldCounts��, 83350), (��title��, ����ζ��������+��ζ�ش���1�ݡ�)], [(��price��, 22), (��soldCounts��, 87941), (��title��, ����ţ���ŷ�+Сľ��+������ʲ�1�ݡ�)], [(��price��, 35), (��soldCounts��, 5669), (��title��, ��������������+��ζ�ش���1�ݡ�)]]', 'http://sh.meituan.com/meishi/api/poi/getPoiList?uuid=9ea17e3be2df43eb9d29.1521878630.3.0.1&platform=1&partner=126&riskLevel=1&optimusCode=1&cityName=%E4%B8%8A%E6%B5%B7&cateId=60&page=1&userId=764832898', 'http://p0.meituan.net/600.600/deal/0b23240b3a5f3ed86623664f96a7067c173651.jpg', '60', 2]
hashkey = md5(''.join(list(map(str, a))).encode('utf-8')).hexdigest()
print(hashkey)