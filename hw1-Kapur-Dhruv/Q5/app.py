from flask import Flask,render_template,json,request
app = Flask(__name__)

@app.route("/")
def hello():
	return render_template('hello.html')
@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/signupuser', methods=['POST'])
def signupuser():
    user =  request.form['username'];
    password = request.form['password'];
    return json.dumps({'status':'OK','user':user,'pass':password});
if __name__=="__main__":
  app.run()	
