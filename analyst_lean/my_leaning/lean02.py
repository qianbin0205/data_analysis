import pandas as pd

#
# with open('./L2/python_baidu.txt', 'r+', encoding='utf-8') as f1_txt:
#     print(f1_txt.read())
#     f1_txt.seek(0)
#     line = f1_txt.readline()
#     while line:
#         print(line, end='')
#         line = f1_txt.readline()

df = pd.read_csv('./L2/gender_country.csv', usecols=['女性'], encoding='utf-8')
# print(df.head())
country_se = df.loc[[]]
print(country_se)
