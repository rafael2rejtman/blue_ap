
import pickle
from flask import Flask, render_template
from flask import request, redirect, g
import os
import psycopg2
from psycopg2 import Error
# import sqlite3

DATABASE_URL = os.environ['DATABASE_URL']

app = Flask(__name__)

with open("model.pkl", 'rb') as file:
    model = pickle.load(file)

port = int(os.environ.get("PORT", 5000))

@app.before_request
def before_request():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error ::
         print ("Error while connecting to PostgreSQL", error)

@app.teardown_request
def teardown_request(exception):
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")    

@app.route('/result', methods=['GET'])
def result():
    #grabbing a set of features from the request's body
    foo = request.args.getlist('foo')

    print(foo)
    
    # our model rates the wine based on the input array
    prediction = model.predict([list(map(float,foo))])
    
    #sending our response object back as json
    return render_template('result.html', prediction=prediction)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert')
def insert():
		return render_template('insert.html')  


@app.route('/database')
def database():
        
    create_table_query = '''CREATE TABLE mobile
          (ID INT PRIMARY KEY     NOT NULL,
          MODEL           TEXT    NOT NULL,
          PRICE         REAL); '''
    
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")        
    
    return redirect('/')    

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