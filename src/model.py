
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import datetime
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix, accuracy_score
import pickle


print('------------------------------------- loading dataset  -------------> ' +
      str(datetime.datetime.now()))

dataset = pd.read_csv('src/dataset/final_data_set_1.csv',
                      delimiter=',', quoting=3)


corpus = []

print('------------------------------------- cleaning stop words ----------> ' +
      str(datetime.datetime.now()))
for i in range(0, len(dataset)):
    line = re.sub('[^a-zA-Z]', ' ', dataset['text_line'][i])
    line = line.lower()
    line = line.split()
    ps = PorterStemmer()
    line = [ps.stem(w)
            for w in line if not w in set(stopwords.words('english'))]
    line = ' '.join(line)
    corpus.append(line)
# the top  frequent words from the corpuse
cv = CountVectorizer(max_features=5200)

print('------------------------------------- creating bag of words model --> ' +
      str(datetime.datetime.now()))

_fit_transform = cv.fit_transform(corpus)

X = _fit_transform.toarray()

Y = dataset['score'].values


print(
    '------------------------------------- number of words --------------> ' + str(len(X[0])))


print(
    '---------------- split dataset into test and train set -------------> ' + str(datetime.datetime.now()))

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=0)


print(
    '----------------  train naive bayes model --------------------------> ' + str(datetime.datetime.now()))

classifier = GaussianNB()
classifier.fit(X_train, Y_train)


print(
    '----------------  prediction test results --------------------------> ' + str(datetime.datetime.now()))

y_pred = classifier.predict(X_test)

# print(np.concatenate((y_pred.reshape(len(y_pred), 1), Y_test.reshape(len(Y_test), 1)), 1))


print(
    '----------------  making confusion matrix --------------------------> ' + str(datetime.datetime.now()))

cm = confusion_matrix(Y_test, y_pred)
print(cm)
print(accuracy_score(Y_test, y_pred))


f = open('./src/dataset/classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()

f = open('./src/dataset/_cv.pickle', 'wb')
pickle.dump(cv, f)
f.close()
