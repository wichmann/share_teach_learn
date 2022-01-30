
"""
stl - share_teach_learn

Sharing network site to upload teaching resources to share it with other
teachers in the world.

Requirements:
* flask

Sources:
 * 

"""


from flask import Flask, request, current_app

import config
from model import db, File, Category, FileCategory, CategoryType, initializeCategories


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


@app.route('/files/filter', methods=['POST'])
def filter_files():
    chosenCategories = request.json['categories']
    print(chosenCategories[0])
    filteredList = File.query.join(FileCategory).join(Category).filter(Category.name == chosenCategories[0])
    allFiles = [{'id': f.id, 'filename': f.filename, 'description': f.description,
                 'preview': f'/files/preview/{f.uuid}',
                 'categories': [c.name for c in f.categories]} for f in filteredList]
    return  {'storedFiles': allFiles}


@app.route('/files/preview/<uuid>', methods=['GET'])
def send_previews(uuid):
    print(f'Sending preview for {uuid}')
    return current_app.send_static_file('images/defaultpreview.png')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
