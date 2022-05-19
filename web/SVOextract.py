# -*- coding: utf-8 -*-

from io import StringIO
from flask import Flask, render_template, request, Response, Blueprint
from web import extract_data, extract_SVO
import re
from pandas import DataFrame as df

SVOextract = Blueprint('SVOextract', __name__, template_folder='templates')

# app.debug = True
# SVOextract.jinja_env.globals.update(zip=zip)
file_csv = []
@SVOextract.route('/post')
def one_sentence():
    return render_template('post.html')

@SVOextract.route('/file')
def file_sentence():
    return render_template("file-post.html")

@SVOextract.route('/result', methods = ['POST', 'GET'])
def result():
    global file_csv
    if request.method == 'POST':
        sentence = request.form['sentence']
        if len(sentence) == 0:
            return "<script type='text/javascript'>alert('빈 문장입니다. 문장을 다시 입력해주세요.');</script>"
        else:
            temp = re.split('(?<=[^0-9])[\.|\r|\?|\!|\n]', sentence)
            sentences = []
            for text in temp:
                if len(text) > 0:
                    sentences.append(text)
            if len(sentences) > 5000:
                return "<script type='text/javascript'>alert('죄송합니다. 용량을 초과하였습니다.');</script>"
            elif len(sentences) > 1:
                data = extract_data.get_data(sentences, False)
            else:
                data = extract_data.get_data(sentence)
            result = extract_SVO.extract_svo(data)
            file_csv = result
            return render_template("result.html", result = result)

@SVOextract.route('/file-result', methods = ['POST', 'GET'])
def file_result():
    global file_csv
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == "":
            return "<script type='text/javascript'>alert('빈 파일입니다. 파일을 다시 제출해주세요.');</script>"
        else:
            f.save(f.filename)
            texts = ""
            with open(f.filename, 'r', encoding='utf-8') as infile:
                for sentence in infile.readlines():
                    texts = texts + '\n' + sentence
            temp = re.split('(?<=[^0-9])[\.|\r|\?|\!|\n]', texts)
            sentences = []
            for text in temp:
                if len(text) > 0:
                    sentences.append(text)
            if len(sentences) > 5000:
                return "<script type='text/javascript'>alert('죄송합니다. 용량을 초과하였습니다.');</script>"
            elif len(sentences) > 1:
                data = extract_data.get_data(sentences, False)
            else :
                data = extract_data.get_data(sentences[0])
            result = extract_SVO.extract_svo(data)
            file_csv = result
            return render_template('result.html', result = result)

@SVOextract.route('/csv_file_download')
def csv_file_download():
    output_stream = StringIO()
    output_stream.write(u'\ufeff')
    subjects = []
    objects = []
    verbs = []
    texts = []
    ids = []
    for d in file_csv:
        for i in range(len(d['subjects'])):
            subjects.append(d['subjects'][i])
            objects.append(d['objects'][i])
            verbs.append(d['verbs'][i])
            texts.append(d['text'])
            ids.append(d['id'])
    my_dict = {"ID": ids, "주어": subjects, "목적어": objects, "동사": verbs, "문장": texts}
    temp_df = df(data=my_dict, columns=['ID', '주어', '목적어', '동사', '문장'])
    temp_df.to_csv(output_stream)
    response = Response(
        output_stream.getvalue(),
        mimetype='text/csv',
        content_type='application/octet-stream',
    )
    response.headers['Content-Disposition'] = "attachment; filename=SVO.csv"
    return response
