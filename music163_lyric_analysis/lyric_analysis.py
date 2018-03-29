import MySQLdb
import pandas
import jieba
import jieba.analyse
import jieba.posseg as psg

conn = MySQLdb.connect(host="localhost",
                       user="root",
                       passwd="root",
                       db="webspider",
                       charset="utf8",
                       use_unicode=True)

sql = '''
SELECT * from webspider.album_info as a
left join webspider.song_info as b on a.album_id = b.album_id
where b.lyric IS NOT NULL AND b.lyric <> '无歌词'

'''
df = pandas.read_sql(sql, con=conn, )
# print(df.head(10))
t_list = df.lyric
all_union_text = ';'.join(t_list).replace('作曲 :', '').replace('作词 :', '')
text = ','.join(set(','.join(set(all_union_text.split('\n'))).split()))

# seg_listh = jieba.cut(all_union_text,cut_all=True)
# print(' '.join(seg_list))

keywords = jieba.analyse.extract_tags(text, topK=30, withWeight=True, allowPOS=('n', 'nv'))
for i in keywords:
    print(i[0], i[1])
