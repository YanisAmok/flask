from flask import Flask,g, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db=connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def dict_factory(cursor, row):
    d ={}
    for idx, col in enumerate(cursor.description):
        # d[col[0]]
        d[col[0]] = row[idx]
    return d


def connect_db():
    sql =sqlite3.connect('gestioneleves.sqlite3')
    #sql.row_factory=sqlite3.Row#avoir un dict plutôt qu'un tuple
    sql.row_factory = dict_factory
    return sql

@app.route('/eleve', methods=['GET'])# Pour afficher tous les eleves
def eleve():
    db= get_db()
    # eleve_cur= db.execute('select id, nom, prenom, adresse, idclasse)
    eleve_cur=db.execute('SELECT eleve.nom, eleve.prenom, eleve.adresse, eleve.id, classe.id AS idclasse, etablissement.id AS idetablissement, etablissement.nom AS nometablissement, classe.nom AS nomclasse, academie.nom AS nomacademie, academie.id AS idacademie FROM eleve INNER JOIN classe ON classe.id = eleve.idclasse INNER JOIN etablissement ON etablissement.id = classe.idetablisement INNER JOIN academie ON academie.id = etablissement.idacademie')
    eleve= eleve_cur.fetchall()
    return jsonify({'eleve': eleve})


@app.route('/eleve/<int:eleve_id>', methods=['GET'])#afficher un seul eleve
def eleveid(eleve_id):
    db = get_db()
    # eleve_cur= db.execute('select id, nom, prenom, adresse, idclasse)
    eleve_cur=db.execute('SELECT eleve.nom, eleve.prenom, eleve.adresse, eleve.id, classe.id AS idclasse, etablissement.id AS idetablissement, etablissement.nom AS nometablissement, classe.nom AS nomclasse, academie.nom AS nomacademie, academie.id AS idacademie FROM eleve INNER JOIN classe ON classe.id = eleve.idclasse INNER JOIN etablissement ON etablissement.id = classe.idetablisement INNER JOIN academie ON academie.id = etablissement.idacademie where eleve.id={}'.format(eleve_id))
    eleve= eleve_cur.fetchone()
    return jsonify({'eleve': eleve})


@app.route('/eleve/<int:eleve_id>', methods=['PUT'])
def put_eleve(eleve_id):
    nom = request.args.get('nom')
    prenom = request.args.get('prenom')
    adresse = request.args.get('adresse')

    if nom is None and prenom is None and adresse is None:
        return jsonify({'status': 'no data in the request'})

    db = get_db()

    if nom is not None:
        req = "UPDATE eleve set nom='{}' WHERE id='{}'".format(nom, eleve_id)
        db.execute(req)
        db.commit()

    if prenom is not None:
        db.execute("UPDATE eleve set prenom='{}' WHERE id='{}'".format(prenom, eleve_id))
        db.commit()

    if adresse is not None:
        db.execute("UPDATE eleve set adresse='{}' WHERE id='{}'".format(adresse, eleve_id))
        db.commit()

    return jsonify({'status': 'ok'})

@app.route('/eleve/<int:eleve_id>', methods=['DELETE'])
def delete_eleve(eleve_id):


    db = get_db()
    db.execute("DELETE FROM eleve WHERE id='{}'".format(eleve_id))
    db.commit()

    return jsonify({'status': 'ok'})

@app.route('/eleve/<int:eleve_id>', methods=['POST'])
def post_eleve():
    recup =request.get_json()

    if 'nom' not in recup or 'prenom' not in recup or 'adresse' not in recup or 'idclasse' not in recup:
        return jsonify({'status': 'no data in the request'})
    db = get_db()
    nom=recup['nom']
    prenom=recup['prenom']
    adresse=recup['adresse']
    idclasse=recup['idclasse']
    req = "insert into eleve (nom, prenom, adresse, idclasse) values ('{}','{}','{}')".format(nom, prenom, adresse, idclasse)

    db.execute(req)
    db.commit()

    return jsonify({'status': 'ok'})

# @app.route('Radar/eleve/<int:eleve_id>', methods =['GET'])
# def AfficheRadar(eleveid):
#     db= get_db()
#     db.execute('SELECT matiere.nom AS matierenom, moyenne FROM MoyennesMatieres WHERE eleveid={}').format(eleve_id)
#     eleve= eleve_cur.fetchall()

@app.route('/radar/<int:eleve_id>', methods=['GET'])
def get_radar(eleve_id):
    db = get_db()
    req = f" SELECT matierenom, moyenne from MoyennesMatieres where eleveid = {eleve_id}"
    eleve_cur = db.execute(req)
    moyenneR = eleve_cur.fetchall()

    listMatElev = []
    listMoyElev = []
    for m in moyenneR:
        matNom = m['matierenom']
        listMatElev.append(matNom)
        moy = m['moyenne']
        listMoyElev.append(moy)

    angles = np.linspace(0, 2 * np.pi, len(moyenneR), endpoint=False)
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, listMoyElev, 'o-', linewidth=2, label="Elève")
    ax.fill(angles, listMoyElev, alpha=0.2)
    ax.set_thetagrids(angles * 180 / np.pi, listMatElev)
    plt.yticks([2, 4, 6, 8, 10, 12, 14, 16, 18], color="grey", size=7)
    plt.ylim(0, 20)
    ax.set_title(f'{eleve_id}')
    ax.grid(True)
    plt.legend(loc='upper right')
    #     # plt.show()
    plt.savefig("radar_tmp.png")

    return send_file("radar_tmp.png", attachment_filename='fig_eleve{}.png'.format(eleve_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)