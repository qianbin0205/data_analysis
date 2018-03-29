import csv

f = open('./L1\survey.csv', 'r', newline='')
table = csv.reader(f)
result_dict = {}
male_tup = 'male', 'm'
female_tup = 'female', 'f'

for row_n, row_v in enumerate(table):
    if row_n == 0:
        continue
    else:
        gender = row_v[2].strip().lower()
        country = row_v[3].strip().lower()
        if country not in result_dict:
            result_dict[country] = [0, 0]
        if gender in female_tup:
            result_dict[country][0] += 1
        if gender in male_tup:
            result_dict[country][1] += 1
# 防止表头乱码编码为gb18030
with open(r'D:\PyScript\analyst_lean\L1\gender&country.csv',
          'w+', newline='', encoding='gb18030') as csvf:
    # 以','分割
    fw = csv.writer(csvf, delimiter=',')
    fw.writerow(['国家', '男性', '女性'])
    for k, v in result_dict.items():
        fw.writerow([k, v[0], v[1]])
    csvf.close()
