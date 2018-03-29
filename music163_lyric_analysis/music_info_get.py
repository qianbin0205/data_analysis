from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import json
import MySQLdb
import re

conn = MySQLdb.connect(host="localhost",
                       user="root",
                       passwd="root",
                       db="webspider",
                       charset="utf8",
                       use_unicode=True)
cursor = conn.cursor()
cursor2 = conn.cursor()


def ua_random():
    headers = {
        "User-Agent": UserAgent().Chrome,
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Referer": "http: // music.163.com /"
    }
    return headers


url = 'http://music.163.com/artist/album?id=6460&limit=108'
# url = 'http://music.163.com/artist/album?id=6066&limit=24'

response = requests.get(url, headers=ua_random())
print(response.status_code)
soup = BeautifulSoup(response.content, 'lxml')
album_href_taglist = soup.select('a.tit.s-fc0')

album_href_list = [_.get('href') for _ in album_href_taglist]
album_id_list = [_.split('=')[1].strip() for _ in album_href_list]
print(album_id_list)
for album_id in album_id_list:
    url2 = ''.join(['http://music.163.com/album?id=', album_id])
    response2 = requests.get(url2, headers=ua_random())
    soup2 = BeautifulSoup(response2.content, 'lxml')
    # print(soup2)
    song_taglist = soup2.select('ul.f-hide a')
    # print(song_taglist)
    song_href_list = [_.get('href') for _ in song_taglist]
    song_id_list = [_.split('=')[1].strip() for _ in song_href_list]
    # print(song_id_list)

    album_id = album_id.strip()
    try:
        album_name = soup2.select_one('h2.f-ff2').get_text().strip()
        album_issue_date = soup2.select('p.intr')[1].get_text().split('：')[1].strip()
        try:
            issue_company_name = soup2.select('p.intr')[2].get_text().split('：')[1].strip()
        except IndexError:
            issue_company_name = None
    except:
        album_name = None
        album_issue_date = None
        print(response2.status_code, response2.url)
        continue

    insert_sql = """INSERT INTO album_info(album_id ,album_name,album_issue_date,issue_company_name)
                    VALUES (%s, %s, %s, %s)
    """
    print(album_id,
          album_name,
          album_issue_date,
          issue_company_name)
    cursor.execute(insert_sql, (album_id,
                                album_name,
                                album_issue_date,
                                issue_company_name))

    song_info_temp = soup2.textarea.get_text()
    song_info = json.loads(song_info_temp)

    for v in song_info:
        song_id = v['id']
        song_name = v['name']
        singer = ','.join([_['name'] for _ in v['artists']])
        song_time = None
        album_id = album_id.strip()

        url3 = ''.join(['http://music.163.com/api/song/lyric?os=pc&id=',
                        str(song_id),
                        '&lv=-1&kv=-1&tv=-1'])

        response3 = requests.get(url3, headers=ua_random())
        # time.sleep(1)
        soup3 = BeautifulSoup(response3.content, 'lxml')
        # print(soup3.get_text())
        try:
            lrc_temp = json.loads(soup3.get_text())['lrc']['lyric']
            lyric = re.sub(r"\[(.*)\]", '', lrc_temp)
        except KeyError:
            lyric = '无歌词'

        except json.decoder.JSONDecodeError:
            lyric = None
            print(response3.status_code, response3.url)

        insert_sql = """INSERT INTO song_info(song_id,song_name,song_time,singer,lyric,album_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
        """
        # print(song_id,
        #       song_name,
        #       song_time,
        #       singer,
        #       lyric,
        #       album_id
        # )

        cursor2.execute(insert_sql, (song_id,
                                     song_name,
                                     song_time,
                                     singer,
                                     lyric,
                                     album_id))

conn.commit()
conn.close()

