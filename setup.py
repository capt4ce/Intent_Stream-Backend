from DExyS import main as dexys
from flask import jsonify
from flask import Flask, redirect,render_template, url_for, request 
import requests
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
            query=request.args.get('query')
            # keywords,suggested_keywords, #result=dexys.querySearch(query)
            data=[]
            ky=[]
            url='https://www.googleapis.com/customsearch/v1?q='+query+'&key=AIzaSyASWpsbC2yHZZA7IVQWuHGTLbFr6I7y6XI&cx=001234642073522909578:dw7qnkw1euk'
            print(url)
            s1=requests.get(url)
            print(s1)
            # pr=s1['response']['items']
            # for d in pr:
            #     data.append({name:pr.link,description:pr.snippet})

            # s2=requests.get('http://api.bing.com/osjson.aspx?query='+query)
            # pr=s2[1]
            # for idx in range(len(pr)):
            #     if idx!=0:
            #         ky.append({name:pr[idx]})

            res = {'success':True,'data':data,'suggested_keywords':ky}
            return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)


