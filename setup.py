from DExyS import main as dexys
from flask import jsonify
from flask import Flask, redirect,render_template, url_for, request 
app = Flask(__name__)
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
            query=request.args.get('query')
            result=dexys.querySearch(query)
            res = {'sucess':True,'data':result}
            return jsonify(res)
# print()
# print('# setup.py')
if __name__ == '__main__':
    app.run(debug=True)


