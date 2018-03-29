import pandas as pd
import numpy as np

# ser_boj = pd.Series(range(10))
# ser_boj.index
# ser_boj.values
# ser_boj.head(3)
# print(ser_boj[8])
# print(ser_boj * 2)
# print(ser_boj[ser_boj > 7])

# year_data = {'2001': 300, '2002': 300.5, '2003': 450.8}
# ser_obj2 = pd.Series(year_data)
# ser_obj2.name = 'temp'
# ser_obj2.index.name = 'year'
# print(ser_obj2.head())

# dict_data = {'a': 3.14,
#              'b': pd.Timestamp(20170901),
#              'c': pd.Series(1, index=list(range(4)), dtype='float32'),
#              'd': np.array([3]*4,dtype='int32')}
# df = pd.DataFrame(dict_data)
# print(df['b'])
# print(df[['b','d']])
# df['e'] = df['a'] + 9
# # loc按列标题名索引、iloc按序号索引、ix混合索引已名称优先
# print(df.loc[0:2])

# 运算与对齐
# s1 = pd.Series(range(10, 20), index=range(10))
# s2 = pd.Series(range(15, 20), index=range(5))
# # 两不等长的series相加，会出现nan值
# print(s1 + s2)
# # 为了避免nan值出现，为s2填充值，默认填充为0
# print(s1.add(s2, fill_value=0))


# apply/applymap行列函数
# # 定义5行4列的df，-1取绝对值
# df = pd.DataFrame(np.random.randn(5, 4) - 1)
# df = np.abs(df)
# print(df)
# # 用apply函数，参数为传入一个传输名（不用带'()'），或匿名函数
# # 对一组数据进行操作，默认列操作,axis=1为行操作
# print(df.apply(lambda _: _.max(), axis=1))
# # applymap对每一个元素进行操作
# print(df.applymap(lambda _: '%.2f' % _))


# 索引排序
# sort_index/sort_values
# 按值排序，有多列情况sort_values(by='label')按照指定列名

# 处理缺失数据
# 判断是否空值存在
# 丢弃缺失值dropna()
# 默认axi=0（行）；1（列），how=‘any’
# df.dropna()#每行只要有空值，就将这行删除
# df.dropna(axis=1)#每列只要有空值，整列丢弃
# df.dropna(how='all')# 一行中全部为NaN的，才丢弃该行
# df.dropna(thresh=3)# 每行至少3个非空值才保留
# 缺失值填充fillna()
# df.fillna(0)
# df.fillna({1:0,2:0.5}) #对第一列nan值赋0，第二列赋值0.5
# df.fillna(method='ffill') #在列方向上以前一个值作为值赋给NaN
# 当ser或df中有null或nan值则删除，dropna中参数可以选择2个参数
# all或any
# 表示当该行任意单元为空则删除整行或所有为空时删除整行
# dropna
# 填充nan值
# fillna


# pandas统计计算
# sum/mean/max/min...
# df中指定axis=1或0
# skipna排除空值
# 最大索引号/最小索引号
# idmax/idmin/cumsum
# 非常有用，describe可以常用的统计一并输出
# describe
# df = pd.DataFrame(np.random.randn(5, 4), columns=list('ABCD'))
# print(df.sum(axis=1))
# print(df.mean())
# print(df.min())
# print(df.describe())

# 层级索引
# 创建2级内外层表格
# ridx1 = ['x0'] * 3 + ['x1'] * 3 + ['x2'] * 3 + ['x3'] * 3
# ridx2 = [0, 1, 2] * 4
# df_obj = pd.DataFrame(np.random.randn(12, 5),
#                       columns=['y' + str(_) for _ in range(5)],
#                       index=[ridx1,
#                              ridx2])
# print(df_obj)
# df_obj.index.names = ['key1', 'key2']
# # 选取外层
# # print(df_obj.loc['x0',:])
# # 选取内层
# print(df_obj.query('key2==2'))
# # print(df_obj.loc[[(k,2) for k in set(ridx1)]])
# # print(df_obj.keys('key2'))
# # 交换分层顺序
# df_swap = df_obj.swaplevel()
# # print(df_swap)
# # # 内外层交换后排序
# # print(df_obj.swaplevel().sortlevel(ascending=False))
# for i in df_swap.groupby(level='key2'):
#     print(i)

#
# df_obj1 = pd.DataFrame(np.random.randn(3, 2),
#                        columns=['y1', 'y2'],
#                        )
# df_obj2 = pd.DataFrame(np.random.randn(5, 2),
#                        columns=['y1', 'y3'],
#                        )
# print(df_obj2)
