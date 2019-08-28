from flask import Flask,jsonify,request

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, <br> World !"

@app.route('/coucou')
def coucou():
    return "coucou salut!"

@app.route('/json')
def json():
    return jsonify({'key' :'value', 'listkey': [1,2,3]})

@app.route('/valeur/<valeur1>')
def afficherValeur(valeur1):
    return str(valeur1)

@app.route('/somme/<valeur1>/<valeur2>')
def somme(valeur1, valeur2):
    resultat = int(valeur1)+int(valeur2)
    return str(resultat)

@app.route('/home', methods = ['POST', 'GET'],defaults={'name':'defaults'})
@app.route('/home/<string:name>', methods = ['POST','GET'])

def home(name):
    return'<h1>Hello{}, you are on the home page!</h1>'.format(name)

#from flask import Flask, jsonify, request
# on saisira dans l'explorateur http://localhost:5000/query?name=Pierre&location=Toulouse

@app.route('/query')
def query():
    name = request.args.get('name')
    location =request.args.get('location')
    return '<h1>Hello{}, you are on the home page!</h1>'.format(name, location)

@app.route('/caculatrice')

def query():
    operations = ('somme', 'soustraction', 'multipliaction','division')
    operation = request.args.get('operation')
    nom = request.args.get('nom')
    val1 = request.args.get('val1')
    val2 = request.args.get('val2')

    if nom == None :
        return'Merde, qui T?'
    if val1 == None :
        return 'Il manque quelque chose'
    if val2 == None :
        return 'il te manque encore quelque chose'
    if operation == None:
        return 'Que veux-tu couillon ?'
    if operation not in operation:
        return 'je ne connais pas'
    resultat = ""
    if operation == operations[0]:
        resultat = str(int(val1) + int(val2))
    if operation == operations[1]:
        resultat =  str(int(val1) - int(val2))
    if operation == operations[2]:
        resultat = str(int(val1) * int(val2))
    if operation == operations[3]:
        resultat =str(int(val1) / int(val2))
    # on saisira dans l'explorateur http://localhost:5000/query?nom=Pierre&operation='somme'&val1=10&val2=2
    return '<h1> Bonjour {}, le resultat de est {} </h1>'.format(nom, resultat)


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
    name= request.form['name']
    location = request.form['location']
    return '<h1>Hello {}.You are form{}. You have submitted the form succesfully </h1>'. format(name, location)

if __name__ == '__main__':
    app.run(host ='0.0.0.0', port=5000, debug=True)
# app.run lance le serveur
# port represente le port d'écoute du serveur
# host 0.0.0.0 toutes les machines peuvent effectuer des requetes
# host avec propre adresse IP => seule la machine avec l'adresse ip peut effectuer une requete
# debug = true pour avoir un retour
# les ports vont de 1 à 65535
# les ports en dessous de 1024 sont réservés au system