from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
from datetime import date
import sqlite3
import json


app = Flask(__name__)

def connect_db():
    sql =sqlite3.connect('Plaque.s3db')
    sql.row_factory=sqlite3.Row#avoir un dict plutôt qu'un tuple
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db=connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/newDetection', methods=['POST'])
def newDetection():
    # print("reception")
    recup = request.get_json()
    dataJson = json.loads(recup)
    # print(dataJson)
    # traitement BDD

    d = dataJson['datetime']
    p = dataJson['plaque']
    i = dataJson['image']

    db = get_db()
    db.execute('insert into plaques(datetime, plaque, image) values(?,?,?)', [d, p, i])
    db.commit()

    return "Ok"


@app.route('/toutesPlaques')
def toutesPlaques():
    db = get_db()
    cur = db.execute('select datetime, plaque, image from plaques')
    results = cur.fetchall()
    return render_template('toutesPlaques.html', results=results)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)