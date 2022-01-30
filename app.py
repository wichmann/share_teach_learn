
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
from model import db, Category, CategoryType


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
        from model import initializeCategories
        initializeCategories()
        return app


app = init_app()


@app.route('/', methods=['GET'])
def info():
    return current_app.send_static_file('main.html')


@app.route('/categories', methods=['GET', 'POST'])
def categories():
    categories = {'contentTypes': [c.name for c in Category.query.filter_by(type=CategoryType.contentTypes)],
                  'schoolTypes': [c.name for c in Category.query.filter_by(type=CategoryType.schoolTypes)],
                  'classes': [c.name for c in Category.query.filter_by(type=CategoryType.classes)],
                  'subjects': [c.name for c in Category.query.filter_by(type=CategoryType.subjects)]}
    if request.method == 'GET':
        return categories
    elif request.method == 'POST':
        # TODO: Add category to list.
        pass


@app.route('/filelist', methods=['POST'])
def list_participants():
    chosenCategories = request.json['categories']
    print(chosenCategories)
    allFiles =[
        {
            'filename': 'datei1.jpg',
                        'description': 'Ein Bild eines kleinen Hundes.',
                        'categories': ['Arbeitsblätter', 'Grundschule']
        },
        {
            'filename': 'datei2.pdf',
                        'description': 'Ein Dokument mit einer Katze. Ein Dokument mit einer Katze. Ein Dokument mit einer Katze. Ein Dokument mit einer Katze.',
                        'categories': ['Info-Texte', 'Realschule']
        },
        {
            'filename': 'ein_langer_dateiname_vom_benutzer.odt',
                        'description': 'Eine lange Datei.',
                        'categories': ['Arbeitsblätter', 'Berufsschule']
        },
        {
            'filename': 'ein_benutzer.odt',
                        'description': 'Eine llkdfjg lsfdgjklsfjd klgjslfdk glksfd klgjlksdfg kldsfklange Datei.',
                        'categories': ['Info-Texte', 'Grundschule']
        },
        {
            'filename': 'dateiname_xyz.odt',
                        'description': 'Eine sklgfjdgl jslkdfj gljlkfsdjg lksjdflkgj klsdfjglksdfklgj lksdfjklg lange Datei.',
                        'categories': ['Info-Texte', 'Berufsschule']
        },
        {
            'filename': 'Arbeitsblatt.pdf',
                        'description': 'Eine lange Datei.',
                        'categories': ['Ergebnissicherung', 'Realschule']
        }
    ]
    return  {'storedFiles': [f for f in allFiles if chosenCategories[0] in f['categories']]}


if __name__ == "__main__":
    app.run(host='0.0.0.0')
