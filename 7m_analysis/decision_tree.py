import csv
from sklearn.feature_extraction import DictVectorizer
from sklearn.externals.six import StringIO
from sklearn import tree
from sklearn import preprocessing

file = open(r"D:\pypro\mleaning\tree.csv", "r")
coll = csv.reader(file)

lab = []
fature = []

tab = [t[0] for t in coll]
tit = tab[0].split("\t")

for r in tab[1:]:
    lab.append(r[-1])

    r1 = r.split("\t")
    rowdict = {tit[cnt]: r1[cnt] for cnt in range(1, 5)}
    fature.append(rowdict)

# print(fature)
# print(lab)
vec = DictVectorizer()
dummyx = vec.fit_transform(fature).toarray()
print(dummyx)
print(vec.get_feature_names())
lb = preprocessing.LabelBinarizer()
dummyy = lb.fit_transform(lab)
print("dummy:" + str(dummyy))
dectree = tree.DecisionTreeClassifier(criterion="entropy")
clf = dectree.fit(dummyx, dummyy)
print("clf:" + str(clf))
