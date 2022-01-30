
"""
stl - share_teach_learn

Sharing network site to upload teaching resources to share it with other
teachers in the world.

Requirements:
* flask

Sources:
 * 

"""

import os
import uuid
import json
from PIL import Image
from io import StringIO, BytesIO

from werkzeug.utils import secure_filename
from flask import Flask, request, current_app, abort, jsonify, send_file
from preview_generator.manager import PreviewManager

import config
from model import db, File, Category, FileCategory, CategoryType, initializeCategories


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, template_folder='.')
    app.config['FLASK_ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    UPLOAD_FOLDER = './uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # initialize thumbnail generator
    cache_path = '/tmp/preview_cache'
    global preview_manager
    preview_manager = PreviewManager(cache_path, create_folder=True)

    db.init_app(app)
    with app.app_context():
        db.create_all()
        initializeCategories()
        return app


app = init_app()


# TODO: Check whether to use a /v1/ path element!?
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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def get_file_extension(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    else:
        return ''


@app.route('/files', methods=['POST'])
def upload_file():
    print('Uploading file...')
    if 'file' not in request.files:
        return abort(400)
    file = request.files['file']
    if file.filename == '':
        return abort(400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        new_uuid = uuid.uuid4()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_uuid.hex))
        chosenCategories = []
        for c in json.loads(request.form.get('categories')):
            result = Category.query.filter_by(name=c).first()
            if result:
                chosenCategories.append(result)
        new_file = File(filename=filename, uuid=new_uuid.hex, description=request.form.get(
            'description'), categories=chosenCategories)
        db.session.add(new_file)
        db.session.commit()
        return jsonify({'success': True}), 200
    return current_app.send_static_file('images/defaultpreview.png')


@app.route('/files/filter', methods=['POST'])
def filter_files():
    chosenCategories = request.json['categories']
    # TODO: Add pagination.
    filteredList = File.query.join(FileCategory).join(
        Category).filter(Category.name.in_(chosenCategories))
    allFiles = [{'id': f.uuid, 'filename': f.filename, 'description': f.description,
                 'preview': f'/files/{f.uuid}/preview',
                 'download': f'/files/{f.uuid}',
                 'categories': [c.name for c in f.categories]} for f in filteredList]
    return {'storedFiles': allFiles}


@app.route('/files/<uuid>/preview', methods=['GET'])
def send_previews(uuid):
    print(f'Sending preview for {uuid}')
    result = File.query.filter_by(uuid=uuid).first()
    if result:
        try:
            path_to_preview_image = preview_manager.get_jpeg_preview(
                os.path.join(app.config['UPLOAD_FOLDER'], uuid), width=config.PREVIEW_WIDTH, height=config.PREVIEW_HEIGHT)
            return send_file(path_to_preview_image)
        except FileNotFoundError:
            pass
    return current_app.send_static_file('images/defaultpreview.png')


@app.route('/files/<uuid>', methods=['GET', 'DELETE'])
def send_file_content(uuid):
    if request.method == 'GET':
        result = File.query.filter_by(uuid=uuid).first()
        if result:
            print(f'Sending file for {uuid}')
            return send_file(os.path.join(app.config['UPLOAD_FOLDER'], uuid),
                             download_name=result.filename)
        else:
            # TODO: Check status code.
            abort(400)
    elif request.method == 'DELETE':
        result = File.query.filter_by(uuid=uuid).first()
        if result:
            print(f'Deleting file for {uuid}')
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], uuid))
            except FileNotFoundError as e:
                print(e)
            db.session.delete(result)
            db.session.commit()
            return jsonify({'success': True}), 200
        else:
            # TODO: Check status code.
            abort(400)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
