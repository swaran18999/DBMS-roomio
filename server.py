
from flask import Flask , render_template, session, request, redirect, url_for, jsonify
import psycopg2, hashlib, os
from flask_cors import CORS

app = Flask(__name__) 
app.secret_key = os.urandom(24)
CORS(app)

def fetchQueryResult(query, parameters):
    con = psycopg2.connect(
        database="klzhcbxk",
        user="klzhcbxk",
        password="1HbbkUWWZxRHNJR_AkxBUg1Dk_8OMcjx",
        host="batyr.db.elephantsql.com",
        port= '5432'
    )

    cur_object = con.cursor()

    cur_object.execute(query, parameters)

    result = cur_object.fetchall()

    return result

def executeQueryResult(query, parameters):
    con = psycopg2.connect(
        database="klzhcbxk",
        user="klzhcbxk",
        password="1HbbkUWWZxRHNJR_AkxBUg1Dk_8OMcjx",
        host="batyr.db.elephantsql.com",
        port= '5432'
    )

    cur_object = con.cursor()

    cur_object.execute(query, parameters)

    con.commit()

    return True

@app.route('/trial')
def trialAPI():
    return jsonify(fetchQueryResult("Select * from Users", {}))


if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=8989)