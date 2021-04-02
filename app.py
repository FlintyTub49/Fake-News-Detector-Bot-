import os
from flask import Flask, request, render_template
import requests
import pickle as pk
from bs4 import BeautifulSoup

from preprocessing import preprocess_text

from rake_nltk import Rake
from googlesearch import search
import urllib.request as urllib
from urllib.request import urlopen


codePath = os.path.dirname(os.path.abspath('preprocessing.py'))
pipe = os.path.join(codePath, 'Models/100lenPipelineLem.pk')
pipeline = pk.load(open(pipe, 'rb'))

# TODO: Fix js files not working
app = Flask(__name__, template_folder='templates')

# app.config['EXPLAIN_TEMPLATE_LOADING'] = True

# @app.before_request
# def init_global_flag():
#     g.hello_flag = 0


@app.route('/')
def home():
    return render_template("index.html")

# CODE FOR REQUESTS ONLINE ON SEARCH/ASKING FROM USER
    # # return a quote
    # r = requests.get('https://api.quotable.io/random')
    # if r.status_code == 200:
    #     data = r.json()
    #     quote = f'{data["content"]} ({data["author"]})'
    # else:
    #     quote = 'I could not retrieve a quote at this time, sorry.'

    # if 'cat' in incoming_msg:
    #     # return a cat pic
    #     msg.media('https://cataas.com/cat')
    #     responded = True


# --------------------------------------
# Reciever And Processor Output Function
# --------------------------------------
@app.route('/', methods=['POST'])
def output():

    input_text = request.form["news"]
    # input_button = request.form["button"]

    text = preprocess_text(input_text)
    pred = pipeline.predict([text])

    output = ''
    if pred > 0.5:
        output = "The Given News is Real. ✅"
    elif pred < 0.5:
        output = "The Given News is Fake. ❌"
        # TODO: Add fact checker, create table or use the clickable div thingy in template
        sent = input_text.split('.')
        r = Rake()
        r.extract_keywords_from_sentences(sent)
        put_links = True
        query = ' '.join(r.get_ranked_phrases()[:3])

        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}

        links, headings = [], []
        articles = {}

        if query:
            for i in search(query, country='india', lang='en', num=3, start=0, stop=3):
                links.append(i)

            for i in links:
                url = urllib.Request(i, headers=hdr)
                soup = BeautifulSoup(urllib.urlopen(url))

                headings.append(soup.title.get_text())
                articles[i] = soup.title.get_text()

        else:
            return render_template("index.html", pred=(output), scroll="scrollable")

        if links:
            print(links)
        print(headings)
        print(articles)

        return render_template("index.html", pred=(output), scroll="scrollable", articles=articles)

    return render_template("index.html", pred=(output), scroll="scrollable")


@app.route('/explore')
def explore():
    return render_template("project.html")


if __name__ == '__main__':
    app.run(debug=True)
