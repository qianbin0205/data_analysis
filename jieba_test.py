import jieba
import jieba.analyse
import jieba.posseg as psg

f = open(r'D:\Temp\a202.txt')
text = f.read()
# seg_list = jieba.cut(text, cut_all=True)
# # join是split的逆操作
# # 即使用一个拼接符将一个列表拼成字符串
# # print("/ ".join(seg_list))  # 全模式
#
seg_list = jieba.cut(text, cut_all=False)
print("/ ".join(seg_list))  # 精确模式
for s in seg_list:
    print(s)
# seg_list = jieba.cut(text)  # 默认是精确模式
# print("/ ".join(seg_list))
#
# seg_list = jieba.cut_for_search(text)  # 搜索引擎模式
# print("/ ".join(seg_list))

keywords = jieba.analyse.extract_tags(text, topK=100, withWeight=True, allowPOS=())
for i in keywords:
    print(i[0].flag, i[1], i)


# 还有一种是rank模式


# type2

# 停用词
# 创建停用词列表
# def get_stopwords_list():
#     stopwords = [line.strip() for line in open('stopwords.txt', encoding='UTF-8').readlines()]
#     return stopwords
#
#
# # 对句子进行中文分词
# def seg_depart(sentence):
#     # 对文档中的每一行进行中文分词
#     sentence_depart = jieba.lcut(sentence.strip())
#     return sentence_depart


# def remove_digits(input_str):
#     punc = u'0123456789.'
#     output_str = re.sub(r'[{}]+'.format(punc), '', input_str)
#     return output_str

# 去除停用词
# def move_stopwords(sentence_list, stopwords_list):
#     # 去停用词
#     out_list = []
#     for word in sentence_list:
#         if word not in stopwords_list:
#             if not remove_digits(word):
#                 continue
#             if word != '\t':
#                 out_list.append(word)
#     return out_list
#
# 样例如下：
# sentence = '1、判令被告赵军霞偿还原告借款本息及应收费用共计4278.6元（计算至2017年1月10日，实际还款额以合同约定的计费方式计算至最终还款日）'
# stopwords = get_stopwords_list()
# sentence_depart = seg_depart(sentence)
# print(sentence_depart)
# sentence_depart = move_stopwords(sentence_depart, stopwords)
# print(sentence_depart)
