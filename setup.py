from DExyS import main as dexys
from flask import jsonify
from flask import Flask, redirect,render_template, url_for, request 
import requests
import json
import ast
from flask_cors import CORS
import nltk

# def google_search_dummy():
#     a ="""
#             {
#         "items": [
#             {
#             "kind": "customsearch#result",
#             "title": "Computer - Wikipedia",
#             "displayLink": "en.wikipedia.org",
#             "snippet": "A computer is a device that can be instructed to carry out arbitrary sequences of \narithmetic or logical operations automatically. The ability of computers to follow \ngeneralized sets of operations, called programs, enables them to perform an \nextremely wide range of tasks. Such computers are used as control systems for a \nvery ...",
#             "cacheId": "fCBvEeFb9p8J",
#             "pagemap": {
#                 "cse_thumbnail": [
#                 {
#                 "width": "119",
#                 "height": "79",
#                 }
#                 ],
#                 "metatags": [
#                 {
#                 "referrer": "origin-when-cross-origin"
#                 }
#                 ],
#                 "cse_image": [

#                 ]
#             }
            
#             ]
#             }
#     """
#     return json.loads(a)


app = Flask(__name__)
CORS(app)
@app.route('/destination/add', methods=['GET', 'POST'])
def destination_add():
    if request.method == 'POST':
        a= request.form['destination_country']
        b=request.form['destination_name']
        c=request.form['tags']
        d=request.form['choice']
        return a+"\n"+b+"\n"+c+"\n"+d
        
    return render_template("app.html")

@app.route('/success/<name>') 
def success(name):
        return 'welcome %s' % name 
@app.route('/',methods=['GET']) 
def test(): 
    user=request.args.get('nm') 
    return redirect(url_for('success',name=user))

@app.route('/search',methods=['POST','GET'])
def search():
        if request.method=='POST':
                req=request.get_json()
                return jsonify(req)
         
        else:
            # query=request.args.get('query')
            # keywords,suggested_keywords, result=dexys.querySearch(query)
            # res = {'success':True,'data':result,'search_keywords':keywords,'suggested_keywords':suggested_keywords}
            # return jsonify(res)


            query=request.args.get('query') #   .lower()
            qSplitted = query.split()
            # keywords,suggested_keywords, #result=dexys.querySearch(query)
            data=[]
            ky=[]
            url='https://www.googleapis.com/customsearch/v1?q='+query+'&key=AIzaSyASWpsbC2yHZZA7IVQWuHGTLbFr6I7y6XI&cx=001234642073522909578:dw7qnkw1euk'
            print(url)
            s1=requests.get(url)
            s2 = json.loads(s1.text)
            # s2=google_search_dummy
            pr=s2["items"]
            # print(pr)
            for d in pr:
                tagsTokens=nltk.word_tokenize(d["title"])
                filteredTags = [w for w in tagsTokens if len(w)>3]
                data.append({"name":d["title"],"link":d["link"],"description":d["snippet"], "tags":list(set(filteredTags))})

            s1=requests.get('http://api.bing.com/osjson.aspx?query='+query)
            s2=json.loads(s1.text)
            pr=s2[1]
            for idx in range(len(pr)):
                if idx!=0:
                    word = pr[idx]
                    for q in qSplitted:
                        q=q.lower()
                        word = word.replace(q,'')
                    ky.append({"title":word.strip()})

            print(str(qSplitted))
            print(str(ky))
            formatedQSplit = []
            for q in qSplitted:
                formatedQSplit.append({"title":q})
            keywords = formatedQSplit+ky
            print(str(keywords))

            res = {'success':True,'data':data,'suggested_keywords':keywords, 'query':query}
            return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)