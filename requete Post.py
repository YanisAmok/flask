from flask import Flask, jsonify, request, render_template


app = Flask(__name__)

@app.route('/theform')
def theform():
    return '''<form method="POST" action="/process">
    Nom:
    <input type="text" name= "name">
    Lieu:
    <input type="text" name= "location">
    <input type= "submit" value="Submit">.
    </form>'''


@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']
    return '<h1>Hello {}.You are form{}. You have submitted the form succesfully </h1>'. format(name, location)

### 2 requetes dans une meme methode
@app.route('/theform2', methods =['GET','POST'])

def theform2():
    if request.method == 'GET':
        return '''<form method="POST" action="/theform2">
    <input type="text" name= "name">
    <input type="text" name= "location">
    <input type= "submit" value="Submit">
    </form>'''
    else:
        name =request.form['name']
        location= request.form['location']
        return '<h1>Hello {}.You are form{}. You have submitted the form successfully </h1>'.format(name, location)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/affiche_somme/<valeur1>/<valeur2>')
def affiche_somme(valeur1,valeur2):
    from datetime import date
    d = date.today().isoformat()
    resultat =int(valeur1)+int(valeur2)
    return render_template("somme.html", la_date=d, v1=valeur1, v2=valeur2, res=resultat)

@app.route('/home', methods = ['POST', 'GET'],defaults={'name':'Default'})
@app.route('/home/<string:name>', methods = ['POST','GET'])

def home(name):
    return render_template('home.html', name=name, display=False)



@app.route('/home2', methods = ['POST', 'GET'], defaults={'name':'Default'})
@app.route('/home2/<string:name>', methods=['POST','GET'])

def home2(name):
    return render_template('home2.html', name=name, display=True, mylist=['one', 'two', 'three', 'four'],listofdictionaries=[{'name':'Zach'}, {'name':'Zoe'}])



if __name__ == '__main__':
    app.run(host ='0.0.0.0', port=5000, debug=True)