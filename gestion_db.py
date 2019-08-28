from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3


app = Flask(__name__)

def connect_db():
    sql =sqlite3.connect('maBDD.s3db')
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

@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

@app.route('/viewfirstresult')
def viewfirstresult():
    db=get_db()
    cur=db.execute('select id, name, location from users')
    results= cur.fetchall()
    if len(results) == 0:
        return '<h1>No databases values</h1>'
    else :
        return'<h1>The ID is {}.The name is {}. The location is {}.</h1>'.format(results[0]['id'], results[0]['name'], results[0]['location'])

@app.route('/viewlastresult')
def viewlastresult():
    db=get_db()
    cur=db.execute('select id, name, location from users')
    results= cur.fetchall()
    if len(results) == 0:
        return '<h1>No databases values</h1>'
    else :
        return '<h1>The ID is {}.The name is {}. The location is {}.</h1>'.format(results[-1]['id'], results[-1]['name'], results[-1]['location'])


@app.route('/viewallresults')
def viewallresults():
    db=get_db()
    cur=db.execute('select id, name, location from users')
    results= cur.fetchall()

    return render_template('viewallresults.html', results=results)

@app.route('/adduser', methods=['GET','POST'])


def adduser():
    if request.method =='GET':
        return render_template('adduser.html')
    else:
        name=request.form['name']
        location=request.form['location']

        db =get_db()
        db.execute('insert into users(name,location) values (?,?)', [name, location])
        db.commit()

        return redirect(url_for('viewlastresult'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
