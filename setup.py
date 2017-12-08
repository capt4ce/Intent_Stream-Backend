from DExyS import main as dexys
from flask import jsonify
from flask import Flask, redirect,render_template, url_for, request 
import requests
import json
from flask_cors import CORS


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
            qSplitted = query.lower().split()
            # keywords,suggested_keywords, #result=dexys.querySearch(query)
            data=[]
            ky=[]
            url='https://www.googleapis.com/customsearch/v1?q='+query+'&key=AIzaSyASWpsbC2yHZZA7IVQWuHGTLbFr6I7y6XI&cx=001234642073522909578:dw7qnkw1euk'
            print(url)
            s1=requests.get(url)
            s2 = json.loads(s1.text)
            pr=s2["items"]
            # print(pr)
            for d in pr:
                data.append({"name":d["title"],"link":d["link"],"description":d["snippet"], "tags":["aaa","bbb","ccc"]})

            s1=requests.get('http://api.bing.com/osjson.aspx?query='+query)
            s2=json.loads(s1.text)
            pr=s2[1]
            for idx in range(len(pr)):
                if idx!=0:
                    word = pr[idx]
                    for q in qSplitted:
                        word = word.replace(q,'')
                    ky.append({"title":word.strip()})

            res = {'success':True,'data':data,'suggested_keywords':ky, 'query':query}
            return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)


