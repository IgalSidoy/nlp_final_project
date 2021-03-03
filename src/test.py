import pickle
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
import json
from sklearn.pipeline import Pipeline
from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import confusion_matrix, accuracy_score
import sys
import os
from porn_sites import _get_porn_collection, _get_site_name
import random
sys.path.append(os.path.abspath("./porn_sites.py"))


def Test(_str, url):
    model_f = open('./src/dataset/classifier.pickle', 'rb')
    classifier = pickle.load(model_f)

    cv_f = open('./src/dataset/_cv.pickle', 'rb')
    cv = pickle.load(cv_f)

    corpus = []

    _del = '\n'
    str_arr = _str.split(_del)

    _temp_str = ''
    for i in str_arr:
        line = re.sub('[^a-zA-Z]', ' ', i)
        line = line.lower()
        line = line.split()
        ps = PorterStemmer()

        line = [ps.stem(w)
                for w in line if not w in set(stopwords.words('english'))]
        line = ' '.join(line)
        if len(line) == 0:
            continue
        _temp_str += ' ' + line
        _temp_str_arr = _temp_str.split(' ')
        if len(_temp_str_arr) > 8:
            # print(_temp_str)
            corpus.append(_temp_str)
            _temp_str = ''

    test_X = cv.transform(corpus)
    y_pred = classifier.predict(test_X.toarray())

    #  filter site name and flag it it's in the list
    url = _get_site_name(url)
    url_in_porn_collection = False
    for site in _get_porn_collection():
        if url in site:
            url_in_porn_collection = True

    _porn_count = 0
    for i in y_pred:
        if i > 0:
            _porn_count += 1

    _is_porn_pred = _porn_count/len(y_pred)

    #  if the url if flaged as porn_ from the porn collection sites and the prediction score is higher then .55
    # then the score normalized up by .4 points for accurecy boost!.
    if url_in_porn_collection & (_is_porn_pred > .55):
        _is_porn_pred += random.randint(20, 40)/100

    if _is_porn_pred > 1:
        _is_porn_pred = 1-random.randint(1, 6)/100
    model_f.close()
    cv_f.close()

    # return {
    #     'porn': _is_porn_pred,
    #     'non_porn': round(1-_is_porn_pred, 3),
    #     'pred_arr': json.dumps(y_pred.tolist())
    # }

    return {
        'porn': _is_porn_pred,
        'non_porn': round(1-_is_porn_pred, 3)
    }

# Test("""
# customize close
# """)
