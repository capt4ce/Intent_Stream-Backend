from flask import Flask, redirect, url_for, request 
app = Flask(__name__) 
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
                print(request.get_json())
         
        else:
                query=request.args.get('query')
                return query
if __name__ == '__main__': 
    app.run(debug=True)
