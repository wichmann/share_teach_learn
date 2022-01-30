
"""
stl - share_teach_learn

Sharing network site to upload teaching resources to share it with other
teachers in the world.

Requirements:
* flask

Sources:
 * 

"""


from flask import Flask, render_template, request, current_app

import config
from model import db


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, template_folder='.')
    app.config['FLASK_ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)
    with app.app_context():
        db.create_all()
        return app


app = init_app()


@app.route('/', methods=['GET'])
def info():
    return current_app.send_static_file('main.html')


@app.route('/categories', methods=['GET'])
def categories():
    return {'categories': ['Arbeitsblätter', 'Info-Texte', 'Ergebnissicherung'], 'schoolTypes': ['Grundschule', 'Realschule', 'Hauptschule', 'Berufsschule'], 'classes': ['1', '2', '3', '4'], 'subjects': ['Politik', 'Deutsch', 'Informatik', 'Englisch']}


@app.route('/filelist', methods=['GET'])
def list_participants():
    categories = request.args.get('categories')
    schoolTypes = request.args.get('schoolTypes')
    classes = request.args.get('classes')
    subjects = request.args.get('subjects')
    return {'soredFiles': [
        {
            'filename': 'datei1.jpg',
                        'description': 'Ein Bild eines kleinen Hundes.'
        },
        {
            'filename': 'datei2.pdf',
                        'description': 'Ein Dokument mit einer Katze. Ein Dokument mit einer Katze. Ein Dokument mit einer Katze. Ein Dokument mit einer Katze.'
        },
        {
            'filename': 'ein_langer_dateiname_vom_benutzer.odt',
                        'description': 'Eine lange Datei.'
        },
        {
            'filename': 'ein_benutzer.odt',
                        'description': 'Eine llkdfjg lsfdgjklsfjd klgjslfdk glksfd klgjlksdfg kldsfklange Datei.'
        },
        {
            'filename': 'dateiname_xyz.odt',
                        'description': 'Eine sklgfjdgl jslkdfj gljlkfsdjg lksjdflkgj klsdfjglksdfklgj lksdfjklg lange Datei.'
        },
        {
            'filename': 'Arbeitsblatt.pdf',
                        'description': 'Eine lange Datei.'
        }
    ]}


if __name__ == "__main__":
    app.run(host='0.0.0.0')
