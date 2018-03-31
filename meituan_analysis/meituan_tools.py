import MySQLdb
from datetime import datetime
from fake_useragent import UserAgent


def ua_random():
    headers = {
        "User-Agent": UserAgent().Chrome,
        "Connection": "keep-alive",
        "Referer": "http: // sh.meituan.com / meishi / c17 /",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cookie": '_lxsdk_cuid=1625708bd2bc8-05f323b7dc645b-b34356b-100200-1625708bd2cc8; mtcdn=K; lsu=; _ga=GA1.2.732392839.1521878614; ci=10; iuuid=3888C3C0BBBD90EBDBF4BF3B2CAFD3153C6E47F73CBAF5EF1DC9225054D2C1B7; isid=7445A2771240C6D5E7225984D11A3848; oops=3-Ux7s-zLZinVNuV_W_TyUjoKGgAAAAAkQUAAEDPy6XDwbDp9hUJiwCMO8hmFygnbwNQdwoRmjN99dJiQu3JGVryPLmkJ_k9y67cdg; logintype=normal; cityname=%E4%B8%8A%E6%B5%B7; oc=8fpIkKMHlOWCh9Z9SqumGJBCVCfcqBvG6WviVDkhRsTwmXYvtlJOu3shCAhmCzGoGJQDRzob0mzq0PPzFVYl0mv18ZefBtLtrgTkhNGLeFRKYVpsa77QMYzEa8nDWX6FfdpsV1a0_zaW-oUELAR5pzDTf_jLW-z8lz_lL9gN9Xk; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_f66b37722f586a240d4621318a5a6ebe=1521989513; __utma=211559370.732392839.1521878614.1521989513.1521989513.1; __utmz=211559370.1521989513.1.1.utmcsr=baidu|utmccn=baidu|utmcmd=organic|utmcct=zt_search; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; client-id=4aaf28de-357d-4487-8ab6-bfa4e5bbbede; _lxsdk=3888C3C0BBBD90EBDBF4BF3B2CAFD3153C6E47F73CBAF5EF1DC9225054D2C1B7; __mta=222674468.1521878727953.1522256925439.1522256938561.47; ls=1522256939; SID=pfr6sa7o0lu740aklvlad7jci6; em=bnVsbA; om=bnVsbA; u=764832898; n=rock0205; lt=x7i6XNEktnhPjRFQAjFktkxHP1UAAAAAkQUAAAw1kbhKLwZSlKJnzUXzGCaagvabhG3SIjSfic9MzyYpYvxsRUxNJTfdJG3VYqnDbw; token2=x7i6XNEktnhPjRFQAjFktkxHP1UAAAAAkQUAAAw1kbhKLwZSlKJnzUXzGCaagvabhG3SIjSfic9MzyYpYvxsRUxNJTfdJG3VYqnDbw; uuid=9ea17e3be2df43eb9d29.1521878630.4.0.1; unc=rock0205; __mta=222674468.1521878727953.1522256938561.1522257050800.48; _lxsdk_s=1626d953cdb-59-e0e-59a%7C%7C26'
    }
    return headers


class Operation:
    def __init__(self, *args, **kwargs):
        self.host = "localhost"
        self.user = "root"
        self.passwd = "root"
        self.db = "webspider"
        self.charset = "utf8"
        self.use_unicode = True

        self._conn = self.db_conn()
        if self._conn:
            self._cur = self._conn.cursor()

    def db_conn(self):
        cn = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.passwd,
                             db=self.db,
                             charset=self.charset,
                             use_unicode=self.use_unicode)
        return cn

    def db_close(self):
        if self._conn:
            if type(self._cur) == 'object':
                self._cur.close()

            if type(self._conn) == 'object':
                self._conn.close()

    def check_data(self, table, col='count(*)', w_sub=None):
        if w_sub and isinstance(w_sub, dict):
            t = [k + ' = ' + '"' + str(w_sub[k]) + '"' for k in w_sub]
            if len(t) > 1:
                sub = ' and '.join(t)
            else:
                sub = t[0]
        else:
            sub = '1=1'

        sql = '''select {} from {} where {}'''.format(col, table, sub)
        self._cur.execute(sql)
        if 'count(*)' == col:
            result = self._cur.fetchone()[0]
        else:
            result = self._cur.fetchall()

        return result

    def insert(self, table, row):
        cur = self._conn.cursor()
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if 'meituan_area_info' in table and len(row) == 7:
            row.append(dt)
            insert_sql = """INSERT INTO meituan_area_info (hashkey,main_id,main_area,sub_id,sub_area,url,entry_date)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
            print('new_area_insert', row[0])
            cur.execute(insert_sql, row)

        elif 'meituan_shop_info' in table and len(row) == 11:
            row.append(dt)
            insert_sql = """INSERT INTO meituan_shop_info (hashkey, poi_id,comment_num,avg_price,
                            avg_score,address,title,deal_list,url,img_url,sub_id,entry_date)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            print('new_shop_insert!', row[0])
            cur.execute(insert_sql, row)

        elif 'meituan_error_link' in table:
            insert_sql = """INSERT INTO meituan_error_link (url,entry_date)
                            VALUES (%s,%s)
                """
            r = (row, dt)
            print('error_link_insert', row)
            cur.execute(insert_sql, r)

        cur.close()
        self._conn.commit()

    def update(self, table, row):
        cur = self._conn.cursor()

        if 'meituan_shop_info' in table:
            sql = 'update  {}  '.format(table) + \
                  '''set 
                  hashkey = "%s",
                  poi_id = %s,
                  comment_num = %s,
                  avg_price = %s,
                  avg_score = %s,
                  address = "%s",
                  title = "%s",
                  deal_list = "%s",
                  url = "%s",
                  img_url = "%s",
                  sub_id = %s
                  ''' % tuple(row) + \
                  '  where  poi_id = {};'.format(row[1])
            cur.execute(sql)
            print('shop_info_update', row[0])

        elif 'error_link' in table:
            sql = '''update {} set status = 0 WHERE url = "{}" and status = 1'''.format(table, row)

            cur.execute(sql)
            print('link_status_update', row)

        self._conn.commit()

    def delete(self):
        cur = self._conn.cursor()
        sql =  '''DELETE FROM meituan_error_link WHERE STATUS = 0'''
        cur.execute(sql)
        self._conn.commit()
