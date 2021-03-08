from test import Test
from porn_sites import _get_porn_collection, _get_site_name
from flask import Flask, request, abort, Response
from flask_restful import Resource
from flask_cors import CORS
import json
import html2text
import urllib.request
import sys
import os

sys.path.append(os.path.abspath("./test.py"))


app = Flask(__name__)
CORS(app)
ENV = 'dev'
if ENV == 'dev':
    app.debug = True
h = html2text.HTML2Text()
h.ignore_links = True
h.bypass_tables = False
h.ignore_images = True
h.quote = False
h.ignore_emphasis = True
h.wrap_links = False
h.emphasis = "|||"


@app.route('/api/filter', methods=['GET', 'POST'])
def testFunc():
    try:
        if request.method == 'POST':
            include_text = request.args.get('include_text')

            body = request.json
            url = body["url"]

            req = urllib.request.Request(url)
            req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')


            with urllib.request.urlopen(req) as response:
                charset = response.info().get_content_charset()
                html = response.read().decode(charset)
                result = h.handle(html)
                result = prepareText(result)
                if result != '':
                    NLP_result = Test(result, url)
                    if include_text:
                        return {"naive_bayes_result": NLP_result,
                                'extracted_text': result}
                    return {"naive_bayes_result": NLP_result}
                else:
                    url = _get_site_name(url)
                    porn_collection_sites = _get_porn_collection()
                    for site in porn_collection_sites:
                        if url in site:
                            return 'Porn Site'
                    return 'Not Porn'
        return rise_error(403, 'not supported.')
    except Exception as e:
        url = _get_site_name(url)
        porn_collection_sites = _get_porn_collection()
        for site in porn_collection_sites:
            if url in site:
                return 'Porn Site'
        return str(e)


def prepareText(str):
    result = ''
    delimiter = '\n'
    arr = str.split('\n')
    for line in arr:
        if len(line) != 0:
            line = ''.join(
                [i for i in line if not i.isdigit() and not invalid_char(i)])
            line = line.lower()
            line = remove_unwanted_words(line)
            if is_empty_string(line):
                continue
            result += line+delimiter
    return result


def invalid_char(c):
    invalid_char = ['#', '*', '▼', ':', '+', '>', '<', "©", '@', '^', '&', '~', '₪', '™'
                    '\\', '-', '.', '%', ',', "'", '!', '$', '|', '(', ')', '/', '•', '[', ']', '_', '?', '»', '«', '"']
    for _c in invalid_char:
        if _c == c:
            return True
    return False


def remove_unwanted_words(str):
    delimiter = ' '
    words = str.split(delimiter)
    fillter = ['login', 'logging', 'sign', 'signup', 'and', 'more',
               'k', 'p', 'views', 'or', 'a', 'x', 'hd', 'm', 'from',
               'mm', 'yy', 'all', 'i', 'ok', 'is', 'u', 'was', 'to',
               'are', 'date', 'this', 'in', 'up', 't', 's', 'if',
               'the', 'it', 'd', 'my', 'you', 'by', 'at', '₪']
    result = ''
    for word in words:
        if word in fillter:
            continue
        result += word+delimiter
    return result


def is_empty_string(str):
    space = ' '
    for c in str:
        if c != space:
            return False
    return True


def rise_error(status, msg):
    response = {'description': msg}
    return Response(json.dumps(response), status=status, headers=None, mimetype=None, content_type='application/json')


if __name__ == '__main__':
    app.run()
