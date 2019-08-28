from flask import Flask, request

app = Flask(__name__)

@app.route('/calculatrice')
def calculatrice():
    operations = ('somme', 'soustraction', 'multipliaction','division')
    operation = request.args.get('operation')
    nom = request.args.get('nom')
    val1 = request.args.get('val1')
    val2 = request.args.get('val2')

    if nom == None :
        return 'Merde, qui T?'
    if val1 == None :
        return 'Il manque quelque chose'
    if val2 == None :
        return 'il te manque encore quelque chose'
    if operation == None:
        return 'Que veux-tu couillon ?'
    if operation not in operation:
        return 'je ne connais pas'
    # resultat = ""
    if operation == operations[0]:
        resultat = str(int(val1) + int(val2))
    if operation == operations[1]:
        resultat =  str(int(val1) - int(val2))
    if operation == operations[2]:
        resultat = str(int(val1) * int(val2))
    if operation == operations[3]:
        resultat = str(int(val1) / int(val2))
    # on saisira dans l'explorateur http://localhost:5000/query?nom=Pierre&operation='somme'&val1=10&val2=2
    return '<h1> Bonjour {}, le resultat de est {} </h1>'.format(nom, resultat)

# @app.route('/query')
# def query():
#     name = request.args.get('name')
#     location =request.args.get('location')
#     return '<h1>Hello{}, you are on the home page!</h1>'.format(name, location)



if __name__ == '__main__':
    app.run(host ='0.0.0.0', port=5000, debug=True)