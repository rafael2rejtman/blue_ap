
import pickle
from flask import Flask, render_template
from flask import request, redirect, g
import os
# import sqlite3

# getting our trained model from a file we created earlier
model = pickle.load(open("model.pkl","r"))

port = int(os.environ.get("PORT", 5000))

app = Flask(__name__)

# @app.before_request
# def before_request():
# 	g.db = sqlite3.connect("emails.db")

# @app.teardown_request
# def teardown_request(exception):
# 	if hasattr(g, 'db'):
# 		g.db.close()	

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict')
def predict():
	return render_template('predict.html')

@app.route('/result', methods=['GET'])
def result():
    #grabbing a set of features from the request's body
    foo = request.args.getlist('foo')
    
    # our model rates the wine based on the input array
    prediction = model.predict([foo])
    
    #sending our response object back as json
    return render_template('result.html', prediction=prediction)

@app.route('/insert')
def insert():
		return render_template('insert.html')    

# @app.route('/signup', methods = ['POST'])
# def signup():
# 	email = request.form['email']
# 	g.db.execute("INSERT INTO email_addresses VALUES (?)", [email])
# 	g.db.commit()
# 	return redirect('/')	

# @app.route('/emails.html')
# def emails():
# 	email_addresses = g.db.execute("SELECT email FROM email_addresses").fetchall()	
# 	return render_template('emails.html', email_addresses=email_addresses)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)