import jieba
import jieba.analyse
import jieba.posseg as psg


# seg_list = jieba.cut(text, cut_all=True)
# # # join是split的逆操作
# # # 即使用一个拼接符将一个列表拼成字符串
# # # print("/ ".join(seg_list))  # 全模式
# #
# seg_list = jieba.cut(text, cut_all=False)
# # print("/ ".join(seg_list))  # 精确模式
#
# # seg_list = jieba.cut(text)  # 默认是精确模式
# # print("/ ".join(seg_list))
# #
# # seg_list = jieba.cut_for_search(text)  # 搜索引擎模式
# # print("/ ".join(seg_list))
#
# keywords = jieba.analyse.extract_tags(text,topK=20,withWeight=True,allowPOS=())
# for i in keywords:
#     print(i[0],i[1])

# 还有一种是rank模式