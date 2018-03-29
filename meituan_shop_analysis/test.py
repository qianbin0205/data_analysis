# import requests
# import re
# import time
# import json
# from meituan_tools import select_fun, insert_fun, update_fun
# from meituan_tools import ua_random

row  = range(11)
x = '''set 
     poi_id = %s,
     comment_num = %s,
     avg_price = %s,
     avg_score = %s,
     address = %s,
     title = %s,
     deal_list = %s,
     url = %s,
     img_url = %s,
     sub_id = %s
     ''' % tuple(row)

print(x)
